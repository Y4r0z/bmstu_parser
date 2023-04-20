from aiohttp import ClientSession
from os import environ, path
from bs4 import BeautifulSoup as bs ,Tag
from db.models import Course, Teacher, Activity, File
import logging as log
from db.enums import ActivityTypes, FileExtensions
import time
from urllib.parse import unquote_plus


async def getCookie(session : ClientSession) -> str:
    async with session.get('https://proxy.bmstu.ru:8443/cas/login?service=https://e-learning.bmstu.ru/kaluga/login/index.php?authCAS=CAS')\
    as r:
        page = bs(await r.text(), 'html.parser')
    find = page.find('section', class_ = 'row btn-row')
    return find.findAll('input', type='hidden')[0]['value']

async def getPayload(session : ClientSession) -> dict:
    return {
        'username' : environ.get("BMSTULogin"),
        'password' : environ.get("BMSTUPassword"),
        'execution' : await getCookie(session),
        '_eventId' : 'submit'
    }



async def parseCourse(coursebox : Tag) -> Course:
    log.info(f'Async parse: Course')
    nm = coursebox.find(class_ = 'coursename').find('a')
    teachers = await parseTeachers(coursebox)
    crs = Course(name=nm.text, link = nm.get('href'), teachers=teachers)
    log.info(f'Parsed course: {str(crs)}')
    #crs.activities = await self.parseActivities(crs)
    return crs

async def parseTeachers(coursebox : Tag) -> list[Teacher]:
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
    log.info(f'Async parse: Activties from {str(course)}')
    res = []
    async with session.get(course.link) as r:
        text = await r.text()
        page = bs(text, 'html.parser')
    find = page.findAll('li', class_ = 'activity')
    a : Tag
    for a in find:
        #Если не найден тип активности, то она будет неизвестной
        type = ActivityTypes.Undefined.value
        for at in ActivityTypes:
            if a['class'][1].lower() == at.value.name.lower():
                type = at.value
        #Активность без контента - пропускается
        if type == ActivityTypes.Label.value: continue
        inst = a.find(class_='activityinstance')
        #Если не найдена ссылка на активность, то она None
        try:
            link = inst.find('a', class_='aalink').get('href')
        except Exception as e:
            log.info('Unable to get activity link: ' + str(e))
            link = None
            continue
        name = inst.find(class_='instancename').contents[0]
        if type == ActivityTypes.Undefined.value: log.warning(f'activity type is undefined: {a["class"][1]} | {course.name}, {name}, {link}')
        act = Activity(course=course, name=name, link=link, type=type)
        res.append(act)
    return res


async def parseFiles(session : ClientSession, activity : Activity) -> list[File]:
    log.info(f'Async parse: Files from {str(activity)}')
    AT = ActivityTypes
    if activity.link is None or len(activity.link) < 2 or\
        activity.type in [AT.Undefined.value, AT.Chat.value, AT.Forum.value, AT.Label.value, AT.Lession.value,
                            AT.Quiz.value, AT.Url.value, AT.Workshop.value]:
        log.warning('Attempt to get files for incorrect activity:' + activity.name)
        return []
    res = []
    if activity.type == AT.Assign.value:
        res.extend(await getFilesAssign(session, activity))
    elif activity.type == AT.Resource.value:
        res.extend(await getResource(session, activity))
    elif activity.type == AT.Folder.value:
        res.extend(await getFilesFolder(session, activity))
    
    return res

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
        rawName = link.split('/')[-1]
        rawName = unquote_plus(rawName, encoding='utf-8')
        name, rawExt = path.splitext(rawName)
        file = File(name=activity.name, link=link, activity=activity, extension=FileExtensions.Get(rawExt))
        log.info(f'Parsed file: {str(file)}')
        return [file]
    except Exception as e:
        log.error(f'Can\'t resource parse file for activity: {str(activity)}\n {str(e)}')
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
