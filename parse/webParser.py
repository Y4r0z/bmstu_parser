import logging as log
from db.database import DatabaseManager
from parse.parseWorker import ParseWorker
import asyncio
from parse.tasks.taskManager import TaskManger

import time




class WebParser:
    """
    Класс для демонстрации работы программы. Парсит всё содержимое сайта.
    
    В будущем этот класс будет убран, так как мне нужны лишь функции для парсинга отдельных объектов на сайте.
    """
    def __init__(self) -> None:
        self.db = DatabaseManager()

    def start(self):
        print('Start') 
        self.loop = asyncio.get_event_loop()

        print('Create TM')
        self.tm = TaskManger(self.loop, 4)
        """
        Заметка о быстродействии нескольких воркеров. Минимальное время работы - на 7 воркерах,
        на 8 уже начинается замедление.
        С увеличением кол-ва воркеров до 7, увеличение быстродействия становится все менее заметным.
        Но это также зависит от скорости интернета.
        """
        timer = time.time()
        tt = lambda: time.time() - timer
        courses = []

        print(f'1st: {tt()}')
        
        print('Parse All Courses')
        self.tm.parseAllCourses(courses)
        print('Start TM')
        self.loop.run_until_complete(self.tm.start())

        print(f'2nd: {tt()}')
        
        try:
            self.db.addCourses(courses)
        except Exception as e:
            print(e)
        print('Stop', tt())




