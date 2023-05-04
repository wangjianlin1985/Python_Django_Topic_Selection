from django.db import models


class SubjectType(models.Model):
    subjectTypeId = models.AutoField(primary_key=True, verbose_name='类型编号')
    subjectTypeName = models.CharField(max_length=20, default='', verbose_name='类型名称')
    subjectTypeDesc = models.CharField(max_length=500, default='', verbose_name='类型说明')

    class Meta:
        db_table = 't_SubjectType'
        verbose_name = '题目类型信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        subjectType = {
            'subjectTypeId': self.subjectTypeId,
            'subjectTypeName': self.subjectTypeName,
            'subjectTypeDesc': self.subjectTypeDesc,
        }
        return subjectType

