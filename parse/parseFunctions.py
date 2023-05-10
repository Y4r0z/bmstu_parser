from aiohttp import ClientSession
from os import environ, path
from bs4 import BeautifulSoup as bs ,Tag
from db.models import Course, Teacher, Activity, File
import logging as log
from db.enums import ActivityTypes, FileExtensions
import time
from urllib.parse import unquote_plus


async def getCookie(session : ClientSession) -> str:
    """
    Для входа недостаточно лишь логина и пароля, требуется так называемые `Cookie,`
    который по неизвестным мне причинам нахдятся на странице входа, как скрытое поле.
    
    Зачем они нужны при входе, я не знаю. Также я заметил, что и рандомная строка вместо
    `Cookie` иногда тоже позволяет войти.
    """
    async with session.get('https://proxy.bmstu.ru:8443/cas/login?service=https://e-learning.bmstu.ru/kaluga/login/index.php?authCAS=CAS')\
    as r:
        page = bs(await r.text(), 'html.parser')
    find = page.find('section', class_ = 'row btn-row')
    return find.findAll('input', type='hidden')[0]['value']

async def getPayload(session : ClientSession) -> dict:
    """
    Сформировать `payload` для post запроса.
    """
    return {
        'username' : environ.get("BMSTULogin"),
        'password' : environ.get("BMSTUPassword"),
        'execution' : await getCookie(session),
        '_eventId' : 'submit'
    }



async def parseCourse(coursebox : Tag) -> Course:
    """
    Преобразует html курса в объект класса `Course`.

    Курсом является каждый предмет на главной странице сайта.
    """
    log.info(f'Async parse: Course')
    nm = coursebox.find(class_ = 'coursename').find('a')
    teachers = await parseTeachers(coursebox)
    crs = Course(name=nm.text, link = nm.get('href'), teachers=teachers)
    log.info(f'Parsed course: {str(crs)}')
    #crs.activities = await self.parseActivities(crs)
    return crs

async def parseTeachers(coursebox : Tag) -> list[Teacher]:
    """
    Парсит список преподавателей из html курса.

    Список преподавателей расположен под курсом на сайте.

    TODO:
    * Парсинг email
    """
    log.info(f'Async parse: Teachers')
    teachers : Tag = coursebox.find('ul', class_ = 'teachers')
    res = []
    if teachers is None:
        return res
    li : Tag
    for li in teachers.find_all('li'):
        a : Tag = li.find('a')
        res.append(Teacher(name=a.text, link=a.get('href')))
    return res

async def parseActivities(session : ClientSession, course : Course) -> list[Activity]:
    """
    Парсит список активностей из объекта курса.

    Активностями называются все объекты внутри курса.

    Если у активности нет ссылки (если она закрыта для пользователя), то
    парсер её пропустит.
    """
    log.info(f'Async parse: Activties from {str(course)}')
    res = []
    async with session.get(course.link) as r:
        text = await r.text()
        page = bs(text, 'html.parser')
    find = page.findAll('li', class_ = 'activity')
    a : Tag
    for a in find:
        #Если не найден тип активности, то она будет неизвестной
        type = ActivityTypes.Undefined
        for at in ActivityTypes:
            if a['class'][1].lower() == at.name.lower():
                type = at
        #Активность без контента - пропускается
        if type == ActivityTypes.Label: continue
        inst = a.find(class_='activityinstance')
        #Если не найдена ссылка на активность, то она None
        try:
            link = inst.find('a', class_='aalink').get('href')
        except Exception as e:
            log.info('Unable to get activity link: ' + str(e))
            link = None
            continue
        name = inst.find(class_='instancename').contents[0]
        if type == ActivityTypes.Undefined: log.warning(f'activity type is undefined: {a["class"][1]} | {course.name}, {name}, {link}')
        act = Activity(course=course, name=name, link=link, type=type)
        res.append(act)
    return res


async def parseFiles(session : ClientSession, activity : Activity) -> list[File]:
    """
    Парсит список файлов из объекта активности.

    Каждому файлу обязательно соответствуент активность,
    даже если они оба - один и тот же объект на сайте.

    TODO:
    * Парсить звуковые файлы. Они встречаются редко, поэтому их можно отложить.
    * Изменить систему выбора парсера c if else на более подходящее ООП.

    """
    log.info(f'Async parse: Files from {str(activity)}')
    AT = ActivityTypes
    if activity.link is None or len(activity.link) < 2 or\
        activity.type in [AT.Undefined, AT.Chat, AT.Forum, AT.Label, AT.Lession,
                            AT.Quiz, AT.Url, AT.Workshop]:
        log.warning('Attempt to get files for incorrect activity:' + activity.name)
        return []
    res = []
    if activity.type == AT.Assign:
        res.extend(await getFilesAssign(session, activity))
    elif activity.type == AT.Resource:
        res.extend(await getResource(session, activity))
    elif activity.type == AT.Folder:
        res.extend(await getFilesFolder(session, activity))
    
    return res


"""
Далее идут отдельные парсеры для каждого типа файлов.
"""

async def getFilesAssign(session : ClientSession, activity : Activity) -> list[File]:
    res = []
    async with session.get(activity.link) as r:
        text = await r.text()
        page = bs(text, 'html.parser')
    find = page.findAll(class_='fileuploadsubmission')
    f : Tag
    for f in find:
        try:
            fileTag = f.find('a',)
            link = fileTag.get('href')
            name, ext = path.splitext(fileTag.text)
            file = File(name=name, link=link, activity=activity, extension=FileExtensions.Get(ext))
            log.info(f'Parsed file: {str(file)}')
            res.append(file)
        except Exception as e:
            log.warning('Can\'t find in assign file: ' + str(e))
    return res

async def getResource(session : ClientSession, activity : Activity) -> list[File]:
    async with session.head(activity.link, allow_redirects=True) as s:
        link : str = str(s.url)
    try:
        rawName = link.split('/')[-1].split('?')[0]
        rawName = unquote_plus(rawName, encoding='utf-8')
        name, rawExt = path.splitext(rawName)
        file = File(name=activity.name, link=link, activity=activity, extension=FileExtensions.Get(rawExt))
        log.info(f'Parsed file: {str(file)}')
        return [file]
    except Exception as e:
        log.error(f'Can\'t parse resource file for activity: {str(activity)}\n {str(e)}')
        return []
    
async def getFilesFolder(session : ClientSession, activity : Activity) -> list[File]:
    res = []
    async with session.get(activity.link) as r:
        text = await r.text()
        page = bs(text, 'html.parser')
    find = page.findAll('span', class_='fp-filename-icon')
    f : Tag
    for f in find:
        try:
            rawFile = f.find('a')
            link = str(rawFile.get('href'))
            rawName = link.split('/')[-1].split('?')[0]
            rawName = unquote_plus(rawName, encoding='utf-8')
            name, rawExt = path.splitext(rawName)
            file = File(name=name, link=link, activity=activity, extension=FileExtensions.Get(rawExt))
            log.info(f'Parsed file: {str(file)}')
            res.append(file)
        except Exception as e:
            log.error(f'Can\'t parse folder file from activity: {str(activity)}.\n{str(e)}')
    return res
