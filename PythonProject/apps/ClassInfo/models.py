from django.db import models


class ClassInfo(models.Model):
    classNumber = models.CharField(max_length=20, default='', primary_key=True, verbose_name='班级编号')
    specialName = models.CharField(max_length=20, default='', verbose_name='所在专业')
    className = models.CharField(max_length=20, default='', verbose_name='班级名称')
    startDate = models.CharField(max_length=20, default='', verbose_name='成立日期')
    headTeacher = models.CharField(max_length=12, default='', verbose_name='班主任')

    class Meta:
        db_table = 't_ClassInfo'
        verbose_name = '班级信息信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        classInfo = {
            'classNumber': self.classNumber,
            'specialName': self.specialName,
            'className': self.className,
            'startDate': self.startDate,
            'headTeacher': self.headTeacher,
        }
        return classInfo

