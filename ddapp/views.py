import datetime
import hashlib
import random
import string
import time
from uuid import UUID

from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from ddapp import models
from ddapp.captcha.image import ImageCaptcha
from ddapp.models import TCategory, TDetail, TUser, TAddress, TOrder, ConfirmString
from ddapp.car import Cartitem,Cart
# Create your views here.
def index(request):
    cateone = TCategory.objects.filter(parent_id__isnull=True)
    catetwo = TCategory.objects.filter(parent_id__isnull=False)
    online = TDetail.objects.order_by("-publish_time")[0:8]
    comment = TDetail.objects.order_by("-comment")[0:10]
    sales = TDetail.objects.order_by("-sales")[0:5]
    sore = TDetail.objects.order_by("-sore")[0:10]
    tuser=request.session.get("tuser")     #为什么在这里获取用户名就可以显示
    print(tuser,18)

    if tuser =="":
        print("我退出了")
        return render(request, 'ddapp/index.html', {"cateone": cateone, "catetwo": catetwo, "online": online,
                                                    "comment": comment, "sales": sales, "sore": sore})
    else:
        print("我怎么进来的")
        return render(request,'ddapp/index.html',{"cateone":cateone,"catetwo":catetwo,"online":online,
                                              "comment":comment,"sales":sales,"sore":sore,"tuser":tuser})




def quit(request):
    request.session["tuser"] = ""
    return redirect("index")





def detail(request):
    id = request.GET.get("id")
    detail = TDetail.objects.get(id=id)
    return render(request,'ddapp/Book details.html',{"detail":detail})


def booklist(request):
    cateone = TCategory.objects.filter(parent_id__isnull=True)
    catetwo = TCategory.objects.filter(parent_id__isnull=False)
    first_cate = request.GET.get("first_cate")
    second_cate = request.GET.get("second_cate")
    num = request.GET.get("num")
    if not num:
        # first_cate = request.GET.get("first_cate")
        # second_cate = request.GET.get("second_cate")
        if second_cate is None:
             request.session["first_cate"] = first_cate
             l=[]
             if not num:
                 num = 1
             first1 = TCategory.objects.get(id = first_cate)
             first = TCategory.objects.filter(parent_id=first_cate) #我是要显示在前端的查到的第一类图书
             for i in first:
                 firstlist = TDetail.objects.filter(category_id=i.id)
                 for j in firstlist:
                    l.append(j)
             pagtor = Paginator(l, per_page=3)
             count = pagtor.num_pages        #这是要传给前端的总页数
             print(pagtor,38)
             page = pagtor.page(num)
             print(page,39)
             return render(request, 'ddapp/booklist.html', {"count":count,"first_cate":first_cate,"first1":first1,"list":l,"cateone":cateone,"catetwo":catetwo,"second_cate":second_cate,"page":page})
        else:
            print(45)
            request.session["second_cate"] = second_cate
            first2 = TCategory.objects.get(id=first_cate)
            second2 = TCategory.objects.get(id =second_cate )   #这是在分类里边点击二级分类时根据二级分类的id查到的分类项
            secondlist = TDetail.objects.filter(category_id=second_cate)
            if not num:
                num = 1
            pagtor = Paginator(secondlist, per_page=3)
            count = pagtor.num_pages      #这是要传给前端的总页数
            print(pagtor, 50)
            page = pagtor.page(num)
            print(page, 52)
            return render(request, 'ddapp/booklist.html',
                          {"count":count,"first2":first2,"first_cate":first_cate,"second2":second2,"secondlist": secondlist,  "cateone": cateone, "catetwo": catetwo,"page":page,
                           "second_cate": second_cate})
    else:
        print(num)
        first_cate = request.session.get("first_cate")
        print(first_cate)
        second_cate2 = request.session.get("second_cate")
        print(second_cate2)
        if second_cate2 is None:
            l = []
            first = TCategory.objects.filter(parent_id=first_cate)
            for i in first:
                firstlist = TDetail.objects.filter(category_id=i.id)
                for j in firstlist:
                    l.append(j)
            pagtor = Paginator(l, per_page=3)
            count = pagtor.num_pages             #这是要传给前端的总页数
            print(pagtor, 69)
            page = pagtor.page(num)
            print(page, 71)
            return render(request, 'ddapp/booklist.html',
                          {"count":count,"list": l, "cateone": cateone, "catetwo": catetwo, "second_cate": second_cate2, "page": page})
        else:
            request.session["second_cate"] = second_cate
            secondlist = TDetail.objects.filter(category_id=second_cate)
            if not num:
                num = 1
            pagtor = Paginator(secondlist, per_page=3)
            count = pagtor.num_pages             #这是要传给前端的总页数
            print(pagtor, 85)
            page = pagtor.page(num)
            print(page, 86)
            return render(request, 'ddapp/booklist.html',
                          {"count":count,"secondlist": secondlist,  "cateone": cateone, "catetwo": catetwo,"page":page,
                           "second_cate": second_cate})




