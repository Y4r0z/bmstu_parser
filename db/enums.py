from db.models import FileType, ActivityType, FileExtension


"""
Весь данный файл занимают предпределенные типы моделей.
Парсер можер работать только с ними, и не создает новые.
"""


class PseudoEnum(type):
     target = type
     """
     Псевдо-`Enum` для того, чтобы было удобнее работать с содержимым классов.

     Полный функционл `Enum` тут не требуется.
     """
     def __iter__(cls): 
          return (i for i in cls.__dict__.values() if type(i) is cls.target)
     

class ActivityTypes(metaclass=PseudoEnum):
    """
    Типы активностей.
    
    Все объекты внутри курса считаются активностями, 
    если активность является одним файлом, 
    то в базе данных она будет представлена и файлом, и самой активностью.
    Активность может содержать в себе несколько файлов (Assign, Folder) 
    или не содержать их вовсе (Url, Chat).
    
    Названия активностей соотвутствуют названиям из HTML тегов сайта.
    """
    target = ActivityType

    Undefined = target(name='undefined')
    Resource = target(name='resource')
    Assign = target(name='assign')
    Chat = target(name='chat')
    Url = target(name='url')
    Folder = target(name='folder')
    Forum = target(name='forum')
    Quiz = target(name='quiz')
    Label = target(name='label')
    Page = target(name='page')
    Lession = target(name='lesson')
    Workshop = target(name='workshop')


class FileTypes(metaclass=PseudoEnum):
    """
    Типы файлов. Как правило, один тип файла открывает одна программа.
    """
    target = FileType

    Undefiend = target(name='undefiend')
    Word = target(name='word')
    Pdf = target(name='pdf')
    Excel = target(name='excel')
    Text = target(name='text')
    Audio = target(name='audio')
    Archive = target(name='archive')
    Image = target(name='image')
    Video = target(name='video')
    Database = target(name='database')
    Exe = target(name='exe')
    Html = target(name='html')
    PowerPoint = target(name='powerPoint')
    Code = target(name='code')


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

class FileExtensions(metaclass=PseudoEnum):
    """
    Расширения файлов. У одного типа файла может быть множество расширений.

    Одному типу файла соответствует множество расширений.

    Данный класс создан, чтобы правильно присваивать типы файлам по их расширениям.

    """

    target = list[FileExtension]

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
        for type in cls:
             for ext in type:
                if ext.name == name.lower() or ext.name == name.replace('.','').lower():
                    return ext
        return FileExtension(name='undefined', fileType=FileTypes.Undefiend)  
    
    Word : target = FEList('doc.dot.wbk.docx.docm.docb.wll.wwl.odt', FileTypes.Word)
    Pdf : target = FEList('pdf', FileTypes.Pdf)
    Excel : target = FEList('xls.xlt.xlm.xlsx.xlsm.xltx.xltm.xlsb.xla.xlam.xll.xlw.csv', FileTypes.Excel)
    PowerPoint  : target = FEList('ppt.pot.pps.ppa.ppam.pptx.pptm.potx.potm.ppam.ppsx.ppsm.sldx.sldm.pa', FileTypes.PowerPoint)
    Text : target = FEList('txt.log', FileTypes.Text)
    Audio : target = FEList('aif.cda.mid.midi.mp3.mpa.ogg.wav.wma.wpl', FileTypes.Audio)
    Archive : target = FEList('7z.arj.deb.pkg.rar.epm.tar.gz.z.zip', FileTypes.Archive)
    Image : target = FEList('bmp.gid.ico.jpeg.jpg.png.psd.sbg.tif.tiff.webp', FileTypes.Image)
    Video : target = FEList('3g2.3gp.avi.flv.h264.m4v.mkv.mov.mp4.mpg.mpeg.rm.swf.vob.webm.wmv', FileTypes.Video)
    Database : target = FEList('db.dbf.mdb.sql.fdb', FileTypes.Database)
    Exe : target = FEList('exe.bat.apk.wsf.msi.com', FileTypes.Exe)
    Html : target = FEList('html.htm', FileTypes.Html)
    Code : target = FEList('c.h.cpp.hpp.py.cgi.pl.py.cs.php.swift.sh.json.xml.r.asm.pdb.src.css.js.cls.', FileTypes.Code)

    
