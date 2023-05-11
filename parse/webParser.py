import logging as log
from db.database import DatabaseManager
import asyncio
from parse.tasks.taskManager import TaskManger

class WebParser:
    """
    Класс для демонстрации работы программы. Парсит всё содержимое сайта.
    
    В будущем этот класс будет убран, так как мне нужны лишь функции для парсинга отдельных объектов на сайте.
    """
    def __init__(self) -> None:
        self.db = DatabaseManager()

    def start(self):
        self.loop = asyncio.get_event_loop()
        self.tm = TaskManger(self.loop, 4)
        """
        Заметка о быстродействии нескольких воркеров. Минимальное время работы - на 7 воркерах,
        на 8 уже начинается замедление.
        С увеличением кол-ва воркеров до 7, увеличение быстродействия становится все менее заметным.
        Но это также зависит от скорости интернета.
        """
        courses = []
        self.tm.parseAllCourses(courses)
        self.loop.create_task(self.tm.start(recursive=False))
        self.loop.run_forever() 
        try:
            self.db.addCourses(courses)
        except Exception as e:
            print(e)




