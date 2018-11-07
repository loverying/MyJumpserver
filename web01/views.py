from django.shortcuts import render, HttpResponse,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import json
# Create your views here.
from web01 import models

from django.contrib import auth


def login(request):
    back_msg = {'user': None, 'msg': None}
    if request.is_ajax():
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        code = request.POST.get('code')

        if code.upper() == request.session['code'].upper():
            user = auth.authenticate(request, username=name, password=pwd)
            if user:
                # return HttpResponse('ok')
                auth.login(request, user)  # 验证成功后，登录
                back_msg['user'] = name
                back_msg['msg'] = '登录成功'
                return JsonResponse(back_msg)
            else:
                back_msg['msg'] = '用户名或密码错误'
                return JsonResponse(back_msg)
        else:
            back_msg['msg'] = '验证码错误'
            return JsonResponse(back_msg)
    return render(request, 'login.html')


def get_random_color():
    '''生成随机颜色的图片'''
    import random
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # （红，绿。蓝）


def get_code(request):
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO  # 生成的验证码存放于内存
    import random
    img = Image.new("RGB", (270, 40), color=get_random_color())
    # (270, 40) 指定生成的图片的长度，高度
    draw = ImageDraw.Draw(img)
    # kumo.ttf 文字样式，网上下载ttf
    kumo_font = ImageFont.truetype("static/font-awesome/fonts/kumo.ttf", size=32)  # 引入字体
    valid_code_str = ""
    for i in range(5):
        random_num = str(random.randint(0, 9))  # 随机一个数字
        random_low_alpha = chr(random.randint(95, 122))  # 随机一个小写字母
        random_upper_alpha = chr(random.randint(65, 90))  # 随机一个大写字母
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])  # 从上面的3个选择一个出来
        draw.text((i * 50 + 20, 5), random_char, get_random_color(), font=kumo_font)  # (i * 50 + 20, 5) 写字母的时候便宜

        # 保存验证码字符串
        valid_code_str += random_char

    print("valid_code_str", valid_code_str)
    f = BytesIO()  # 生成一个对象，保存于内存
    img.save(f, "png")  # 验证码图片保存于内存
    data = f.getvalue()
    request.session['code'] = valid_code_str  # 验证码保存于session中
    return HttpResponse(data)


@login_required()
def index(request):
    host_list = models.Host.objects.all()
    return render(request, 'index.html',{"host_list":host_list})


def add_host(request):
    if request.method == "GET":
        idc_list = models.IDC.objects.all()
        host_group_list =  models.Host_group.objects.all()
        user_list = models.UserInfo.objects.all()
        return render(request, 'add_host2.html',{"idc_list":idc_list,"host_group_list":host_group_list,"user_list":user_list})
    elif request.method == "POST":
        host_name = request.POST.get('host_name')
        in_ip = request.POST.get('in_ip')
        print('来了')
        out_ip = request.POST.get('out_ip')
        print(out_ip)
        port = request.POST.get('port')
        host_user = request.POST.get('host_user')
        password = request.POST.get('password')
        idc = request.POST.get('idc')
        Host_group = request.POST.get('Host_group')     # TypeError: 'Host_Host_group_id' is an invalid keyword argument for this function
        user = request.POST.get('user')

        models.Host.objects.create(host_name=host_name,in_ip=in_ip,out_ip=out_ip,port=port,host_user=host_user,password=password,
                                   Host_group_id=Host_group,
                                   idc_id=idc,
                                   user_id=user)
        return redirect('/index/')

def add_idc(request):
    back_msg = {'user': None, 'msg': None}
    if request.is_ajax():
        idc = request.POST.get('idc')
        user = models.IDC.objects.filter(idc=idc).first()
        if user:
            back_msg['msg'] = '该机房已经存在'
            return JsonResponse(back_msg)
        else:
            models.IDC.objects.create(idc=idc)
            back_msg['user'] = idc
            return JsonResponse(back_msg)
    return render(request, 'add_idc.html')


def add_host_group(request):
    back_msg = {'user': None, 'msg': None}
    if request.is_ajax():
        group_name = request.POST.get('group_name')
        user = models.Host_group.objects.filter(group_name=group_name).first()
        print(user)
        if user:
            back_msg['msg'] = '该主机组已经存在'
            return JsonResponse(back_msg)
        else:
            models.Host_group.objects.create(group_name=group_name)
            back_msg['user'] = group_name
            return JsonResponse(back_msg)
    return render(request, 'add_host_group.html')



def host_group_list(request):
    host_group_list = models.Host_group.objects.all()
    return render(request, 'host_group_list.html', {"host_group_list": host_group_list})


def idc_list(request):
    idc_list = models.IDC.objects.all()
    return render(request, 'idc_list.html',{"idc_list":idc_list})

def user_list(request):
    user_list = models.UserInfo.objects.all()
    return render(request, 'user_list.html',{"user_list":user_list})


from django import forms
from django.forms import widgets


class RegForms(forms.Form):
    name = forms.CharField(max_length=20, min_length=2, label='用户名',
                           widget=widgets.TextInput(attrs={'class': 'form-control'}),
                           error_messages={'max_length': '太长了', 'min_length': '太短了'}
                           )
    pwd = forms.CharField(max_length=20, min_length=2, label='密码',
                          widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                          error_messages={'max_length': '太长了', 'min_length': '太短了'}
                          )
    re_pwd = forms.CharField(max_length=20, min_length=2, label='确认密码',
                             widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                             error_messages={'max_length': '太长了', 'min_length': '太短了'}
                             )
    email = forms.EmailField(label='邮箱',
                             widget=widgets.EmailInput(attrs={'class': 'form-control'}),
                             )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        user = models.UserInfo.objects.filter(username=name).first()
        if user:
            raise ValidationError('用户已经存在')
        else:
            return name

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd == re_pwd:
            return self.cleaned_data
        else:
            # __all__
            raise ValidationError('两次密码不一致')

def add_user(request):
    form_obj = RegForms()
    back_msg = {}
    if request.is_ajax():
        print("PK")
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        re_pwd = request.POST.get('re_pwd')
        email = request.POST.get('email')
        myfile = request.FILES.get('myfile')
        print(myfile)
        print(re_pwd)
        form_obj = RegForms(request.POST)
        if form_obj.is_valid():
            if myfile:
                user = models.UserInfo.objects.create_user(username=name, password=pwd, email=email, avatar=myfile)
            else:
                user = models.UserInfo.objects.create_user(username=name, password=pwd, email=email)
            back_msg['user'] = name
            back_msg['msg'] = '注册成功'
        else:
            back_msg['msg'] = form_obj.errors
            print(form_obj.errors)
            print(type(form_obj.errors))
        return JsonResponse(back_msg)
    return render(request, 'add_user.html', {'form_obj': form_obj})


def details(request,id):
    details_host = models.Host.objects.filter(id=id).first()
    idc_list = models.IDC.objects.all()
    host_group_list =  models.Host_group.objects.all()
    user_list = models.UserInfo.objects.all()

    return render(request,'edit_host.html',locals())

def del_host(request):
    ret = {'status': True}
    try:
        nid = request.GET.get('id')
        print(nid)
        models.Host.objects.filter(id=nid).delete()
    except Exception as e:
        print('aaa')
        ret['status'] = False
    return HttpResponse(json.dumps(ret))



