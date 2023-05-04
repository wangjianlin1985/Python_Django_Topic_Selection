from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.Subject.models import Subject
from apps.SubjectType.models import SubjectType
from apps.Teacher.models import Teacher
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台题目信息添加
    def get(self,request):
        subjectTypes = SubjectType.objects.all()  # 获取所有题目类型
        teachers = Teacher.objects.all()  # 获取所有教师信息
        context = {
            'subjectTypes': subjectTypes,
            'teachers': teachers,
        }

        # 使用模板
        return render(request, 'Subject/subject_frontAdd.html', context)

    def post(self, request):
        subject = Subject() # 新建一个题目信息对象然后获取参数
        subject.subjectTypeObj = SubjectType.objects.get(subjectTypeId=request.POST.get('subject.subjectTypeObj.subjectTypeId'))
        subject.subjectName = request.POST.get('subject.subjectName')
        try:
            subject.subjectPhoto = self.uploadImageFile(request,'subject.subjectPhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        subject.content = request.POST.get('subject.content')
        subject.subjectState = request.POST.get('subject.subjectState')
        subject.personNum = int(request.POST.get('subject.personNum'))
        subject.teacherObj = Teacher.objects.get(teacherNumber=request.POST.get('subject.teacherObj.teacherNumber'))
        subject.addTime = request.POST.get('subject.addTime')
        subject.save() # 保存题目信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改题目信息
    def get(self, request, subjectId):
        context = {'subjectId': subjectId}
        return render(request, 'Subject/subject_frontModify.html', context)


class FrontListView(BaseView):  # 前台题目信息查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        subjectTypeObj_subjectTypeId = self.getIntParam(request, 'subjectTypeObj.subjectTypeId')
        subjectName = self.getStrParam(request, 'subjectName')
        subjectState = self.getStrParam(request, 'subjectState')
        teacherObj_teacherNumber = self.getStrParam(request, 'teacherObj.teacherNumber')
        addTime = self.getStrParam(request, 'addTime')
        # 然后条件组合查询过滤
        subjects = Subject.objects.all()
        if subjectTypeObj_subjectTypeId != '0':
            subjects = subjects.filter(subjectTypeObj=subjectTypeObj_subjectTypeId)
        if subjectName != '':
            subjects = subjects.filter(subjectName__contains=subjectName)
        if subjectState != '':
            subjects = subjects.filter(subjectState__contains=subjectState)
        if teacherObj_teacherNumber != '':
            subjects = subjects.filter(teacherObj=teacherObj_teacherNumber)
        if addTime != '':
            subjects = subjects.filter(addTime__contains=addTime)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(subjects, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        subjects_page = self.paginator.page(self.currentPage)

        # 获取所有题目类型
        subjectTypes = SubjectType.objects.all()
        # 获取所有教师信息
        teachers = Teacher.objects.all()
        # 构造模板需要的参数
        context = {
            'subjectTypes': subjectTypes,
            'teachers': teachers,
            'subjects_page': subjects_page,
            'subjectTypeObj_subjectTypeId': int(subjectTypeObj_subjectTypeId),
            'subjectName': subjectName,
            'subjectState': subjectState,
            'teacherObj_teacherNumber': teacherObj_teacherNumber,
            'addTime': addTime,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'Subject/subject_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示题目信息详情页
    def get(self, request, subjectId):
        # 查询需要显示的题目信息对象
        subject = Subject.objects.get(subjectId=subjectId)
        context = {
            'subject': subject
        }
        # 渲染模板显示
        return render(request, 'Subject/subject_frontshow.html', context)


class ListAllView(View): # 前台查询所有题目信息
    def get(self,request):
        subjects = Subject.objects.all()
        subjectList = []
        for subject in subjects:
            subjectObj = {
                'subjectId': subject.subjectId,
                'subjectName': subject.subjectName,
            }
            subjectList.append(subjectObj)
        return JsonResponse(subjectList, safe=False)


class UpdateView(BaseView):  # Ajax方式题目信息更新
    def get(self, request, subjectId):
        # GET方式请求查询题目信息对象并返回题目信息json格式
        subject = Subject.objects.get(subjectId=subjectId)
        return JsonResponse(subject.getJsonObj())

    def post(self, request, subjectId):
        # POST方式提交题目信息修改信息更新到数据库
        subject = Subject.objects.get(subjectId=subjectId)
        subject.subjectTypeObj = SubjectType.objects.get(subjectTypeId=request.POST.get('subject.subjectTypeObj.subjectTypeId'))
        subject.subjectName = request.POST.get('subject.subjectName')
        try:
            subjectPhotoName = self.uploadImageFile(request, 'subject.subjectPhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        if subjectPhotoName != 'img/NoImage.jpg':
            subject.subjectPhoto = subjectPhotoName
        subject.content = request.POST.get('subject.content')
        subject.subjectState = request.POST.get('subject.subjectState')
        subject.personNum = int(request.POST.get('subject.personNum'))
        subject.teacherObj = Teacher.objects.get(teacherNumber=request.POST.get('subject.teacherObj.teacherNumber'))
        subject.addTime = request.POST.get('subject.addTime')
        subject.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台题目信息添加
    def get(self,request):
        subjectTypes = SubjectType.objects.all()  # 获取所有题目类型
        teachers = Teacher.objects.all()  # 获取所有教师信息
        context = {
            'subjectTypes': subjectTypes,
            'teachers': teachers,
        }

        # 渲染显示模板界面
        return render(request, 'Subject/subject_add.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        subject = Subject() # 新建一个题目信息对象然后获取参数
        subject.subjectTypeObj = SubjectType.objects.get(subjectTypeId=request.POST.get('subject.subjectTypeObj.subjectTypeId'))
        subject.subjectName = request.POST.get('subject.subjectName')
        try:
            subject.subjectPhoto = self.uploadImageFile(request,'subject.subjectPhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        subject.content = request.POST.get('subject.content')
        subject.subjectState = request.POST.get('subject.subjectState')
        subject.personNum = int(request.POST.get('subject.personNum'))
        subject.teacherObj = Teacher.objects.get(teacherNumber=request.POST.get('subject.teacherObj.teacherNumber'))
        subject.addTime = request.POST.get('subject.addTime')
        subject.save() # 保存题目信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class TeacherAddView(BaseView):  # 后台题目信息添加
    def get(self,request):
        subjectTypes = SubjectType.objects.all()  # 获取所有题目类型
        teachers = Teacher.objects.all()  # 获取所有教师信息
        context = {
            'subjectTypes': subjectTypes,
            'teachers': teachers,
        }

        # 渲染显示模板界面
        return render(request, 'Subject/subject_teacherAdd.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        subject = Subject() # 新建一个题目信息对象然后获取参数
        subject.subjectTypeObj = SubjectType.objects.get(subjectTypeId=request.POST.get('subject.subjectTypeObj.subjectTypeId'))
        subject.subjectName = request.POST.get('subject.subjectName')
        try:
            subject.subjectPhoto = self.uploadImageFile(request,'subject.subjectPhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        subject.content = request.POST.get('subject.content')
        subject.subjectState = request.POST.get('subject.subjectState')
        subject.personNum = int(request.POST.get('subject.personNum'))
        subject.teacherObj = Teacher.objects.get(teacherNumber=request.session.get('teacherNumber'))
        import datetime
        subject.addTime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        subject.save() # 保存题目信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新题目信息
    def get(self, request, subjectId):
        context = {'subjectId': subjectId}
        return render(request, 'Subject/subject_modify.html', context)


class ListView(BaseView):  # 后台题目信息列表
    def get(self, request):
        # 使用模板
        return render(request, 'Subject/subject_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        subjectTypeObj_subjectTypeId = self.getIntParam(request, 'subjectTypeObj.subjectTypeId')
        subjectName = self.getStrParam(request, 'subjectName')
        subjectState = self.getStrParam(request, 'subjectState')
        teacherObj_teacherNumber = self.getStrParam(request, 'teacherObj.teacherNumber')
        addTime = self.getStrParam(request, 'addTime')
        # 然后条件组合查询过滤
        subjects = Subject.objects.all()
        if subjectTypeObj_subjectTypeId != '0':
            subjects = subjects.filter(subjectTypeObj=subjectTypeObj_subjectTypeId)
        if subjectName != '':
            subjects = subjects.filter(subjectName__contains=subjectName)
        if subjectState != '':
            subjects = subjects.filter(subjectState__contains=subjectState)
        if teacherObj_teacherNumber != '':
            subjects = subjects.filter(teacherObj=teacherObj_teacherNumber)
        if addTime != '':
            subjects = subjects.filter(addTime__contains=addTime)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(subjects, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        subjects_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        subjectList = []
        for subject in subjects_page:
            subject = subject.getJsonObj()
            subjectList.append(subject)
        # 构造模板页面需要的参数
        subject_res = {
            'rows': subjectList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(subject_res, json_dumps_params={'ensure_ascii':False})



class TeacherListView(BaseView):  # 后台题目信息列表
    def get(self, request):
        # 使用模板
        return render(request, 'Subject/subject_teacherQuery_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        subjectTypeObj_subjectTypeId = self.getIntParam(request, 'subjectTypeObj.subjectTypeId')
        subjectName = self.getStrParam(request, 'subjectName')
        subjectState = self.getStrParam(request, 'subjectState')
        teacherObj_teacherNumber =request.session.get('teacherNumber')
        addTime = self.getStrParam(request, 'addTime')
        # 然后条件组合查询过滤
        subjects = Subject.objects.all()
        if subjectTypeObj_subjectTypeId != '0':
            subjects = subjects.filter(subjectTypeObj=subjectTypeObj_subjectTypeId)
        if subjectName != '':
            subjects = subjects.filter(subjectName__contains=subjectName)
        if subjectState != '':
            subjects = subjects.filter(subjectState__contains=subjectState)
        if teacherObj_teacherNumber != '':
            subjects = subjects.filter(teacherObj=teacherObj_teacherNumber)
        if addTime != '':
            subjects = subjects.filter(addTime__contains=addTime)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(subjects, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        subjects_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        subjectList = []
        for subject in subjects_page:
            subject = subject.getJsonObj()
            subjectList.append(subject)
        # 构造模板页面需要的参数
        subject_res = {
            'rows': subjectList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(subject_res, json_dumps_params={'ensure_ascii':False})




class DeletesView(BaseView):  # 删除题目信息信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        subjectIds = self.getStrParam(request, 'subjectIds')
        subjectIds = subjectIds.split(',')
        count = 0
        try:
            for subjectId in subjectIds:
                Subject.objects.get(subjectId=subjectId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出题目信息信息到excel并下载
    def get(self, request):
        # 收集查询参数
        subjectTypeObj_subjectTypeId = self.getIntParam(request, 'subjectTypeObj.subjectTypeId')
        subjectName = self.getStrParam(request, 'subjectName')
        subjectState = self.getStrParam(request, 'subjectState')
        teacherObj_teacherNumber = self.getStrParam(request, 'teacherObj.teacherNumber')
        addTime = self.getStrParam(request, 'addTime')
        # 然后条件组合查询过滤
        subjects = Subject.objects.all()
        if subjectTypeObj_subjectTypeId != '0':
            subjects = subjects.filter(subjectTypeObj=subjectTypeObj_subjectTypeId)
        if subjectName != '':
            subjects = subjects.filter(subjectName__contains=subjectName)
        if subjectState != '':
            subjects = subjects.filter(subjectState__contains=subjectState)
        if teacherObj_teacherNumber != '':
            subjects = subjects.filter(teacherObj=teacherObj_teacherNumber)
        if addTime != '':
            subjects = subjects.filter(addTime__contains=addTime)
        #将查询结果集转换成列表
        subjectList = []
        for subject in subjects:
            subject = subject.getJsonObj()
            subjectList.append(subject)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(subjectList)
        # 设置要导入到excel的列
        columns_map = {
            'subjectId': '题目编号',
            'subjectTypeObj': '题目类型',
            'subjectName': '题目名称',
            'content': '题目内容',
            'subjectState': '题目状态',
            'personNum': '限选人数',
            'teacherObj': '发布老师',
            'addTime': '发布时间',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'subjects.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="subjects.xlsx"'
        return response

