from django.db import models

# Create your models here.
# 一级菜单表
class Menu(models.Model):
    name = models.CharField(max_length=32)
    weight = models.IntegerField(default=100)
    icon = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.name

# 权限
class Permission(models.Model):
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    menus = models.ForeignKey('Menu', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    url_name = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.title

# 用户表
class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role')
    def __str__(self):
        return self.username

# 角色表
class Role(models.Model):
    name = models.CharField(max_length=16)
    permissions = models.ManyToManyField('Permission')

    def __str__(self):
        return self.name






