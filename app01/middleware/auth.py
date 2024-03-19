""" 中间件验证是否需要登录 """

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 情况一：不需登录就能直接通过
        if request.path_info in ["/login/", "/image/code/"]:
            return
        # 情况二：已登陆过了可以允许通过
        info_dict = request.session.get("info")
        if info_dict:
            return
        # 情况三：没有登录过，重新回到登录页面
        return redirect('/login/')
