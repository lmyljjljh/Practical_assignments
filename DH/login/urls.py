from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('adlogin/', views.adlogin, name='adlogin'),
    path('ad/', views.ad, name='ad'),
    # path('chat_room/', views.chat_room, name='chat_room'),
    path('register/', views.register),
    path('yh/', views.yonghuguanli),
    path('add/', views.add, name='add'),
    path('drop/', views.drop, name='drop'),
    path('zh/', views.zh, name='zh'),
    path('cz/', views.cz, name='cz'),
    path('jz/', views.jz, name='jz'),
    path('jcjz/', views.jcjz, name='jcjz'),
    path('hdwz/', views.huidawenzi, name='hdwz'),
    path('addhdwz/', views.addhdwz, name='addhdwz'),
    path('delhdwz/', views.delhdwz, name='delhdwz'),
    path('huidaxg1/', views.huidaxg1, name='huidaxg1'),
    path('huidaxg/', views.huidaxg, name='huidaxg'),
    path('tj1/', views.tj1, name='tj1'),
    path('tj2/', views.tj2, name='tj2'),
    path('shlogin/', views.shjlogin, name='shlogin'),
    path('yzm/', views.Aliyun_register, name='yzm'),
    path('errof/', views.errof, name='errof'),
    path('sjlogin/', views.sjlogin, name='sjlogin'),

]