def register(request):
    # flag = request.GET.get("flag")
    # if flag == "index":
    fromcart = request.GET.get("flag")
    print(fromcart, "我fromcart是有值的")
    request.session["fromcart"] = fromcart
    return render(request,"ddapp/register.html")







def checkemail(request):
    email = request.GET.get("email")
    print(email,33)
    print("email",114)
    e= TUser.objects.filter(email=email)
    if e:
        print("ok")
        return HttpResponse("ok")
    else:
        if email=="":
            print("null")
            return HttpResponse("null")
        else:
            print("no")
            return HttpResponse("no")





def checkname(request):
    name=request.GET.get("username")
    user = TUser.objects.filter(username=name)
    if user:
        print("ok")
        return HttpResponse( "ok")
    else:
        if name == "":
            print("null")
            return HttpResponse("null")
        else:
            print("no",140)
            return HttpResponse("no")

def checkphone(request):
    phone = request.GET.get("phone")
    if phone == "":
        return HttpResponse("null")
    else:
        return HttpResponse("no")




def checkpwd(request):
    pwd = request.GET.get('pwd')
    if pwd =="":
        print("null")
        return HttpResponse("no")
    else:
        print('ok',156)
        return HttpResponse("ok")


def getcaptcha(request):
    image = ImageCaptcha()
    code = random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits,5)
    random_code = "".join(code)
    print(random_code)
    request.session["code"] = random_code
    data = image.generate(random_code)
    return HttpResponse(data,"image/png")

def checknum(request):
    a=request.session.get("code")
    print(a)
    num = request.GET.get("num")
    print(num)
    if a.lower() == num.lower():
        return HttpResponse("ok")
    else:
        if num=="":
            print("null",178)
            return HttpResponse("null")
        else:
            print("no")
            return HttpResponse("no")



def registerlogic(request):
    try:
        with transaction.atomic():
            fromcart=request.session.get("fromcart")   #得到来自订单的标识
            loginfromindex = request.session.get("loginfromindex")       #这里的接收是必要的，因为为了判断是不是既有从首页的登录进去，又能接收到订单页进去的标识
            email = request.POST.get("email")
            username = request.POST.get("username")
            password = request.POST.get("password")
            code1 = request.POST.get("code")
            c = request.session.get("code")
            if c.lower() == code1.lower():
                tuser = TUser.objects.create(email=email,username=username,password=password)
                if tuser:
                    if fromcart=="cart" and loginfromindex=="":
                        # request.session["login"] = "ok"
                        guser = TUser.objects.get(email=email, username=username, password=password)  # 获取刚注册好的对象
                        email_main(guser)
                        print("我是要跳转到订单表的注册")
                        return HttpResponse("邮件发送成功")    #来自购物车注册的逻辑

                    elif loginfromindex=="index" and fromcart=="":   #来自首页的登录，再注册
                        request.session["tuser"] = tuser.username
                        print("我希望我可以收到验证码,我是先从首页的登录进去再进注册")
                        request.session["login"] = "ok"
                        guser = TUser.objects.get(email=email,username=username,password=password)   #获取刚注册好的对象
                        email_main(guser)
                        return HttpResponse("邮件发送成功")
                        # return redirect("login")
                        # return redirect("registok")
                    else:          #这是既有首页进的标识又有购物车的标识
                        request.session["tuser"] = tuser.username           #从首页的注册进来
                        print("这是既有没有从登录进的标识又没有购物车的标识")
                        request.session["login"] = "ok"
                        guser = TUser.objects.get(email=email, username=username, password=password)  # 获取刚注册好的对象
                        email_main(guser)
                        return  HttpResponse("邮件发送成功")

    except:
        return HttpResponse("注册失败")


