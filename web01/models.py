from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserInfo(AbstractUser):
    """堡垒机账号"""
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to='avatars/', default="/avatars/default.png")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    mypage = models.OneToOneField(to='Mypage', to_field='nid', null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.username


class Host(models.Model):
    """存储主机列表"""
    host_name = models.CharField(max_length=64,unique=True)	# 主机名,不能重复
    in_ip = models.GenericIPAddressField(unique=True)		# 内IP
    out_ip = models.GenericIPAddressField(unique=False)		# 外IP
    port = models.SmallIntegerField(default=22)				# 端口
    host_user = models.CharField(max_length=32)				# 主机用户
    password = models.CharField(max_length=32,null=True)				# 密码
    key = models.CharField(max_length=128,null=False)		 			# 秘钥
    idc = models.ForeignKey("IDC")							# 机房
    Host_group = models.ForeignKey("Host_group",null=True)	# 主机组
    user = models.ForeignKey("UserInfo",null=True)			# 主机分配的堡垒机账户
    def __str__(self):
        return self.host_name	# 返回主机名



class Mypage(models.Model):
    """个人管理服务器的首页"""
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='个人首页', max_length=64)

    def __str__(self):
        return self.title


class Host_group(models.Model):
    nid = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=32)

    def __str__(self):
        return self.group_name

class IDC(models.Model):
    nid = models.AutoField(primary_key=True)
    idc = models.CharField(max_length=32)

    def __str__(self):
        return self.idc

class command_log(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey("UserInfo")
    host = models.ForeignKey("Host")
    command = models.CharField(max_length=32)


