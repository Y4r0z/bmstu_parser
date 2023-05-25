from parse.tasks.tasks import Task, AllCoursesTask, ActivityTask, FileTask, CourseTask
from parse.parseWorker import ParseWorker
from db.models import Course, Activity
from bs4 import Tag
from asyncio import AbstractEventLoop
import asyncio
from config import Config

class TaskManger:
    """
    Класс для управления задачами. Он нужен для:
    * Распределения `задач (Task)` между `воркерами (Worker)`
    * Поддержания работы программы и автоматического её завершения при окончании парсинга
    """
    def __init__(self, loop : AbstractEventLoop, workersCount : int) -> None:
        self.loop = loop
        self.workersCount = workersCount
        self.workers : list[ParseWorker]  = []
        self.tasks : list[Task] = []
        tasks = [self._addWorker() for _ in range(self.workersCount)]
        self.loop.run_until_complete(asyncio.gather(*tasks)) 
        self._forceStop = False
    
    async def start(self, recursive = True):
        n = 0
        while len(self.tasks) != 0 and not self._forceStop:
            for task in self.tasks:
                for worker in self.workers:
                    if task.started == False and worker.busy == False:
                        if Config.MaximumTasks and task.id > Config.MaximumTasks:
                            self._forceStop = True
                        task.started = True
                        worker.busy = True
                        print(f'Exec task: {task.id} by worker {worker.id}. n: {n}. Type: {task.__class__.__name__}')
                        self.loop.create_task(task.exec(worker, recursive=recursive))
                        n = 0
            await asyncio.sleep(0.01)
            n+=1
        ('Collecting all tasks')
        while len(asyncio.all_tasks()) > 1:
            await asyncio.sleep(0.1)
        print('Stopped task manager')
        await self.close()


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

    async def close(self):
        self._forceStop = True
        for worker in self.workers:
            await worker.close()
        #self.loop.stop()
    
    async def _addWorker(self):
        self.workers.append(await ParseWorker.create())
    