def make_string(new_user):
    """
    用来给每一个用户生成一个唯一不可重的注册码
    :param new_user:当前用户
    :return:生成完成的验证码
    """
    print("我进了make函数")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    h = hashlib.md5()
    print("我进了make函数1")
    code = new_user.username + now
    h.update(code.encode())
    print("我进了make函数2")
    code2 =h.hexdigest()
    print("我进了make函数3")
    print(code2,'我是code2我生成了随机码')
    models.ConfirmString.objects.create(user=code2, u=new_user)
    print("我进了make函数4")
    return code2


def send_email(email, code):
    """
    用来真正发送邮件发方法
    :param email:用户的邮箱号
    :param code:唯一的注册码
    :return:
    """
    print("我进了send_email函数")
    subject, from_email, to = '欢迎注册当当网！', 'ai_zhanghuan@sina.com', email
    print("我进了send_email函数2")
    text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
    html_content = '<p>感谢注册！，<a href="http://{}/ddapp/confirm1/?email={}&code={}" target = blank >点击验证邮箱</a>，欢迎你来验证你的邮箱，验证结束你就可以登录了！ </p> '.format('127.0.0.1:8000', email, code)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def email_main(user):
    """
    views.registlogic函数的组件，负责验证邮箱的业务处理
    :param user: 新建的对象
    :return:  处理user的email，发送验证邮件，成功则返回True,否则返回False
    """
    print("我进了main函数")
    try:
        code = make_string(user)
        print(code,'我能进send函数')
        send_email(user.email, code)
    except:
        return False
    return True






def confirm1(request):
    """
    用来处理用户点击邮箱中的连接来验证邮箱是否可用的视图
    :param request:邮箱确认请求
    :return:确认成功后直接变成已登陆状态，并跳转登陆界面
    """
    print("我进了confirm函数")
    email = request.GET.get('email')
    code = request.GET.get('code')
    a = request.session.get("")#获取是否路过了
    print(a,"我路过了fromcart")
    try:
        user = TUser.objects.get(email=email)
        print("我进了confirm函数1")
    except: # 用户不存在
        return HttpResponse('链接已失效')
    # 判断请求的注册码是否与数据库中该用户保存的一致
    old_code = ConfirmString.objects.get(u=user)
    # old_code = ConfirmString.objects.all()
    # print( old_code,type( old_code))
    if code != old_code.user:
        return HttpResponse('链接已失效')
    # 将该用户的状态改为可用
    user.status = True
    user.save()
    print("我进了confirm函数2")
    # 删除注册码
    old_code.delete()
    print("我进了confirm函数3")
    # 直接登录，保存登录状态&用户名&用户id
    request.session['login_state'] = 'ok'
    request.session['login_user'] = email
    print("我进了confirm函数4")
    request.session['name'] = user.username
    if a:
        print("我来自购物车注册的验证将要去订单页")          # 3为什么是空的
        return redirect("indent")
    else:
        return render(request, 'ddapp/register ok.html', {'username': email,
                                                        'login_state': request.session.get('login_state'),
                                                        'login_user': request.session.get('login_user'),
                                                        "name":request.session.get('name')})







# def registok(request):
#     user= request.session.get("tuser")
#     return render(request,"ddapp/register ok.html" ,{"user":user})







