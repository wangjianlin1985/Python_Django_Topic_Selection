from django.db import models
from apps.SubjectType.models import SubjectType
from apps.Teacher.models import Teacher
from tinymce.models import HTMLField


class Subject(models.Model):
    subjectId = models.AutoField(primary_key=True, verbose_name='题目编号')
    subjectTypeObj = models.ForeignKey(SubjectType,  db_column='subjectTypeObj', on_delete=models.PROTECT, verbose_name='题目类型')
    subjectName = models.CharField(max_length=40, default='', verbose_name='题目名称')
    subjectPhoto = models.ImageField(upload_to='img', max_length='100', verbose_name='题目图片')
    content = HTMLField(max_length=5000, verbose_name='题目内容')
    subjectState = models.CharField(max_length=20, default='', verbose_name='题目状态')
    personNum = models.IntegerField(default=0,verbose_name='限选人数')
    teacherObj = models.ForeignKey(Teacher,  db_column='teacherObj', on_delete=models.PROTECT, verbose_name='发布老师')
    addTime = models.CharField(max_length=20, default='', verbose_name='发布时间')

    class Meta:
        db_table = 't_Subject'
        verbose_name = '题目信息信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        subject = {
            'subjectId': self.subjectId,
            'subjectTypeObj': self.subjectTypeObj.subjectTypeName,
            'subjectTypeObjPri': self.subjectTypeObj.subjectTypeId,
            'subjectName': self.subjectName,
            'subjectPhoto': self.subjectPhoto.url,
            'content': self.content,
            'subjectState': self.subjectState,
            'personNum': self.personNum,
            'teacherObj': self.teacherObj.name,
            'teacherObjPri': self.teacherObj.teacherNumber,
            'addTime': self.addTime,
        }
        return subject

