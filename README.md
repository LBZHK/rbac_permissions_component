# rbac_permissions_component

### 1. rbac描述

1. 每个用户有不同的身份
2. 每种身份有对应不同的身份
3. 每种身份有不同的权限，根据不同身份设定不同的权限
4. 同时具有生成左侧菜单的功能



### 2. 表结构

1. 用户表

   ```python
   class UserInfo(models.Model):
       """ 用户表 """
       username = models.CharField(max_length=32)
       password = models.CharField(max_length=32)
       roles = models.ManyToManyField('Role')
       def __str__(self):
           return self.username
   ```

2. 角色表

   ```python
   class Role(models.Model):
       """ 角色表 """
       name = models.CharField(max_length=16)
       permissions = models.ManyToManyField('Permission')
   
       def __str__(self):
           return self.name
   ```

3. 权限

   ```python
   class Permission(models.Model):
       """ 权限表 """
       title = models.CharField(max_length=32)
       url = models.CharField(max_length=32)
       menus = models.ForeignKey('Menu', null=True, blank=True)
       parent = models.ForeignKey('self', null=True, blank=True)
       url_name = models.CharField(max_length=32, null=True, blank=True)
   
       def __str__(self):
           return self.title
   ```

4. 一级菜单表

   ```python
   class Menu(models.Model):
       """ 一级菜单表 """
       name = models.CharField(max_length=32)
       weight = models.IntegerField(default=100)
       icon = models.CharField(max_length=32, null=True, blank=True)
   
       def __str__(self):
           return self.name
   ```

   

### 总结

- 可以灵活的嵌套进一些需要权限的项目