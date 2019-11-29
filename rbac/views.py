from django.shortcuts import render, redirect, HttpResponse
from rbac import models
from django import forms
from django.db.models import Q
from rbac.Icon_library import icon_list
from django.utils.safestring import mark_safe
# 批量操作
from django.forms import modelformset_factory, formset_factory
from rbac.utils.routes import get_all_url_dict
from rbac.forms import MultiPermissionForm

from rbac.models import Permission



# 角色表 -- modelform
class RoleModelForm(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = '__all__'
        exclude = ['permissions', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': '角色',
        }

# 菜单表 -- modelform
class MenuModelForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.RadioSelect(choices=[[i[0],mark_safe(i[1])] for i in icon_list]),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': '菜单',
            'icon': 'icon',
            'weight': '权重',
        }

# 权限表 -- modelform
class PermissionModelForm(forms.ModelForm):
    class Meta:
        model = models.Permission
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})

# 角色展示
def role_list(request):
    role_obj = models.Role.objects.all()
    return render(request, 'role_list.html', {'role_obj': role_obj})

# 角色添加和编辑
def role_add_edit(request,n=None):
    role_obj = models.Role.objects.filter(id=n).first()
    if request.method == 'GET':
        form_obj = RoleModelForm(instance=role_obj)
        return render(request, 'form.html', {'form_obj': form_obj})
    else:
        form_obj = RoleModelForm(request.POST, instance=role_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('rbac:role_list')
        else:
            return render(request, 'form.html', {'form_obj': form_obj})

# 角色删除
def role_del(request,n):
    models.Role.objects.filter(id=n).delete()
    return redirect('rbac:role_list')

# 菜单权限展示
def menu_list(request):
    menu_id = request.GET.get('mid')
    menu_obj = models.Menu.objects.all()
    # 判断有无点击左侧菜单选项
    if menu_id:
        permission_list=models.Permission.objects.filter(Q(menus__id=menu_id)|Q(parent__menus__id=menu_id)).values('id', 'title', 'url', 'menus__id', 'url_name', 'parent_id', 'menus__icon', 'menus__name')
    else:
        permission_list = models.Permission.objects.all().values('id', 'title', 'url', 'menus__id', 'url_name', 'parent_id', 'menus__icon', 'menus__name')

    # 组数据结构
    permission_dict = {}
    for permission in permission_list:
        pid = permission.get('menus__id')
        if pid:
            permission_dict[permission.get('id')] = permission
            permission_dict[permission.get('id')]['children'] = []
    for p in permission_list:
        parent_id = p.get('parent_id')
        if parent_id:
            permission_dict[parent_id]['children'].append(p)

    return render(request, 'menu_list.html', {'menu_obj': menu_obj,'permission_list': permission_dict.values(), 'menu_id': menu_id})

# 菜单添加和编辑
def menu_add_edit(request,n=None):
    role_obj = models.Menu.objects.filter(id=n).first()
    if request.method == 'GET':
        form_obj = MenuModelForm(instance=role_obj)
        return render(request, 'form.html', {'form_obj': form_obj})
    else:
        form_obj = MenuModelForm(request.POST, instance=role_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('rbac:menu_list')
        else:
            return render(request, 'form.html', {'form_obj': form_obj})

# 菜单删除
def menu_del(request,n):
    models.Menu.objects.filter(id=n).delete()
    return redirect('rbac:menu_list')

# 权限添加和编辑
def permission_add_edit(request,n=None):
    permission_obj = models.Permission.objects.filter(id=n).first()
    if request.method == 'GET':
        form_obj = PermissionModelForm(instance=permission_obj)
        return render(request, 'form.html', {'form_obj': form_obj})
    else:
        form_obj = PermissionModelForm(request.POST, instance=permission_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('rbac:menu_list')
        else:
            return render(request, 'form.html', {'form_obj': form_obj})

# 权限删除
def permission_del(request,n):
    models.Permission.objects.filter(id=n).delete()
    return redirect('rbac:menu_list')

# 批量操作
def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """
    post_type = request.GET.get('type')

    # 更新、编辑
    FormSet = modelformset_factory(models.Permission, MultiPermissionForm, extra=0)

    # 增加
    AddFormSet = formset_factory(MultiPermissionForm, extra=0)

    # 数据库所有URL
    permissions = models.Permission.objects.all()

    # 项目路由系统的所有URL
    router_dict = get_all_url_dict(ignore_namespace_list=['admin', ])

    # 数据库所有权限别名
    permissions_name_set = set([i.url_name for i in permissions])

    # 项目路由系统的所有权限别名
    router_name_set = set(router_dict.keys())

    # 新增的url别名信息
    add_name_set = router_name_set - permissions_name_set
    add_formset = AddFormSet(initial=[row for name,row in router_dict.items() if name in add_name_set])

    # 更新的url别名信息
    update_name_set = permissions_name_set & router_name_set
    update_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=update_name_set))

    # 删除的url别名信息
    del_name_set = permissions_name_set - router_name_set
    del_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=del_name_set))

    # 批量添加
    if request.method == 'POST' and post_type == 'add':
        add_formset = AddFormSet(request.POST)
        if add_formset.is_valid():
            permission_obj_list = [models.Permission(**i) for i in add_formset.cleaned_data]
            query_list = models.Permission.objects.bulk_create(permission_obj_list)
            for i in query_list:
                permissions_name_set.add(i.url_name)

    # 批量更新
    if request.method == 'POST' and post_type == 'update':
        update_formset = FormSet(request.POST)
        if update_formset.is_valid():
            update_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=update_name_set))

    return render(request,'multi_permissions.html',{
        'del_formset': del_formset,
        'update_formset': update_formset,
        'add_formset': add_formset,
    })

# 权限分配
def distribute_permissions(request):
    """
    权限分配
    :param request:
    :return:
    """
    uid = request.GET.get('uid')
    rid = request.GET.get('rid')

    if request.method == 'POST' and request.POST.get('postType') == 'role':
        user = models.UserInfo.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        user.roles.set(request.POST.getlist('roles'))

    if request.method == 'POST' and request.POST.get('postType') == 'permission' and rid:
        role = models.Role.objects.filter(id=rid).first()
        if not role:
            return HttpResponse('角色不存在')
        role.permissions.set(request.POST.getlist('permissions'))

    # 所有用户
    user_list = models.UserInfo.objects.all()
    # 用户对应的id和角色
    user_has_roles = models.UserInfo.objects.filter(id=uid).values('id', 'roles')

    user_has_roles_dict = {item['roles']: None for item in user_has_roles}

    """
    用户拥有的角色id
    user_has_roles_dict = { 角色id：None }
    """
    # 所有角色
    role_list = models.Role.objects.all()

    if rid:
        role_has_permissions = models.Role.objects.filter(id=rid).values('id', 'permissions')
    elif uid and not rid:
        user = models.UserInfo.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        role_has_permissions = user.roles.values('id', 'permissions')
    else:
        role_has_permissions = []

    role_has_permissions_dict = {item['permissions']: None for item in role_has_permissions}

    """
    角色拥有的权限id
    role_has_permissions_dict = { 权限id：None }
    """

    # 储存数据结构
    all_menu_list = [] # 最终要做的数据结构就存在这里面
    # 一级菜单数据
    queryset = models.Menu.objects.values('id', 'name')
    menu_dict = {}
    # queryset = [{'id':1,'name':'业务系统','children':[]},{'id':2,'name':'财务系统','children':[]}]

    '''
        menu_dict = {
            一级菜单id--1：{'id':1,'name':'业务系统','children':[
                {id:1,'title':'客户展示','menus_id':1,'children':[
                    {'id':1,'title':'添加客户','parent_id':1},
                    {'id':2,'title':'编辑客户','parent_id':1},
                ]},
                {id:2,'title':'缴费展示','menus_id':2,'children':[]},

            ]}，
            一级菜单id--2：{'id':2,'name':'财务系统','children':[]}，
            没有分配菜单的权限--None：{'id': None, 'name': '其他', 'children': []}
        }
        all_menu_list = [
            {'id':1,'name':'业务系统','children':[
                {id:1,'title':'客户展示','menus_id':1,'children':[
                    {'id':1,'title':'添加客户','parent_id':1},
                    {'id':2,'title':'编辑客户','parent_id':1},
                ]},
                {id:2,'title':'缴费展示','menus_id':2,'children':[]},
            ]},
            {'id':2,'name':'财务系统','children':[]},
            {'id': None, 'name': '其他', 'children': []}
        ]
        '''

    for item in queryset:
        item['children'] = []  # 放二级菜单，父权限
        menu_dict[item['id']] = item
        all_menu_list.append(item)

    other = {'id': None, 'title': '其他', 'children': []}
    all_menu_list.append(other)
    menu_dict[None] = other

    # 二级菜单权限数据
    root_permission = models.Permission.objects.filter(menus__isnull=False).values('id', 'title', 'menus_id')
    root_permission_dict = {}
    # [{id:1,'title':'客户展示','menus_id':1,'children':[]},{id:1,'title':'缴费展示','menus_id':2,'children':[]}]

    """
    root_permission_dict = {
        二级菜单id--1：{id:1,'title':'客户展示','menus_id':1,'children':[
            {'id':1,'title':'添加客户','parent_id':1},
            {'id':2,'title':'编辑客户','parent_id':1},
        ]},
        二级菜单id--2：{id:2,'title':'缴费展示','menus_id':2,'children':[]},

    }
    """

    for per in root_permission:
        per['children'] = []  # 放子权限
        nid = per['id']  # 二级菜单id值
        menu_id = per['menus_id']  # 一级菜单id值
        root_permission_dict[nid] = per
        menu_dict[menu_id]['children'].append(per)

    # 二级菜单的子权限
    node_permission = models.Permission.objects.filter(menus__isnull=True).values('id', 'title', 'parent_id')
    # [{'id':1,'title':'添加客户','parent_id':1},{'id':2,'title':'编辑客户','parent_id':1},]

    for per in node_permission:
        pid = per['parent_id']  # pid -- 对应的二级菜单的id
        if not pid:
            menu_dict[None]['children'].append(per)
            continue
        root_permission_dict[pid]['children'].append(per)

    return render(
        request,
        'distribute_permissions.html',
        {
            'user_list': user_list,
            'role_list': role_list,
            'user_has_roles_dict': user_has_roles_dict,
            'role_has_permissions_dict': role_has_permissions_dict,
            'all_menu_list': all_menu_list,
            'uid': uid,
            'rid': rid
        }
    )