def login(request):
    # email3 = request.COOKIES.get("email2")
    # pwd3 = request.COOKIES.get("pwd2")
    # result = TUser.objects.get(email=email3,password=pwd3)
    # if result:
    #     request.session["login"] = "ok"
    #     return redirect("index")
    index =request.GET.get("flag")
    request.session["loginfromindex"] = index
    # indent1=request.session.get("indent")
    if index:
        return render(request,"ddapp/login.html")
    else:
        return render(request,"ddapp/login.html")



def indent(request):
    fromcart=request.session.get("fromcart")
    login = request.session.get("login")   #获取登录状态来判断最终跳转到登陆页还是地址页
    user = request.session.get("user")     #获取在登录逻辑里查询到的用户对象
    shopping = request.session.get("shopping")    #购物车
    indent = request.GET.get("flag")      #a标签传来的标示
    request.session["indent"] =indent
    print(indent,"看一下indent到底有没有存进去")
    if login:                             #有登录状态
        if fromcart:
            print("我是从购物车注册的，既有标识，又有登录状态")
            return render(request, "ddapp/indent.html", {"shopping": shopping})
        else:
            tuser= request.session.get("tuser")
            print(tuser)
            address = TAddress.objects.filter(user_id=user.id)  # 查询地址
            print(address,"能查出该用户的address")
            return render(request,"ddapp/indent.html",{"shopping":shopping,"address":address,"name":user.username})
    else:
         # return render(request,"ddapp/login.html?falg="+indent)
         return redirect("login")







def indentok(request):
    try:
        with transaction.atomic():
            user = request.session.get("user")
            shopping = request.session.get("shopping")
            receiver = request.POST.get("receiver")
            address1 = request.POST.get("address1")
            iphone = request.POST.get("iphone")
            zipcode = request.POST.get("zipcode")
            ordernum = str(int(time.time()*1000))+str(int(time.clock()*1000000))
            ta = TAddress.objects.get(receiver=receiver, receive_address=address1, zip_code=zipcode, tel=iphone)  # 判断新旧地址
            if ta:
                return render(request, "ddapp/indent ok.html", {"shopping": shopping,"ordernum":ordernum,"user":user,"ta":ta})
            else:
                user = request.session.get("user")  # 看看user是什么类型
                print("我进了if")
                user.taddress_set.create(receiver=receiver, receive_address=address1, tel=iphone, zip_code=zipcode)  # 创建地址
                print("地址创建成功")
                taddress = TAddress.objects.get(receiver=receiver)
                print(taddress,"11")
                taddress.torder_set.create(all_price=shopping.total_price,order_number=ordernum)  # 创建订单
                print("12")
                return render(request, "ddapp/indent ok.html", {"shopping": shopping,"ordernum":ordernum})
    except:
        return HttpResponse("订单生成失败")




def checkoption(request):
    myoption = int(request.GET.get("myoption")) #从ajax获取到地址的id
    tadd = TAddress.objects.get(id=myoption)   #查这本书
    print("我进了option函数")
    return JsonResponse({"receiver":tadd.receiver,"readdress":tadd.receive_address,"zcode":tadd.zip_code,"tel":tadd.tel}, safe=True)




def checkreceiver(request):
    uname = request.GET.get("uname")
    if uname == "":
        print("我进了验证收货人")
        return HttpResponse("null")
    else:
        return HttpResponse("ok")



def loginlogic(request):
    shopping = request.session.get("shopping")
    indent1 = request.session.get("indent")
    email2 = request.POST.get("txtUsername")
    pwd2 = request.POST.get("txtPassword")
    user = TUser.objects.get(email=email2,password=pwd2)
    print(user.status,"看看用户的登录状态是不是True")
    request.session["user"] = user              #这是从购物车进登录页面提交后保存的用户对象
    print("我是卡在这了吗")
    request.session["tuser"] = user.username
    print("我是卡在这了吗11")
    if user.status:
        if indent1:                     #我要判断有这个标识证明路过了结算，然后跳转到订单页
            request.session["login"] = "ok"
            return redirect('indent')

        else:                                #否则就是从首页进来的
            request.session["login"] = "ok"
            print("我应该进主页的")
            res = redirect("index")
            res.set_cookie('email2', email2, max_age=7 * 24 * 60 * 60)
            res.set_cookie('pwd2', pwd2, max_age=7 * 24 * 3600)
            request.session["tuser"] = user.username
            request.session["user"] = user
            return res
    else:
        return HttpResponse("用户名或密码错误，请重新登录")





