import re

from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect,HttpResponse,render
from rbac import models

class Auth(MiddlewareMixin):

    def process_request(self,request):
        # 登录认证白名单
        white_list = [reverse('login'),]
        # 权限认证白名单
        permission_white_list = [reverse('index'), '/admin/*', '.*',] #/admin/login/?next=/admin/
        request.pid = None

        # 面包线
        bread_crumb = [
            {'url': reverse('index'),'title': '首页'},
        ]
        request.bread_crumb = bread_crumb

        # 登录认证
        path = request.path
        if path not in white_list:
            is_login = request.session.get('is_login')
            if not is_login:
                return redirect('login')
            # 权限认证
            # permission_list = request.session.get('permission_list')
            permission_dict = request.session.get('permission_dict')

            for white_path in permission_white_list:
                if re.match(white_path,path):
                    break
            else:
                for i in permission_dict.values():
                    reg = r"^%s$"%i['permissions__url']
                    if re.match(reg,path):
                        pid = i.get('permissions__parent_id')
                        if pid:# 如果是非一级、非二级菜单
                            request.pid = pid
                            # 面包线
                            # 方式一：数据库操作
                            # parent_permission = models.Permission.objects.get(pk=pid)
                            # request.bread_crumb.append(
                            #     {'url': parent_permission.url, 'title': parent_permission.title}
                            # )

                            # 方式二：调整数据结构
                            request.bread_crumb.append(
                                {'url': permission_dict[str(pid)]['permissions__url'], 'title': permission_dict[str(pid)]['permissions__title']}
                            )

                            request.bread_crumb.append(
                                {'url': i.get('permissions__url'), 'title': i.get('permissions__title')}
                            )

                        else:
                            request.pid = i.get('permissions__pk')
                            request.bread_crumb.append(
                                {'url': i.get('permissions__url'), 'title': i.get('permissions__title')}
                            )
                        break
                else:
                    return HttpResponse('您配吗？？！')









