from django import forms
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse

from app01 import models
from utils.bootstrap import BootStrap


class UpModelForm(BootStrap, forms.ModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = "__all__"


def city_list(request):
    queryset = models.City.objects.all()
    form = UpModelForm()
    return render(request, 'city_list.html', {'queryset': queryset, 'form': form})


def city_add(request):
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # # （一）原始方式：  {'name': '武沛齐', 'age': 123, 'img': <InMemoryUploadedFile: 图片 1.png (image/png)>}
        # # 1.读取图片内容，写入到文件夹中并获取文件的路径。
        # image_object = form.cleaned_data.get("img")
        # media_path = os.path.join("media", image_object.name)
        # f = open(media_path, mode='wb')
        # for chunk in image_object.chunks():
        #     f.write(chunk)
        # f.close()
        # # 2.将图片文件路径写入到数据库
        # models.City.objects.create(
        #     name=form.cleaned_data['name'],
        #     count=form.cleaned_data['count'],
        #     img=media_path,
        # )

        # （二）高级方式：
        # 对于文件：自动保存在media目录下：city/文件名
        # 字段+文件名 写入到数据库；    list展示：src="/media/{{ obj.img }}"
        form.save()
        return redirect("/city/list/")
    return HttpResponse("出错了")


def city_delete(request):
    """ 删除    """
    delete_id = request.GET.get('delete_id')
    exists = models.City.objects.filter(id=delete_id).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在。"})
    models.City.objects.filter(id=delete_id).delete()
    return JsonResponse({"status": True})

