from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, Table, Column
from typing import List


"""
Подробнее о моделях можно также узнать в parse/parseFunction.py
"""

class Base(DeclarativeBase):
    """
    Базовый класс модели SQLAlchemy
    """
    ...

class BaseName(Base):
    """
    Базовый класс, у которого есть только название (вместо ID).
    Пример: `Extension` - у этого класса все имена уникальные и служат идентификатором.
    """
    __abstract__ = True

    name : Mapped[str] = mapped_column(String, primary_key=True)

    def __repr__(self) -> str:
        return f'<{self.__tablename__}: {self.name}>'

class BaseModel(Base):
    """
    Обычная модель с названием и ID.
    """
    __abstract__ = True

    id : Mapped[int] = mapped_column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f'<{self.__tablename__}: {self.name}#{self.id}>'

class BaseLinkModel(Base):
    """
    Модель, в которой вместо ID используется ссылка на объект.
    Данный подход можно использовать, так как у всех объектов уникальные ссылки.
    """
    __abstract__ = True

    link : Mapped[str] = mapped_column(String, primary_key=True)
    name : Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f'<{self.__tablename__}: {self.name} -- {self.link}>'



teacher_course = Table(
    'teacher_course',
    Base.metadata,
    Column('teacher', ForeignKey('teacher.link'), primary_key=True),
    Column('course', ForeignKey('course.link'), primary_key=True)
)

class Teacher(BaseLinkModel):
    __tablename__ = 'teacher'

    email :Mapped[str] = mapped_column(String, nullable=True, default=None)   
    courses : Mapped[List["Course"]] = relationship(secondary=teacher_course, back_populates='teachers')


class Course(BaseLinkModel):
    __tablename__ = 'course'

    activities : Mapped[List["Activity"]] = relationship(back_populates='course')
    teachers : Mapped[List["Teacher"]] = relationship(secondary=teacher_course, back_populates='courses')


class ActivityType(BaseName):
    __tablename__ = 'activityType'

    activities : Mapped[List["Activity"]] = relationship(back_populates='type')

class Activity(BaseLinkModel):
    __tablename__ = 'activity'

    description : Mapped[str] = mapped_column(String, nullable=True, default=None)
    typeName : Mapped[str] = mapped_column(ForeignKey("activityType.name"))
    type : Mapped["ActivityType"] = relationship(back_populates="activities")
    courseLink : Mapped[str] = mapped_column(ForeignKey('course.link'))
    course : Mapped["Course"] = relationship(back_populates='activities')
    files : Mapped[List["File"]] = relationship(back_populates='activity')



class FileType(BaseName):
    __tablename__ = 'fileType'

    fileExtensions : Mapped[List["FileExtension"]] = relationship(back_populates='fileType')

class FileExtension(BaseName):
    __tablename__ = 'fileExtension'

    fileTypeName : Mapped[str] = mapped_column(ForeignKey('fileType.name'))
    fileType : Mapped["FileType"] = relationship(back_populates='fileExtensions')
    files : Mapped[List["File"]] = relationship(back_populates='extension')

class File(BaseLinkModel):
    __tablename__ = 'file'

    path : Mapped[str] = mapped_column(String, nullable=True, default=None)
    download : Mapped[float] = mapped_column(Float, nullable=True, default=0.0)
    extensionName : Mapped[str] = mapped_column(ForeignKey("fileExtension.name"))
    extension : Mapped["FileExtension"] = relationship(back_populates='files')
    activityLink : Mapped[str] = mapped_column(ForeignKey('activity.link'))
    activity : Mapped["Activity"] = relationship(back_populates='files')




    




