from parse.tasks.tasks import Task, AllCoursesTask, ActivityTask, FileTask, CourseTask
from parse.parseWorker import ParseWorker
from db.models import Course, Activity, File
from bs4 import Tag
from asyncio import AbstractEventLoop
import asyncio

class TaskManger:
    def __init__(self, loop : AbstractEventLoop, workersCount : int) -> None:
        self.loop = loop
        self.workersCount = workersCount
        self.workers : list[ParseWorker]  = []
        self.tasks : list[Task] = []
        tasks = [self._addWorker() for _ in range(self.workersCount)]
        self.loop.run_until_complete(asyncio.gather(*tasks)) 
        self._forceStop = False
    
    async def start(self):
        n = 0
        while len(self.tasks) != 0 and not self._forceStop:
            for task in self.tasks:
                for worker in self.workers:
                    if task.started == False and worker.busy == False:
                        if task.id > 100 and False: return
                        task.started = True
                        worker.busy = True
                        print(f'Exec task: {task.id} by worker {worker.id}. n: {n}. Type: {task.__class__.__name__}')
                        self.loop.create_task(task.exec(worker))
                        n = 0
            await asyncio.sleep(0.1)
            n+=1

        print('Stopped task manager')
        self.close()


    def parseAllCourses(self, store : list[Course]):
        AllCoursesTask(self.tasks, store)

    def parseCourse(self, coursebox : Tag):
        CourseTask(self.tasks, coursebox)

    def parseActivity(self, course : Course):
        ActivityTask(self.tasks, course)
    
    def parseFile(self, activity : Activity):
        FileTask(self.tasks, activity)

    def busyWorkersCount(self):
        n = 0
        for i in self.workers:
            if i.busy:
                n+=1
        return n

    def isWorkersBusy(self):
        flag = 0
        for i in self.workers:
            if i.busy:
                flag += 1
        return flag == self.workersCount

    def close(self):
        self._forceStop = True
        self.loop.stop()

    def __del__(self):
        self.tasks.clear()
        self.workers.clear()
        self.close()
    
    async def _addWorker(self):
        self.workers.append(await ParseWorker.create())
    