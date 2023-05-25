import unittest

import asyncio
from parse.tasks.taskManager import TaskManger
from debug.timer import Timer
import logging as log
from dotenv import load_dotenv, find_dotenv
from debug.timer import Timer

class TestLoading(unittest.TestCase):
    def test_one(self):
        t = Timer("Test Load One")
        log.debug("test_1: start")
        self.loop = asyncio.get_event_loop()
        self.tm = TaskManger(self.loop, 1)
        self.loop.create_task(self.tm.start())
        self.loop.run_forever()
        t.log()


    def test_four(self):
        t = Timer("Test Load Four")
        self.loop = asyncio.get_event_loop()
        self.tm = TaskManger(self.loop, 4)
        self.loop.create_task(self.tm.start())
        self.loop.run_forever()
        t.log()

class TestParse(unittest.TestCase):
    def test_courses(self):
        self.loop = asyncio.get_event_loop()
        self.tm = TaskManger(self.loop, 1)
        self.tm.parseAllCourses([])
        self.loop.create_task(self.tm.start())
        self.loop.run_forever()

    





if __name__ == '__main__':
    load_dotenv(find_dotenv())
    unittest.main()
