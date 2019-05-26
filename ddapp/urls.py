from django.urls import path,include
from ddapp import views
urlpatterns = [
    path('index/',views.index,name='index'),
    path('detail/',views.detail,name='detail'),
    path('booklist/',views.booklist,name='booklist'),
    path('register/',views.register,name='register'),
    path('checkemail/',views.checkemail,name='checkemail'),
    path('checkname/',views.checkname,name='checkname'),
    path('checkpwd/',views.checkpwd,name='checkpwd'),
    path('getcaptcha/',views.getcaptcha,name='getcaptcha'),
    path('checknum/',views.checknum,name='checknum'),
    path('registerlogic/',views.registerlogic,name='registerlogic'),
    path('login/',views.login,name='login'),
    path('loginlogic/',views.loginlogic,name='loginlogic'),
    path('quit/',views.quit,name='quit'),
    path('add_cart/',views.add_cart,name='add_cart'),
    path('mycart/',views.mycart,name='mycart'),
    path('reduce/',views.reduce,name='reduce'),
    # path('registok/',views.registok,name='registok'),
    path('increase/',views.increase,name='increase'),
    path('delete1/',views.delete1,name='delete1'),
    path('indent/',views.indent,name='indent'),
    path('checkphone/',views.checkphone,name='checkphone'),
    path('indentok/',views.indentok,name='indentok'),
    path('checkreceiver/',views.checkreceiver,name='checkreceiver'),
    path('checkoption/',views.checkoption,name='checkoption'),
    path('iptchange/',views.iptchange,name='iptchange'),
    path('confirm1/',views.confirm1,name='confirm1'),
]