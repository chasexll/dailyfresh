from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import transaction
from .models import *
from datetime import datetime
from decimal import Decimal
from df_user import user_decorator
from df_user.models import *
from df_cart.models import *


@user_decorator.login
def order(request):
    cart_ids = request.GET.getlist('cart_id')
    user_id = request.session['user_id']
    user = UserInfo.objects.get(pk=user_id)
    carts = []
    for cart_id in cart_ids:
        cart = CartInfo.objects.get(pk=int(cart_id))
        carts.append(cart)
    context = {'title': '订单页', 'carts': carts, 'user': user}
    return render(request, 'df_order/order.html', context)


@transaction.atomic()
@user_decorator.login
def order_handle(request):
    # 保存事物点
    tran_id = transaction.savepoint()
    # 接收购物车编号
    cart_list = request.POST.getlist('cart_ids[]')
    try:
        # 创建订单
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(request.POST.get('totalPay'))
        order.oaddress = request.POST.get('address')
        order.save()
        # 创建订单详情
        for cart_id in cart_list:
            detail = OrderDetailInfo()
            detail.order = order
            cart = CartInfo.objects.get(pk=int(cart_id))
            goods = cart.goods
            # 判断库存
            if goods.gstock >= cart.count:
                goods.gstock -= cart.count
                goods.save()
                # 保存订单详情
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                # 删除购物车数据
                cart.delete()
            else:
                # 库存不够
                transaction.savepoint_rollback(tran_id)
                return JsonResponse({'status': 0})
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print('==============%s'%(e))
        transaction.savepoint_rollback(tran_id)
    return JsonResponse({'status': 1})