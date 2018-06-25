from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator, EmptyPage


def index(request):
    type_list = TypeInfo.objects.all()
    type0 = type_list[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = type_list[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = type_list[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = type_list[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = type_list[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = type_list[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = type_list[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = type_list[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = type_list[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = type_list[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = type_list[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = type_list[5].goodsinfo_set.order_by('-gclick')[0:4]
    context = {'title': '首页',
               'type0': type0, 'type01': type01,
               'type1': type1, 'type11': type11,
               'type2': type2, 'type21': type21,
               'type3': type3, 'type31': type31,
               'type4': type4, 'type41': type41,
               'type5': type5, 'type51': type51,
               }
    return render(request, 'df_goods/index.html', context)


def list(request, tid, pindex, sort):
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    new = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':  # 默认按最新排序
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == '2':  # 按价格排序
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3':  # 按点击量排序
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    paginator = Paginator(goods_list, 5)
    page = paginator.page(int(pindex))
    context = {
        'title': typeinfo.ttitle,
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'new': new,
        'sort': sort,
        'pindex': pindex,
    }
    return render(request, 'df_goods/list.html', context)


def detail(request, gid):
    goods = GoodsInfo.objects.get(pk=int(gid))
    goods.gclick += 1
    goods.save()
    new = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'title': goods.gtitle,
        'goods': goods,
        'new': new,
        'gid': gid,
    }
    response = render(request, 'df_goods/detail.html', context)
    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id = '%d'%goods.id
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        if goods_ids1.count(goods_id) >= 1:
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0, goods_id)
        if len(goods_ids1) >= 6:
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)
    else:
        goods_ids = goods_id
    response.set_cookie('goods_ids', goods_ids)
    return response