
from rbac import models


def init_permission(request,user_obj):
    # 登录成功之后，将该用户所有的权限(url)全部注入到session中
    permission_list = models.Role.objects.filter(userinfo__username=user_obj.username) \
        .values('permissions__pk',
                'permissions__url',
                'permissions__title',
                'permissions__parent_id',
                'permissions__menus__pk',
                'permissions__menus__name',
                'permissions__menus__icon',
                'permissions__menus__weight',
                'permissions__url_name',).distinct()
    request.session['permission_list'] = list(permission_list)
    '''
        {
            # 1-- 一级菜单的id
            1:{
                'name':'业务系统',
                'icon':'fa fa-xx',
                'children':[
                    {'title':'客户管理','url':'/customer/list/',},
                ]
            },
            2:{
                'name':'财务系统',
                'icon':'fa fa-xx2',
                'weight':100,
                'children':[
                    {'title':'缴费展示','url':'/payment/list/',},
                ]
            }
        }

    '''
    # 权限精确到按钮级别
    url_names = []
    # 优化面包线/避免从数据库查数据
    permission_dict = {}
    # 筛选菜单
    menu_dict = {}
    for i in permission_list:
        # 将权限路径别名添加到一个列表中
        url_names.append(i.get('permissions__url_name'))
        # 输出规定格式的字典数据
        permission_dict[i.get('permissions__pk')] = i
        # 判断是不是菜单
        if i.get('permissions__menus__pk'):
            if i.get('permissions__menus__pk') in menu_dict:
                menu_dict[i.get('permissions__menus__pk')]['children'].append(
                    {'title': i.get('permissions__title'),
                     'url': i.get('permissions__url'),
                     'second_menu_id': i.get('permissions__pk'),
                     },)
            else:
                menu_dict[i.get('permissions__menus__pk')] = {
                    'name':i.get('permissions__menus__name'),
                    'icon':i.get('permissions__menus__icon'),
                    'weight':i.get('permissions__menus__weight'),
                    'children':[
                        {'title': i.get('permissions__title'),
                         'url': i.get('permissions__url'),
                         'second_menu_id': i.get('permissions__pk'),
                         },
                    ]
                }
    request.session['menu_dict'] = menu_dict
    request.session['permission_dict'] = permission_dict
    request.session['url_names'] = url_names


