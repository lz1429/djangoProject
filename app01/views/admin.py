# -*- coding:utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from app01 import models
from utils.encrypt import md5
from utils.pagination import Pagination
from utils.bootstrap import BootStrap


class AdminAddModelForm(BootStrap, forms.ModelForm):
    """ 新增管理员的类 """
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", 'password', "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        return md5(self.cleaned_data.get("password"))

    def clean_confirm_password(self):
        md5_pwd = self.cleaned_data.get("password")
        md5_confirm = md5(self.cleaned_data.get("confirm_password"))
        if md5_confirm != md5_pwd:
            raise ValidationError("密码不一致")
        return md5_confirm


class AdminEditModelForm(BootStrap, forms.ModelForm):
    """ 编辑管理员账户名的类 """

    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetModelForm(BootStrap, forms.ModelForm):
    """ 重置管理员登录密码的类  """
    old_password = forms.CharField(
        label="原密码",
        widget=forms.PasswordInput(render_value=True)
    )
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['old_password', 'password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_old_password(self):
        md5_old_pwd = md5(self.cleaned_data.get("old_password"))
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_old_pwd).exists()
        if not exists:
            raise ValidationError("请输入原密码")
        return md5_old_pwd

    def clean_password(self):
        md5_pwd = md5(self.cleaned_data.get("password"))
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("请输入新密码")
        return md5_pwd

    def clean_confirm_password(self):
        md5_pwd = self.cleaned_data.get("password")
        md5_confirm = md5(self.cleaned_data.get("confirm_password"))
        if md5_confirm != md5_pwd:
            raise ValidationError("密码不一致")
        return md5_confirm


def admin_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data
    queryset = models.Admin.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)
    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, 'admin_list.html', context)


def admin_add(request):
    if request.method == "GET":
        form = AdminAddModelForm()
        return render(request, 'add_edit.html', {"form": form, "panel_title": "新增管理员"})
    form = AdminAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'add_edit.html', {"form": form, "panel_title": "新增管理员"})


def admin_edit(request):
    nid = request.GET.get('nid')
    row_object = models.Admin.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'add_edit.html', {"form": form, "panel_title": "编辑账号名"})
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'add_edit.html', {"form": form, "panel_title": "编辑账号名"})


def admin_reset(request):
    nid = request.GET.get('nid')
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')
    title = "重置密码 - {}".format(row_object.username)
    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, 'add_edit.html', {"form": form, "panel_title": title})
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'add_edit.html', {"form": form, "panel_title": title})


def admin_delete(request):
    """ 删除管理员   """
    nid = request.GET.get('nid')
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')
