from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import *
from . import user_decorator
from hashlib import sha1
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from df_goods.models import *
from df_order.models import *


def index(request):
    return redirect('/')


def register(request):
    return render(request, 'df_user/register.html', {'title': '天天生鲜-注册'})


def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')
    count = UserInfo.objects.filter(uname=uname).count()
    # 判断两次密码
    if upwd != ucpwd:
        return redirect('/user/register/')
    elif count != 0:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd2 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd2
    user.uemail = uemail
    user.save()
    # 注册成功, 转到登录页面
    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '天天生鲜-登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    remember = post.get('remember', 0)
    users = UserInfo.objects.filter(uname=uname)
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        if s1.hexdigest() == users[0].upwd:
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)
            # if remember != 0:
            #     red.set_cookie('uname', uname)
            # else:
            #     red.set_cookie('uname','', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            if remember == 0:
                uname = ''
            context = {'title': '天天生鲜-登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname}
            return render(request, 'df_user/login.html', context)
    else:
        if remember == 0:
            uname = ''
        context = {'title': '天天生鲜-登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname}
        return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


@user_decorator.login
def user_center_info(request):
    id = request.session['user_id']
    user = UserInfo.objects.get(pk=id)
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    for goods_id in goods_ids1:
        if goods_id != '':
            goods_list.append(GoodsInfo.objects.get(pk=int(goods_id)))

    context = {'title': '天天生鲜-用户中心', 'user': user, 'goods_list': goods_list}
    return render(request, 'df_user/user_center_info.html', context)



@user_decorator.login
def user_center_order(request, pindex):
    id = request.session['user_id']
    user = UserInfo.objects.get(pk=id)
    orders = OrderInfo.objects.filter(user_id=id).order_by('oIsPay', '-oid')
    paginator = Paginator(orders, 2)
    page = paginator.page(int(pindex))
    context = {'title': '天天生鲜-用户中心', 'user': user, 'orders': orders, 'paginator': paginator, 'page': page}
    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
def user_center_site(request):
    id = request.session['user_id']
    user = UserInfo.objects.get(pk=id)
    if request.method == 'POST':
        post = request.POST
        addressee = post.get('addressee')
        uaddress = post.get('uaddress')
        postcode = post.get('postcode')
        uphone = post.get('phone')
        user.addressee = addressee
        user.uaddress = uaddress
        user.postcode = postcode
        user.uphone = uphone
        user.save()
    context = {'title': '天天生鲜-用户中心', 'user': user}
    return render(request, 'df_user/user_center_site.html', context)


