from django.db import models
from apps.ClassInfo.models import ClassInfo


class Student(models.Model):
    studentNumber = models.CharField(max_length=20, default='', primary_key=True, verbose_name='学号')
    password = models.CharField(max_length=30, default='', verbose_name='登录密码')
    classObj = models.ForeignKey(ClassInfo,  db_column='classObj', on_delete=models.PROTECT, verbose_name='所在班级')
    name = models.CharField(max_length=12, default='', verbose_name='姓名')
    sex = models.CharField(max_length=4, default='', verbose_name='性别')
    birthday = models.CharField(max_length=20, default='', verbose_name='出生日期')
    zzmm = models.CharField(max_length=15, default='', verbose_name='政治面貌')
    telephone = models.CharField(max_length=20, default='', verbose_name='联系电话')
    address = models.CharField(max_length=80, default='', verbose_name='家庭地址')
    photo = models.ImageField(upload_to='img', max_length='100', verbose_name='个人照片')

    class Meta:
        db_table = 't_Student'
        verbose_name = '学生信息信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        student = {
            'studentNumber': self.studentNumber,
            'password': self.password,
            'classObj': self.classObj.className,
            'classObjPri': self.classObj.classNumber,
            'name': self.name,
            'sex': self.sex,
            'birthday': self.birthday,
            'zzmm': self.zzmm,
            'telephone': self.telephone,
            'address': self.address,
            'photo': self.photo.url,
        }
        return student

