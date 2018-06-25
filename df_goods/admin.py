from django.contrib import admin
from .models import TypeInfo, GoodsInfo


class TypeAdmin(admin.ModelAdmin):
    list_display = ['ttitle', 'isDelete']


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['gtitle', 'gprice', 'gunit', 'gstock', 'isDelete']
    search_fields = ['gtitle']
    list_filter = ['gtype']


admin.site.register(TypeInfo, TypeAdmin)
admin.site.register(GoodsInfo, GoodsAdmin)