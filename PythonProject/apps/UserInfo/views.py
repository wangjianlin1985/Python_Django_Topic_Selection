from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.UserInfo.models import UserInfo
from apps.ClassInfo.models import ClassInfo
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台学生信息添加
    def primaryKeyExist(self, user_name):  # 判断主键是否存在
        try:
            UserInfo.objects.get(user_name=user_name)
            return True
        except UserInfo.DoesNotExist:
            return False

    def get(self,request):
        classInfos = ClassInfo.objects.all()  # 获取所有班级信息
        context = {
            'classInfos': classInfos,
        }

        # 使用模板
        return render(request, 'UserInfo/userInfo_frontAdd.html', context)

    def post(self, request):
        user_name = request.POST.get('userInfo.user_name') # 判断学号是否存在
        if self.primaryKeyExist(user_name):
            return JsonResponse({'success': False, 'message': '学号已经存在'})

        userInfo = UserInfo() # 新建一个学生信息对象然后获取参数
        userInfo.user_name = user_name
        userInfo.password = request.POST.get('userInfo.password')
        userInfo.classObj = ClassInfo.objects.get(classNumber=request.POST.get('userInfo.classObj.classNumber'))
        userInfo.name = request.POST.get('userInfo.name')
        userInfo.sex = request.POST.get('userInfo.sex')
        userInfo.birthday = request.POST.get('userInfo.birthday')
        userInfo.zzmm = request.POST.get('userInfo.zzmm')
        userInfo.telephone = request.POST.get('userInfo.telephone')
        userInfo.address = request.POST.get('userInfo.address')
        try:
            userInfo.photo = self.uploadImageFile(request,'userInfo.photo')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        userInfo.save() # 保存学生信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改学生信息
    def get(self, request, user_name):
        context = {'user_name': user_name}
        return render(request, 'UserInfo/userInfo_frontModify.html', context)


