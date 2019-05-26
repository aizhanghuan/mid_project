# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TAddress(models.Model):
    id = models.IntegerField(primary_key=True)
    receiver = models.CharField(max_length=40, blank=True, null=True)
    receive_address = models.CharField(max_length=60, blank=True, null=True)
    zip_code = models.CharField(max_length=40, blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True, null=True)
    tel = models.CharField(max_length=40, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    obligate = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_address'


class TCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=40, blank=True, null=True)
    parent_id = models.IntegerField()
    book_num = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_category'


class TDetail(models.Model):
    id = models.IntegerField(primary_key=True)
    bbok_name = models.CharField(max_length=40, blank=True, null=True)
    book_name = models.CharField(max_length=40, blank=True, null=True)
    headpic = models.CharField(max_length=40, blank=True, null=True)
    author = models.CharField(max_length=40, blank=True, null=True)
    publish = models.CharField(max_length=40, blank=True, null=True)
    publish_time = models.DateField(blank=True, null=True)
    version = models.CharField(max_length=40, blank=True, null=True)
    printtime = models.DateField(blank=True, null=True)
    isbn = models.CharField(db_column='ISBN', max_length=40, blank=True, null=True)  # Field name made lowercase.
    word_num = models.CharField(max_length=40, blank=True, null=True)
    page_num = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=40, blank=True, null=True)
    pages = models.CharField(max_length=40, blank=True, null=True)
    packing = models.CharField(max_length=40, blank=True, null=True)
    market_price = models.FloatField(blank=True, null=True)
    editer_commend = models.IntegerField(blank=True, null=True)
    storage = models.CharField(max_length=40, blank=True, null=True)
    sales = models.CharField(max_length=40, blank=True, null=True)
    dd_price = models.FloatField(blank=True, null=True)
    save = models.FloatField(blank=True, null=True)
    comment = models.CharField(max_length=60, blank=True, null=True)
    author_intro = models.CharField(max_length=60, blank=True, null=True)
    catalog = models.CharField(max_length=60, blank=True, null=True)
    media_comment = models.CharField(max_length=60, blank=True, null=True)
    pic_url = models.CharField(max_length=40, blank=True, null=True)
    shelf_time = models.DateField(blank=True, null=True)
    print_num = models.CharField(max_length=40, blank=True, null=True)
    list = models.CharField(max_length=10, blank=True, null=True)
    sore = models.FloatField(blank=True, null=True)
    picture = models.CharField(max_length=60, blank=True, null=True)
    category = models.ForeignKey(TCategory, models.DO_NOTHING, blank=True, null=True)
    obligate = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_detail'


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    all_price = models.FloatField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    order_number = models.CharField(max_length=40, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    address = models.ForeignKey(TAddress, models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_order'


class TOrderitem(models.Model):
    id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=40, blank=True, null=True)
    sub_total = models.FloatField(blank=True, null=True)
    order = models.ForeignKey(TOrder, models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(TDetail, models.DO_NOTHING, blank=True, null=True)
    book_count = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_orderitem'


class TUser(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    username = models.CharField(max_length=60, blank=True, null=True)
    password = models.CharField(max_length=40, blank=True, null=True)
    status = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user'



class ConfirmString(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=60, blank=True, null=True)
    u = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        db_table = 't_confirmstring'


