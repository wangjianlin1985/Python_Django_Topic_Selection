from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.SubjectType.models import SubjectType
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台题目类型添加
    def get(self,request):

        # 使用模板
        return render(request, 'SubjectType/subjectType_frontAdd.html')

    def post(self, request):
        subjectType = SubjectType() # 新建一个题目类型对象然后获取参数
        subjectType.subjectTypeName = request.POST.get('subjectType.subjectTypeName')
        subjectType.subjectTypeDesc = request.POST.get('subjectType.subjectTypeDesc')
        subjectType.save() # 保存题目类型信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改题目类型
    def get(self, request, subjectTypeId):
        context = {'subjectTypeId': subjectTypeId}
        return render(request, 'SubjectType/subjectType_frontModify.html', context)


class FrontListView(BaseView):  # 前台题目类型查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        # 然后条件组合查询过滤
        subjectTypes = SubjectType.objects.all()
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(subjectTypes, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        subjectTypes_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'subjectTypes_page': subjectTypes_page,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'SubjectType/subjectType_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示题目类型详情页
    def get(self, request, subjectTypeId):
        # 查询需要显示的题目类型对象
        subjectType = SubjectType.objects.get(subjectTypeId=subjectTypeId)
        context = {
            'subjectType': subjectType
        }
        # 渲染模板显示
        return render(request, 'SubjectType/subjectType_frontshow.html', context)


class ListAllView(View): # 前台查询所有题目类型
    def get(self,request):
        subjectTypes = SubjectType.objects.all()
        subjectTypeList = []
        for subjectType in subjectTypes:
            subjectTypeObj = {
                'subjectTypeId': subjectType.subjectTypeId,
                'subjectTypeName': subjectType.subjectTypeName,
            }
            subjectTypeList.append(subjectTypeObj)
        return JsonResponse(subjectTypeList, safe=False)


class UpdateView(BaseView):  # Ajax方式题目类型更新
    def get(self, request, subjectTypeId):
        # GET方式请求查询题目类型对象并返回题目类型json格式
        subjectType = SubjectType.objects.get(subjectTypeId=subjectTypeId)
        return JsonResponse(subjectType.getJsonObj())

    def post(self, request, subjectTypeId):
        # POST方式提交题目类型修改信息更新到数据库
        subjectType = SubjectType.objects.get(subjectTypeId=subjectTypeId)
        subjectType.subjectTypeName = request.POST.get('subjectType.subjectTypeName')
        subjectType.subjectTypeDesc = request.POST.get('subjectType.subjectTypeDesc')
        subjectType.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台题目类型添加
    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'SubjectType/subjectType_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        subjectType = SubjectType() # 新建一个题目类型对象然后获取参数
        subjectType.subjectTypeName = request.POST.get('subjectType.subjectTypeName')
        subjectType.subjectTypeDesc = request.POST.get('subjectType.subjectTypeDesc')
        subjectType.save() # 保存题目类型信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新题目类型
    def get(self, request, subjectTypeId):
        context = {'subjectTypeId': subjectTypeId}
        return render(request, 'SubjectType/subjectType_modify.html', context)


class ListView(BaseView):  # 后台题目类型列表
    def get(self, request):
        # 使用模板
        return render(request, 'SubjectType/subjectType_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        # 然后条件组合查询过滤
        subjectTypes = SubjectType.objects.all()
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(subjectTypes, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        subjectTypes_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        subjectTypeList = []
        for subjectType in subjectTypes_page:
            subjectType = subjectType.getJsonObj()
            subjectTypeList.append(subjectType)
        # 构造模板页面需要的参数
        subjectType_res = {
            'rows': subjectTypeList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(subjectType_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除题目类型信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        subjectTypeIds = self.getStrParam(request, 'subjectTypeIds')
        subjectTypeIds = subjectTypeIds.split(',')
        count = 0
        try:
            for subjectTypeId in subjectTypeIds:
                SubjectType.objects.get(subjectTypeId=subjectTypeId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出题目类型信息到excel并下载
    def get(self, request):
        # 收集查询参数
        # 然后条件组合查询过滤
        subjectTypes = SubjectType.objects.all()
        #将查询结果集转换成列表
        subjectTypeList = []
        for subjectType in subjectTypes:
            subjectType = subjectType.getJsonObj()
            subjectTypeList.append(subjectType)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(subjectTypeList)
        # 设置要导入到excel的列
        columns_map = {
            'subjectTypeId': '类型编号',
            'subjectTypeName': '类型名称',
            'subjectTypeDesc': '类型说明',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'subjectTypes.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="subjectTypes.xlsx"'
        return response