def add_cart(request):
    bookid = int(request.GET.get("bookid"))
    c= request.session.get("shopping")
    print(c,"我获取到session了终于")
    print(bookid)
    if c is None:
        cart = Cart()
        store = cart.add_book_toCart(bookid)
        print(store,"我是空的购物车")
        request.session["shopping"] = cart           #因为创建好了购物车，所以要把购物车存入session  for i in cart.cartitem: print(i.qamount)
        print(cart)
        return HttpResponse("ok") #响应到模板是把store响应到吗
    else:
        store = c.add_book_toCart(bookid)
        print(store, "我是已经存在的购物车了呢")
        request.session["shopping"] = c            #这里的session是存的c吗
        return HttpResponse("no")


def mycart(request):
    shopping = request.session.get("shopping")
    print(shopping.cartitem,"如果有我说明我的页面可以显示图书")
    return render(request,"ddapp/car.html",{"shopping":shopping})



def reduce(request):
    print("看看能不能进来reduce函数")
    shopping = request.session.get("shopping")
    print(shopping)
    bookid = int(request.GET.get("bookid"))
    print("id",bookid)
    amount = request.GET.get("val")
    print("数量",amount)
    a = shopping.sums()
    b=shopping.total_price
    print(b,"我希望sum有值,因为总价是购物车的属性")
    if bookid and amount:
        for i in shopping.cartitem:
            if i.book.id == bookid:
                i.amount -= 1
                if i.amount < 1:
                    amoun=1
                    print(amoun,"我如果变成1就不动了")
                else:
                    amoun = i.amount
                    print("减少了",amoun)
        modify = shopping.modify_cart(bookid,amoun)
        total = shopping.total_price
        save = shopping.save_price
        request.session["shopping"] = shopping
        print(total,"看看total变化了没")
        return JsonResponse({"amoun":amoun,"save": save,"total":total}, safe=True)




def increase(request):
    print("看看能不能进来increase函数")
    shopping = request.session.get("shopping")
    print(shopping)
    bookid = int(request.GET.get("bookid"))
    print("id",bookid)
    amount = request.GET.get("val")
    print("数量",amount)
    a = shopping.sums()
    b=shopping.total_price
    print(b,"我希望sum有值,因为总价是购物车的属性")
    if bookid and amount:
        for i in shopping.cartitem:
            if i.book.id == bookid:
                i.amount += 1
                amoun = i.amount
                print("增加了",amoun)
        modify = shopping.modify_cart(bookid,amoun)
        total = shopping.total_price
        save = shopping.save_price
        request.session["shopping"] = shopping
        return JsonResponse({"amoun":amoun,"save": save,"total":total}, safe=True)


def iptchange(request):
    print("进了iptchange函数")
    shopping = request.session.get("shopping")
    bookid = int(request.GET.get("bookid"))
    print("id", bookid)
    amount = int(request.GET.get("val"))
    print("数量", amount)
    a = shopping.sums()
    b = shopping.total_price
    print(b, "我希望sum有值,因为总价是购物车的属性")
    modify = shopping.modify_cart(bookid, amount)
    print("如果我进了这一步证明我可以实现变化了")
    total = shopping.total_price
    save = shopping.save_price
    print(total, "我是input里的总价")
    request.session["shopping"] = shopping
    print("我快开始返回了呢")
    return JsonResponse({"amoun": amount, "save": save, "total": total}, safe=True)


def delete1(request):
    shopping = request.session.get("shopping")
    print("我进了delete函数")
    bookid = int(request.GET.get("bookid"))
    print(bookid,type(bookid))
    shopping.delete_book(bookid)
    shopping = request.session["shopping"]
    print("我想渲染购物车页面")
    return render(request,"ddapp/car.html",{"shopping":shopping})




