from enum import Enum
from db.models import FileType, ActivityType, FileExtension


class ActivityTypes(Enum):
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


class FileTypes(Enum):
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
        return [FileExtension(name=i, fileType=type) for i in names.split('.')]
class FileExtensions(Enum):
    @classmethod
    def Get(cls, name : str):
        for type in cls:
            ext : FileExtension
            for ext in type.value:
                if ext.name == name.lower() or ext.name == name.replace('.','').lower():
                    return ext
        return FileExtension(name='undefined', fileType=FileTypes.Undefiend.value)
    
    Word : list[FileExtension] = FEList('doc.dot.wbk.docx.docm.docb.wll.wwl', FileTypes.Word.value)
    Pdf : list[FileExtension] = FEList('pdf', FileTypes.Pdf.value)
    Excel : list[FileExtension] = FEList('xls.xlt.xlm.xlsx.xlsm.xltx.xltm.xlsb.xla.xlam.xll.xlw.csv', FileTypes.Excel.value)
    PowerPoint  : list[FileExtension] = FEList('ppt.pot.pps.ppa.ppam.pptx.pptm.potx.potm.ppam.ppsx.ppsm.sldx.sldm.pa', FileTypes.PowerPoint.value)
    Text : list[FileExtension] = FEList('txt.log', FileTypes.Text.value)
    Audio : list[FileExtension] = FEList('aif.cda.mid.midi.mp3.mpa.ogg.wav.wma.wpl', FileTypes.Audio.value)
    Archive : list[FileExtension] = FEList('7z.arj.deb.pkg.rar.epm.tar.gz.z.zip', FileTypes.Archive.value)
    Image : list[FileExtension] = FEList('bmp.gid.ico.jpeg.jpg.png.psd.sbg.tif.tiff.webp', FileTypes.Image.value)
    Video : list[FileExtension] = FEList('3g2.3gp.avi.flv.h264.m4v.mkv.mov.mp4.mpg.mpeg.rm.swf.vob.webm.wmv', FileTypes.Video.value)
    Database : list[FileExtension] = FEList('db.dbf.mdb.sql.fdb', FileTypes.Database.value)
    Exe : list[FileExtension] = FEList('exe.bat.apk.wsf.msi.com', FileTypes.Exe.value)
    Html : list[FileExtension] = FEList('html.htm', FileTypes.Html.value)
    Code : list[FileExtension] = FEList('c.h.cpp.hpp.py.cgi.pl.py.cs.php.swift.sh.json.xml.r.asm.pdb.src.css.js.cls.', FileTypes.Code.value)

    
