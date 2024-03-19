# -*- coding:utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from utils.pagination import Pagination
from utils.bootstrap import BootStrap


class UserModelForm(BootStrap, forms.ModelForm):
    mobile = forms.CharField(
        label="手机号码",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式错误'), ],
    )

    class Meta:
        model = models.UserInfo
        fields = "__all__"


def user_list(request):
    """ 用户列表    """
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data
    queryset = models.UserInfo.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)
    form = UserModelForm()
    context = {
        "form": form,
        "search_data": search_data,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, 'user_list.html', context)


@csrf_exempt
def user_add(request):
    """ 用户添加    """
    form = UserModelForm(data=request.POST)
    # 验证输入的手机号是否已被占用
    txt_mobile = request.POST.get('mobile')
    exists = models.UserInfo.objects.filter(mobile=txt_mobile).exists()
    if exists:
        form.add_error('mobile', "手机号码已存在")
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def user_detail(request):
    """ 编辑功能前戏：获取详细信息   """
    edit_id = request.GET.get("edit_id")
    row_dict = models.UserInfo.objects.filter(id=edit_id).values("name", "gender", "create_date", "depart",
                                                                 "account", "mobile", "birth_date").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在。"})
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)


@csrf_exempt
def user_edit(request):
    """ 用户编辑    """
    edit_id = request.GET.get('edit_id')
    row_object = models.UserInfo.objects.filter(id=edit_id).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在，请刷新重试。"})
    form = UserModelForm(data=request.POST, instance=row_object)
    # 验证修改后的手机号是否已被他人占用
    txt_mobile = request.POST.get('mobile')
    exists = models.UserInfo.objects.exclude(id=edit_id).filter(mobile=txt_mobile).exists()
    if exists:
        form.add_error('mobile', "手机号码已存在")
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def user_delete(request):
    """ 用户删除    """
    delete_id = request.GET.get('delete_id')
    exists = models.UserInfo.objects.filter(id=delete_id).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在。"})
    models.UserInfo.objects.filter(id=delete_id).delete()
    return JsonResponse({"status": True})
