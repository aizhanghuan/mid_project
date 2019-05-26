from ddapp.models import TDetail


class Cartitem():
    def __init__(self,book,amount):  #为什么要传入两个参数，不传不能调用的吗
        self.book = book
        self.amount = amount


class Cart():
    def __init__(self):
        self.save_price = 0
        self.total_price = 0
        self.cartitem = []
    def add_book_toCart(self,bookid):  #加入书籍
        for i in self.cartitem:
            if i.book.id==bookid:
                i.amount+=1
                self.sums()
                return i.amount
        book = TDetail.objects.get(id=bookid)
        self.cartitem.append(Cartitem(book,1))  #这里的C是大写还是小写，用类还是方法
        self.sums()
        return
        # book = TDetail.objects.get(id=bookid)
        # self.cartitem.append(Cartitem(book, 1))  # 这里的C是大写还是小写，用类还是方法
        # self.sums()
    def modify_cart(self,bookid,amount):
        for i in self.cartitem:
            if i.book.id== bookid:
                i.amount=amount
        self.sums()


    def delete_book(self,bookid):
        for i in self.cartitem:
            if i.book.id == bookid:
                self.cartitem.remove(i)
        self.sums()






    def sums(self):  #计算购物车商品的节省金额以及总金额
        self.save_price = 0
        self.total_price = 0
        for i in self.cartitem:
            self.save_price += (i .book.market_price-i.book.dd_price)*i.amount
            self.total_price += i.book.dd_price*i.amount






