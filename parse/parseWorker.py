import asyncio
from db.models import Course, Activity, File
from bs4 import BeautifulSoup as bs, Tag
import logging as log
from aiohttp import CookieJar, ClientSession
import parse.parseFunctions as pf
import os

class ParseWorker:
    """
    Этот класс отвечает за работу парсера из отдельной сессии.
    Для каждого экземпляра производится вход, но все они работают
    в одном цикле `asyncio`.
    """
    Count = 0
    CookiePath = 'data/workers/'

    @classmethod
    async def create(cls):
        instance = ParseWorker()
        await instance.__init()
        return instance

    async def __init(self):
        self.busy = True
        self.mainPage : bs
        self.cookies = CookieJar()
        self.session : ClientSession = ClientSession(cookie_jar=self.cookies)
        self.id = ParseWorker.Count
        ParseWorker.Count += 1
        log.info(f'Parse Worker {self.id} created')
        await self.checkLogin()
        self.busy = False
    
    def __del__(self):
        asyncio.shield(self.close())
    
    async def close(self):
        self.saveCookies()
        await self.session.close()

    async def checkLogin(self):
        """
        Использование данного метода позволяет сэкономить время на автризации.
        
        После завершения работы программа сохраняет все использованные сессии
        в файлы, этот метод открывает эти файлы и проверяет работоспособность
        сессий.

        TODO:
        * Декоратор для `busy`
        """
        # Загрузка сессии из файла
        try:
            self.loadCookies()
            log.info('Cookie загружены из файла')
        except Exception as e:
            log.warning(f'Не удалось загрузить Cookie из файла: {str(e)}')
        # Открытие сайта без входа
        try:
            async with self.session.get('https://e-learning.bmstu.ru/kaluga/') as r:
                text = await r.text()
                page = bs(text, 'html.parser')
        except Exception as e:
            log.error("Unable to connect to e-learning server!")
            return
        # Проверка работоспособности сессии
        find = page.find('span', class_ = 'login')
        if find:
            log.info("Первичный вход не удался. Создание новой сессии.")
            async with self.session.post(
            'https://proxy.bmstu.ru:8443/cas/login?service=https%3A%2F%2Fe-learning.bmstu.ru%2Fkaluga%2Flogin%2Findex.php%3FauthCAS%3DCAS',
            data = await pf.getPayload(self.session)) as r:
                text = await r.text()
                self.mainPage = bs(text, 'html.parser')
        else:
            log.info("Произведен первичный вход по сохраненной сессии.")
            self.mainPage = page


    async def getAllCourses(self) -> list[Course]:
        self.busy = True
        res = []
        coursebox : Tag
        for coursebox in self.mainPage.find('div', class_='courses').find_all('div', class_='coursebox'):
            course = await self.getCourse(coursebox)
            res.append(course)
        self.busy = False
        return res

    async def getCourse(self, coursebox : Tag) -> Course:
        self.busy = True
        res = await pf.parseCourse(coursebox)
        self.busy = False
        return res

    async def getActivities(self, course : Course) -> list[Activity]:
        self.busy = True
        res = await pf.parseActivities(self.session, course)
        course.activities = res
        self.busy = False
        return res

    async def getFiles(self, activity : Activity) -> list[File]:
        self.busy = True
        res = await pf.parseFiles(self.session, activity)
        activity.files = res
        self.busy = False
        return res

    
    def saveCookies(self):
        path = self.CookiePath + f'cookie{self.id}'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.cookies.save(path)
    
    def loadCookies(self):
        self.cookies.load(self.CookiePath + f'cookie{self.id}')