from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.ClassInfo.models import ClassInfo
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台班级信息添加
    def primaryKeyExist(self, classNumber):  # 判断主键是否存在
        try:
            ClassInfo.objects.get(classNumber=classNumber)
            return True
        except ClassInfo.DoesNotExist:
            return False

    def get(self,request):

        # 使用模板
        return render(request, 'ClassInfo/classInfo_frontAdd.html')

    def post(self, request):
        classNumber = request.POST.get('classInfo.classNumber') # 判断班级编号是否存在
        if self.primaryKeyExist(classNumber):
            return JsonResponse({'success': False, 'message': '班级编号已经存在'})

        classInfo = ClassInfo() # 新建一个班级信息对象然后获取参数
        classInfo.classNumber = classNumber
        classInfo.specialName = request.POST.get('classInfo.specialName')
        classInfo.className = request.POST.get('classInfo.className')
        classInfo.startDate = request.POST.get('classInfo.startDate')
        classInfo.headTeacher = request.POST.get('classInfo.headTeacher')
        classInfo.save() # 保存班级信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改班级信息
    def get(self, request, classNumber):
        context = {'classNumber': classNumber}
        return render(request, 'ClassInfo/classInfo_frontModify.html', context)


class FrontListView(BaseView):  # 前台班级信息查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        classNumber = self.getStrParam(request, 'classNumber')
        specialName = self.getStrParam(request, 'specialName')
        className = self.getStrParam(request, 'className')
        startDate = self.getStrParam(request, 'startDate')
        # 然后条件组合查询过滤
        classInfos = ClassInfo.objects.all()
        if classNumber != '':
            classInfos = classInfos.filter(classNumber__contains=classNumber)
        if specialName != '':
            classInfos = classInfos.filter(specialName__contains=specialName)
        if className != '':
            classInfos = classInfos.filter(className__contains=className)
        if startDate != '':
            classInfos = classInfos.filter(startDate__contains=startDate)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(classInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        classInfos_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'classInfos_page': classInfos_page,
            'classNumber': classNumber,
            'specialName': specialName,
            'className': className,
            'startDate': startDate,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'ClassInfo/classInfo_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示班级信息详情页
    def get(self, request, classNumber):
        # 查询需要显示的班级信息对象
        classInfo = ClassInfo.objects.get(classNumber=classNumber)
        context = {
            'classInfo': classInfo
        }
        # 渲染模板显示
        return render(request, 'ClassInfo/classInfo_frontshow.html', context)


class ListAllView(View): # 前台查询所有班级信息
    def get(self,request):
        classInfos = ClassInfo.objects.all()
        classInfoList = []
        for classInfo in classInfos:
            classInfoObj = {
                'classNumber': classInfo.classNumber,
                'className': classInfo.className,
            }
            classInfoList.append(classInfoObj)
        return JsonResponse(classInfoList, safe=False)


class UpdateView(BaseView):  # Ajax方式班级信息更新
    def get(self, request, classNumber):
        # GET方式请求查询班级信息对象并返回班级信息json格式
        classInfo = ClassInfo.objects.get(classNumber=classNumber)
        return JsonResponse(classInfo.getJsonObj())

    def post(self, request, classNumber):
        # POST方式提交班级信息修改信息更新到数据库
        classInfo = ClassInfo.objects.get(classNumber=classNumber)
        classInfo.specialName = request.POST.get('classInfo.specialName')
        classInfo.className = request.POST.get('classInfo.className')
        classInfo.startDate = request.POST.get('classInfo.startDate')
        classInfo.headTeacher = request.POST.get('classInfo.headTeacher')
        classInfo.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台班级信息添加
    def primaryKeyExist(self, classNumber):  # 判断主键是否存在
        try:
            ClassInfo.objects.get(classNumber=classNumber)
            return True
        except ClassInfo.DoesNotExist:
            return False

    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'ClassInfo/classInfo_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        classNumber = request.POST.get('classInfo.classNumber') # 判断班级编号是否存在
        if self.primaryKeyExist(classNumber):
            return JsonResponse({'success': False, 'message': '班级编号已经存在'})

        classInfo = ClassInfo() # 新建一个班级信息对象然后获取参数
        classInfo.classNumber = classNumber
        classInfo.specialName = request.POST.get('classInfo.specialName')
        classInfo.className = request.POST.get('classInfo.className')
        classInfo.startDate = request.POST.get('classInfo.startDate')
        classInfo.headTeacher = request.POST.get('classInfo.headTeacher')
        classInfo.save() # 保存班级信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新班级信息
    def get(self, request, classNumber):
        context = {'classNumber': classNumber}
        return render(request, 'ClassInfo/classInfo_modify.html', context)


class ListView(BaseView):  # 后台班级信息列表
    def get(self, request):
        # 使用模板
        return render(request, 'ClassInfo/classInfo_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        classNumber = self.getStrParam(request, 'classNumber')
        specialName = self.getStrParam(request, 'specialName')
        className = self.getStrParam(request, 'className')
        startDate = self.getStrParam(request, 'startDate')
        # 然后条件组合查询过滤
        classInfos = ClassInfo.objects.all()
        if classNumber != '':
            classInfos = classInfos.filter(classNumber__contains=classNumber)
        if specialName != '':
            classInfos = classInfos.filter(specialName__contains=specialName)
        if className != '':
            classInfos = classInfos.filter(className__contains=className)
        if startDate != '':
            classInfos = classInfos.filter(startDate__contains=startDate)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(classInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        classInfos_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        classInfoList = []
        for classInfo in classInfos_page:
            classInfo = classInfo.getJsonObj()
            classInfoList.append(classInfo)
        # 构造模板页面需要的参数
        classInfo_res = {
            'rows': classInfoList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(classInfo_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除班级信息信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        classNumbers = self.getStrParam(request, 'classNumbers')
        classNumbers = classNumbers.split(',')
        count = 0
        try:
            for classNumber in classNumbers:
                ClassInfo.objects.get(classNumber=classNumber).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出班级信息信息到excel并下载
    def get(self, request):
        # 收集查询参数
        classNumber = self.getStrParam(request, 'classNumber')
        specialName = self.getStrParam(request, 'specialName')
        className = self.getStrParam(request, 'className')
        startDate = self.getStrParam(request, 'startDate')
        # 然后条件组合查询过滤
        classInfos = ClassInfo.objects.all()
        if classNumber != '':
            classInfos = classInfos.filter(classNumber__contains=classNumber)
        if specialName != '':
            classInfos = classInfos.filter(specialName__contains=specialName)
        if className != '':
            classInfos = classInfos.filter(className__contains=className)
        if startDate != '':
            classInfos = classInfos.filter(startDate__contains=startDate)
        #将查询结果集转换成列表
        classInfoList = []
        for classInfo in classInfos:
            classInfo = classInfo.getJsonObj()
            classInfoList.append(classInfo)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(classInfoList)
        # 设置要导入到excel的列
        columns_map = {
            'classNumber': '班级编号',
            'specialName': '所在专业',
            'className': '班级名称',
            'startDate': '成立日期',
            'headTeacher': '班主任',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'classInfos.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="classInfos.xlsx"'
        return response

