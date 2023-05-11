import unittest

import asyncio
from parse.tasks.taskManager import TaskManger
from debug.timer import Timer

class TestLoading(unittest.TestCase):
    def test_one(self):
        self.loop = asyncio.get_event_loop()
        self.tm = TaskManger(self.loop, 1)
        self.loop.create_task(self.tm.start())
        self.loop.run_forever()

    def test_four(self):
        self.loop = asyncio.get_event_loop()
        self.tm = TaskManger(self.loop, 4)
        self.loop.create_task(self.tm.start())
        self.loop.run_forever()

class TestParse(unittest.TestCase):
    def test_courses(self):
        self.loop = asyncio.get_event_loop()
        self.tm = TaskManger(self.loop, 1)
        self.tm.parseAllCourses([])
        self.loop.create_task(self.tm.start())
        self.loop.run_forever()



if __name__ == '__main__':
    unittest.main()
