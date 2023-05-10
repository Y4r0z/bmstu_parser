from db.models import FileType, ActivityType, FileExtension


"""
Весь данный файл занимают предпределенные типы моделей.
Парсер можер работать только с ними, и не создает новые.
"""


class PseudoEnum:
     """
     Псевдо-`Enum` для того, чтобы было удобнее работать с содержимым классов.
     """
     def __iter__(self):
          return iter(self.__dict__.values())
     

class ActivityTypes(PseudoEnum):
    """
    Типы активностей. Все объекты внутри курса считаются активностями, 
    если активность является одним файлом, 
    то в базе данных она будет представлена и файлом, и самой активностью.
    Активность может содержать в себе несколько файлов (Assign, Folder) 
    или не содержать их вовсе (Url, Chat).
    
    Названия активностей соотвутствуют названиям из HTML тегов сайта.
    """
    Undefined = ActivityType(name='undefined')
    Resource = ActivityType(name='resource')
    Assign = ActivityType(name='assign')
    Chat = ActivityType(name='chat')
    Url = ActivityType(name='url')
    Folder = ActivityType(name='folder')
    Forum = ActivityType(name='forum')
    Quiz = ActivityType(name='quiz')
    Label = ActivityType(name='label')
    Page = ActivityType(name='page')
    Lession = ActivityType(name='lesson')
    Workshop = ActivityType(name='workshop')


class FileTypes(PseudoEnum):
    """
    Типы файлов. Как правило, один тип файла открывает одна программа.
    """
    Undefiend = FileType(name='undefiend')
    Word = FileType(name='word')
    Pdf = FileType(name='pdf')
    Excel = FileType(name='excel')
    Text = FileType(name='text')
    Audio = FileType(name='audio')
    Archive = FileType(name='archive')
    Image = FileType(name='image')
    Video = FileType(name='video')
    Database = FileType(name='database')
    Exe = FileType(name='exe')
    Html = FileType(name='html')
    PowerPoint = FileType(name='powerPoint')
    Code = FileType(name='code')


def FEList(names : str, type : FileType):
        """
        Функция пребразует строку с расширениями файлов в список с объектами типа Extension.
    
        Parameters
        -
        names : str
            Строка, в которой перечислекны расширения с точкой в качестве разделителя, пример: "pdf.doc.xls";
        type : FileType
            Тип файла, к которому будут принадлежать всек расширения

        Returns
        -
        list[FileExtension]
        """
        return [FileExtension(name=i, fileType=type) for i in names.split('.')]

class FileExtensions(PseudoEnum):
    """
    Расширения файлов. У одного типа файла может быть множество расширений.

    Одному типу файла соответствует множество расширений.

    Данный класс создан, чтобы правильно присваивать типы файлам по их расширениям.

    """

    @classmethod
    def Get(cls, name : str):
        """
        Возвращает объект класса `Extension` по его строковому названию.

        Parameters
        -
        name : str
            Название расшиения (можно с точкой), например .pdf или pdf.

        Returns
        -
        FileExtension
            Найденное расширение или расширение `undefined`.
        """
        type : list[FileExtension]
        for type in cls.__dict__.values():
             for ext in type:
                if ext.name == name.lower() or ext.name == name.replace('.','').lower():
                    return ext
        return FileExtension(name='undefined', fileType=FileTypes.Undefiend)  
    
    Word : list[FileExtension] = FEList('doc.dot.wbk.docx.docm.docb.wll.wwl.odt', FileTypes.Word)
    Pdf : list[FileExtension] = FEList('pdf', FileTypes.Pdf)
    Excel : list[FileExtension] = FEList('xls.xlt.xlm.xlsx.xlsm.xltx.xltm.xlsb.xla.xlam.xll.xlw.csv', FileTypes.Excel)
    PowerPoint  : list[FileExtension] = FEList('ppt.pot.pps.ppa.ppam.pptx.pptm.potx.potm.ppam.ppsx.ppsm.sldx.sldm.pa', FileTypes.PowerPoint)
    Text : list[FileExtension] = FEList('txt.log', FileTypes.Text)
    Audio : list[FileExtension] = FEList('aif.cda.mid.midi.mp3.mpa.ogg.wav.wma.wpl', FileTypes.Audio)
    Archive : list[FileExtension] = FEList('7z.arj.deb.pkg.rar.epm.tar.gz.z.zip', FileTypes.Archive)
    Image : list[FileExtension] = FEList('bmp.gid.ico.jpeg.jpg.png.psd.sbg.tif.tiff.webp', FileTypes.Image)
    Video : list[FileExtension] = FEList('3g2.3gp.avi.flv.h264.m4v.mkv.mov.mp4.mpg.mpeg.rm.swf.vob.webm.wmv', FileTypes.Video)
    Database : list[FileExtension] = FEList('db.dbf.mdb.sql.fdb', FileTypes.Database)
    Exe : list[FileExtension] = FEList('exe.bat.apk.wsf.msi.com', FileTypes.Exe)
    Html : list[FileExtension] = FEList('html.htm', FileTypes.Html)
    Code : list[FileExtension] = FEList('c.h.cpp.hpp.py.cgi.pl.py.cs.php.swift.sh.json.xml.r.asm.pdb.src.css.js.cls.', FileTypes.Code)

    
