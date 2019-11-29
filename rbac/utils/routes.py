from django.conf import settings
from django.utils.module_loading import import_string
from django.urls import RegexURLResolver, RegexURLPattern
from collections import OrderedDict


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    '''
    :param pre_namespace:  None  web
    :param pre_url:   '/'   '/^'
    :param urlpatterns:  []
    :param url_ordered_dict:  空的有序字典
    :return:
    '''
    for item in urlpatterns:
        if isinstance(item, RegexURLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace,)
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:  # 'web'
                    namespace = item.namespace  # namespace = 'web'

                else:
                    namespace = None
            # recursion_urls('web','/^',)
            recursion_urls(namespace, pre_url + item.regex.pattern, item.url_patterns, url_ordered_dict)

        else:
            if pre_namespace:  # 'web'
                name = "%s:%s" % (pre_namespace, item.name,)  # name='web:role_list'
            else:
                name = item.name  # 别名
            if not item.name:
                raise Exception('URL路由中必须设置name属性')

            url = pre_url + item._regex  # '/role/list/'
            url_ordered_dict[name] = {'url_name': name, 'url': url.replace('^', '').replace('$', '')}

        # url_ordered_dict['web:role_list'] = {'name': 'web:role_list', 'url': '/role/list/'}


def get_all_url_dict(ignore_namespace_list=None):
    """
    获取路由中
    :return:
    """
    ignore_list = ignore_namespace_list or []  # 短路
    url_ordered_dict = OrderedDict()  # 存放项目中所有的url

    md = import_string(settings.ROOT_URLCONF)

    # md = import_string('luffy_permission.urls')
    urlpatterns = []
    print(md.urlpatterns)

    '''
        [            
            <RegexURLResolver <module 'web.urls' from 'D:\\pro\\luffy_permission\\web\\urls.py'> (None:web) ^>, 
            <RegexURLResolver <module 'rbac.urls' from 'D:\\pro\\luffy_permission\\rbac\\urls.py'> (None:rbac) ^rbac/>, 
            <RegexURLPattern xx ^xx>
        ]
    '''
    for item in md.urlpatterns:
        if isinstance(item, RegexURLResolver) and item.namespace in ignore_list:
            continue
        urlpatterns.append(item)
    recursion_urls(None, "/", urlpatterns, url_ordered_dict)

    return url_ordered_dict







