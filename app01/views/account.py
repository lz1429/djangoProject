from io import BytesIO

from django import forms
from django.shortcuts import render, HttpResponse, redirect

from app01 import models
from utils.bootstrap import BootStrap
from utils.encrypt import md5
from utils.code import check_code


class LoginForm(BootStrap, forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """ 登录  """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证码校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})
        # 账号密码校验
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        # 登录成功; 相关信息写到浏览器的cookie中；写入到session中；
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        request.session.set_expiry(60 * 60 * 24 * 3)
        return redirect("/depart/list/")
    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 返回图片验证码 """
    img, code_string = check_code()
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)
    # 将图片保存到内存
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销  """
    request.session.clear()
    return redirect('/login/')
