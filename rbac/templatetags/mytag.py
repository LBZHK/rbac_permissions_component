import re

from django import template
from collections import OrderedDict

register = template.Library()


'''
{
    1: {
        'name': '业务系统',
        'icon': 'fa fa-home fa-fw',
        'children': [{
            'title': '客户管理',
            'url': '/customer/list/'
        }],
        'class':''
    },
    2: {
        'name': '财务系统',
        'icon': 'fa fa-jpy fa-fw',
        'children': [{
            'title': '账单管理',
            'url': '/payment/list/'
            'class':'acitve'
        }, {
            'title': '纳税展示',
            'url': '/nashui/'
        }],
        'class':'hidden'
    }
}
'''
@register.inclusion_tag('menu.html')
def menu(request):
    menu_dict =  request.session.get('menu_dict')
    menu_order_key = sorted(menu_dict,key=lambda x:menu_dict[x]['weight'],reverse=True)
    menu_order_dict = OrderedDict()
    for key in menu_order_key:
        menu_order_dict[key] = menu_dict[key]
    path = request.path
    for k,v in menu_order_dict.items():
        v['class'] = 'hidden'
        for i in v['children']:
            # if re.match(i['url'],path):
            if request.pid == i['second_menu_id']:
                v['class'] = ''
                i['class'] = 'active'

    return {'menu_order_dict':menu_order_dict}

@register.inclusion_tag('breadcrumb.html')
def bread_crumb(request):
    bread_crumb = request.bread_crumb
    data = {'bread_crumb': bread_crumb}
    return data


from django.conf import settings


@register.filter
def has_permission(request, permission):
    # if permission in request.session.get(settings.PERMISSION_SESSION_KEY):
    if permission in request.session.get('url_name'):
        return True


@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()

    params._mutable = True
    params['rid'] = rid
    # params = {'uid': 1,'rid':'a=1'}
    return params.urlencode()



