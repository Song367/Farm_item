from django.urls import path,include
from django.conf.urls import url
from . import views
urlpatterns=[
        url('add/', views.add),   #店铺添加商品
        url('account/(?P<shop_id>\d+)', views.account),  #结算页面
        url('fruit/', views.fruit),     #水果类
        url('productManage/', views.productManage),   #店铺的产品管理
        url('modify/(?P<modify_id>\d+)', views.modify),   #商品修改
        url('^order/', views.orderd),    #订单
        url('shop/(?P<shop_id>\d+)', views.shop),      #商品详情页
        url('shopCar/(?P<shop_id>\d+)', views.shopCar),        #购物车
        url('shopRegister/', views.shopRegister),        #店铺注册
        url('vegetable/', views.vegetable),       #蔬菜类
        url('^userHelp/',views.userhelp),           #客服、使用帮助、退货
        path('getStore/',views.getStroe),       #查看用户是否有注册过店铺
        path('Store_reg/',views.Store_reg),
        url('trans_shopCar/',views.tran_shopCar),
        url('del_shopCar/',views.del_shopCar),
        url('^trans_order/',views.tran_order),
        url('^del_order/',views.del_order),
]