class FrontListView(BaseView):  # 前台学生信息查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        user_name = self.getStrParam(request, 'user_name')
        classObj_classNumber = self.getStrParam(request, 'classObj.classNumber')
        name = self.getStrParam(request, 'name')
        birthday = self.getStrParam(request, 'birthday')
        zzmm = self.getStrParam(request, 'zzmm')
        # 然后条件组合查询过滤
        userInfos = UserInfo.objects.all()
        if user_name != '':
            userInfos = userInfos.filter(user_name__contains=user_name)
        if classObj_classNumber != '':
            userInfos = userInfos.filter(classObj=classObj_classNumber)
        if name != '':
            userInfos = userInfos.filter(name__contains=name)
        if birthday != '':
            userInfos = userInfos.filter(birthday__contains=birthday)
        if zzmm != '':
            userInfos = userInfos.filter(zzmm__contains=zzmm)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(userInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        userInfos_page = self.paginator.page(self.currentPage)

        # 获取所有班级信息
        classInfos = ClassInfo.objects.all()
        # 构造模板需要的参数
        context = {
            'classInfos': classInfos,
            'userInfos_page': userInfos_page,
            'user_name': user_name,
            'classObj_classNumber': classObj_classNumber,
            'name': name,
            'birthday': birthday,
            'zzmm': zzmm,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'UserInfo/userInfo_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示学生信息详情页
    def get(self, request, user_name):
        # 查询需要显示的学生信息对象
        userInfo = UserInfo.objects.get(user_name=user_name)
        context = {
            'userInfo': userInfo
        }
        # 渲染模板显示
        return render(request, 'UserInfo/userInfo_frontshow.html', context)


class ListAllView(View): # 前台查询所有学生信息
    def get(self,request):
        userInfos = UserInfo.objects.all()
        userInfoList = []
        for userInfo in userInfos:
            userInfoObj = {
                'user_name': userInfo.user_name,
                'name': userInfo.name,
            }
            userInfoList.append(userInfoObj)
        return JsonResponse(userInfoList, safe=False)


class UpdateView(BaseView):  # Ajax方式学生信息更新
    def get(self, request, user_name):
        # GET方式请求查询学生信息对象并返回学生信息json格式
        userInfo = UserInfo.objects.get(user_name=user_name)
        return JsonResponse(userInfo.getJsonObj())

    def post(self, request, user_name):
        # POST方式提交学生信息修改信息更新到数据库
        userInfo = UserInfo.objects.get(user_name=user_name)
        userInfo.password = request.POST.get('userInfo.password')
        userInfo.classObj = ClassInfo.objects.get(classNumber=request.POST.get('userInfo.classObj.classNumber'))
        userInfo.name = request.POST.get('userInfo.name')
        userInfo.sex = request.POST.get('userInfo.sex')
        userInfo.birthday = request.POST.get('userInfo.birthday')
        userInfo.zzmm = request.POST.get('userInfo.zzmm')
        userInfo.telephone = request.POST.get('userInfo.telephone')
        userInfo.address = request.POST.get('userInfo.address')
        try:
            photoName = self.uploadImageFile(request, 'userInfo.photo')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        if photoName != 'img/NoImage.jpg':
            userInfo.photo = photoName
        userInfo.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台学生信息添加
    def primaryKeyExist(self, user_name):  # 判断主键是否存在
        try:
            UserInfo.objects.get(user_name=user_name)
            return True
        except UserInfo.DoesNotExist:
            return False

    def get(self,request):
        classInfos = ClassInfo.objects.all()  # 获取所有班级信息
        context = {
            'classInfos': classInfos,
        }

        # 渲染显示模板界面
        return render(request, 'UserInfo/userInfo_add.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        user_name = request.POST.get('userInfo.user_name') # 判断学号是否存在
        if self.primaryKeyExist(user_name):
            return JsonResponse({'success': False, 'message': '学号已经存在'})

        userInfo = UserInfo() # 新建一个学生信息对象然后获取参数
        userInfo.user_name = user_name
        userInfo.password = request.POST.get('userInfo.password')
        userInfo.classObj = ClassInfo.objects.get(classNumber=request.POST.get('userInfo.classObj.classNumber'))
        userInfo.name = request.POST.get('userInfo.name')
        userInfo.sex = request.POST.get('userInfo.sex')
        userInfo.birthday = request.POST.get('userInfo.birthday')
        userInfo.zzmm = request.POST.get('userInfo.zzmm')
        userInfo.telephone = request.POST.get('userInfo.telephone')
        userInfo.address = request.POST.get('userInfo.address')
        try:
            userInfo.photo = self.uploadImageFile(request,'userInfo.photo')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        userInfo.save() # 保存学生信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新学生信息
    def get(self, request, user_name):
        context = {'user_name': user_name}
        return render(request, 'UserInfo/userInfo_modify.html', context)


class ListView(BaseView):  # 后台学生信息列表
    def get(self, request):
        # 使用模板
        return render(request, 'UserInfo/userInfo_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        user_name = self.getStrParam(request, 'user_name')
        classObj_classNumber = self.getStrParam(request, 'classObj.classNumber')
        name = self.getStrParam(request, 'name')
        birthday = self.getStrParam(request, 'birthday')
        zzmm = self.getStrParam(request, 'zzmm')
        # 然后条件组合查询过滤
        userInfos = UserInfo.objects.all()
        if user_name != '':
            userInfos = userInfos.filter(user_name__contains=user_name)
        if classObj_classNumber != '':
            userInfos = userInfos.filter(classObj=classObj_classNumber)
        if name != '':
            userInfos = userInfos.filter(name__contains=name)
        if birthday != '':
            userInfos = userInfos.filter(birthday__contains=birthday)
        if zzmm != '':
            userInfos = userInfos.filter(zzmm__contains=zzmm)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(userInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        userInfos_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        userInfoList = []
        for userInfo in userInfos_page:
            userInfo = userInfo.getJsonObj()
            userInfoList.append(userInfo)
        # 构造模板页面需要的参数
        userInfo_res = {
            'rows': userInfoList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(userInfo_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除学生信息信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        user_names = self.getStrParam(request, 'user_names')
        user_names = user_names.split(',')
        count = 0
        try:
            for user_name in user_names:
                UserInfo.objects.get(user_name=user_name).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出学生信息信息到excel并下载
    def get(self, request):
        # 收集查询参数
        user_name = self.getStrParam(request, 'user_name')
        classObj_classNumber = self.getStrParam(request, 'classObj.classNumber')
        name = self.getStrParam(request, 'name')
        birthday = self.getStrParam(request, 'birthday')
        zzmm = self.getStrParam(request, 'zzmm')
        # 然后条件组合查询过滤
        userInfos = UserInfo.objects.all()
        if user_name != '':
            userInfos = userInfos.filter(user_name__contains=user_name)
        if classObj_classNumber != '':
            userInfos = userInfos.filter(classObj=classObj_classNumber)
        if name != '':
            userInfos = userInfos.filter(name__contains=name)
        if birthday != '':
            userInfos = userInfos.filter(birthday__contains=birthday)
        if zzmm != '':
            userInfos = userInfos.filter(zzmm__contains=zzmm)
        #将查询结果集转换成列表
        userInfoList = []
        for userInfo in userInfos:
            userInfo = userInfo.getJsonObj()
            userInfoList.append(userInfo)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(userInfoList)
        # 设置要导入到excel的列
        columns_map = {
            'user_name': '学号',
            'classObj': '所在班级',
            'name': '姓名',
            'sex': '性别',
            'birthday': '出生日期',
            'zzmm': '政治面貌',
            'telephone': '联系电话',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'userInfos.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="userInfos.xlsx"'
        return response

