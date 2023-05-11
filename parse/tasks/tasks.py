from parse.parseWorker import ParseWorker
from db.models import Course, Activity
from bs4 import Tag

class Task:
    """
    Задача для парсинга. 

    Задача может выполнится в обычном режиме или рекурсивном. Рекурсивный
    режим при выполнении задачи будет добавлять в список задач новые.

    На данный момент каждая задача автоматически добавляет себя в спискок задач. 
    Это временне решение, сделанне для того, чтобы программа выполнялась, пока
    новые задачи не перестанут поступать.

    В будущем все задачи будут независимы и не будут принимать `tasks` в
    конструкторе.
    """
    Count = 0
    def __init__(self, tasks : list) -> None:
        self.started = False
        self.tasks =  tasks
        self.id = self.Count
        tasks.append(self)
        Task.Count += 1
    
    def exec(self, worker : ParseWorker, recursive : bool = True):
        raise NotImplementedError('Exec method is not implemented!')

    def start(self):
        self.started = True
        self.tasks.remove(self)

    def end(self):
        ...
    

class AllCoursesTask(Task):
    def __init__(self, tasks : list, store : list[Course]) -> None:
        super().__init__(tasks)
        self.store = store
    async def exec(self, worker : ParseWorker, recursive : bool = True):
        self.start()
        courses = await worker.getAllCourses()
        if recursive:
            for i in courses:
                ActivityTask(self.tasks, i)
        self.store.extend(courses)
        self.end()

class CourseTask(Task):
    def __init__(self, tasks : list, coursebox : Tag) -> None:
        super().__init__(tasks)
        self.coursebox = coursebox
    async def exec(self, worker : ParseWorker, recursive : bool = True):
        self.start()
        course = await worker.getCourse(self.coursebox)
        if recursive: ActivityTask(self.tasks, course)
        self.end()

class ActivityTask(Task):
    def __init__(self, tasks : list, course : Course) -> None:
        super().__init__(tasks)
        self.course = course
    async def exec(self, worker : ParseWorker, recursive : bool = True):
        self.start()
        activities = await worker.getActivities(self.course)
        if recursive:
            for i in activities:
                FileTask(self.tasks, i)
        self.end()

class FileTask(Task):
    def __init__(self, tasks : list, activity : Activity) -> None:
        super().__init__(tasks)
        self.activity = activity
    async def exec(self, worker : ParseWorker):
        self.start()
        await worker.getFiles(self.activity)
        self.end()