import logging as log
from db.database import DatabaseManager
from parse.parseWorker import ParseWorker
import asyncio
from parse.tasks.taskManager import TaskManger

import time




class WebParser:
    def __init__(self) -> None:
        self.db = DatabaseManager()

    def start(self):
        print('Start') 
        self.loop = asyncio.get_event_loop()

        print('Create TM')
        self.tm = TaskManger(self.loop, 4)

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




