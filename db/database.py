from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.models import Teacher, Course, Activity, Base, BaseLinkModel, BaseName
from typing import List
from config import Config

class DatabaseManager:
    """
    Класс, управляющей базой данных. Содержит не так много функций, так как
    её обновление происходит путем объединения курсов, которые содержат всю информацю 
    в иерархическом виде.
    """
    def __init__(self) -> None:
        self.engine = create_engine('sqlite:///' + Config.Path.Database, echo=False)
        Base.metadata.create_all(self.engine)

    def _addSingle(self, o):
        with Session(self.engine) as s:
            s.add(o)
            s.commit()

    def addTeachers(self, lst : List[Teacher]):
        if len(lst) == 0:
            return
        with Session(self.engine) as s:
            for t in lst:
                if s.query(Teacher).filter(Teacher.link == t.link).first() is None:
                    s.add(t)
            s.commit()
    
    def addCourses(self, lst : List[Course]):
        """
        Функция, которая добавляет курсы в базу данных или обновляет их.

        Других функций для работы с БД не требуется, так как курсы содержат
        в себе всю остальную инфрмацию.

        NOTE:
        Раньше курсы объединялись вручную, перечислением, но теперь 
        всю работу делает `merge()`.
        """
        if len(lst) == 0:
            return
        with Session(self.engine) as s:
            c : Course
            for c in lst:
                if c is None:
                    continue
                #q = s.query(Course).filter(Course.link == c.link).first()
                #c.id = None if q is None else q.id
                #course : Course = self._mergeModels(s, [c], Course)[0]
                #course.activities = self.mergeActivties(s, c.activities)
                #course.teachers = self._mergeModels(s, c.teachers, Teacher)
                s.merge(c)
            s.commit()

    def _mergeModels(self, session : Session, models : list[BaseLinkModel], modelType):
        newModels = []
        if models is None or len(models) == 0:
            return newModels
        m : BaseLinkModel
        for m in models:
            q = session.query(modelType).filter(modelType.link == m.link).first()
            newModels.append(m if q is None else q)
        return newModels
    
    def _mergeActivties(self, session : Session, activities : list[Activity]):
        newActivities = []
        if activities is None or len(activities) == 0:
            return newActivities
        a : Activity
        for a in activities:
            #a.type = session.merge(a.type)
            q = session.query(Activity).filter(Activity.link == a.link).first()
            cur = a if q is None else q
            #cur.files = self._mergeModels(session, a.files, File)
            #cur.files = session.merge(a.files)
            newActivities.append(cur)
        return newActivities
    
    def _mergeTypes(self, session : Session, type : BaseName, cls : BaseName):
        q = session.query(cls).filter(cls.name == type.name).first()
        return type if q is None else q
    

