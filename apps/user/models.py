from django.db import models
PAY_ONE=1
PAY_TWO=2
PAYWAY=(
    (PAY_ONE,'线上支付'),
    (PAY_TWO,'货到付款'),
)
CATEGORY_ONE=3
CATEGORY_TWO=4
CATEGORY=(
    (CATEGORY_ONE,'fruit'),
    (CATEGORY_TWO,'vegetable'),
)
#图片
class product_image(models.Model):
    image=models.ImageField(upload_to='product_img',blank=True)
    class Meta:
        db_table='product_image'


#店铺表
class store(models.Model):
    name=models.CharField(max_length=32,verbose_name='店铺名')
    store_state=models.TextField(verbose_name='店铺描述')
    #store_product=models.ForeignKey(product,verbose_name='店铺产品',on_delete=models.CASCADE,null=True)
    store_address=models.CharField(max_length=128,verbose_name='店铺地址')
    store_phone=models.CharField(max_length=128,verbose_name='店铺电话')
    class Meta:
        db_table='store'


#产品表
class product(models.Model):
    name=models.CharField(max_length=32,verbose_name='产品名')
    price=models.FloatField(verbose_name='产品价格')
    count=models.IntegerField(verbose_name='产品数量')
    product_state=models.TextField(verbose_name='产品描述')
    category=models.CharField(choices=CATEGORY,default=CATEGORY_ONE,verbose_name='商品类别',max_length=32)
    product_address=models.CharField(max_length=128,verbose_name='生产地')
    product_phone=models.CharField(max_length=32,verbose_name='联系电话')
    store_product=models.ForeignKey(store,on_delete=models.CASCADE,null=True)
    product_img=models.ManyToManyField(product_image,verbose_name='产品图片')
    Shop_product=models.ForeignKey('ShopCar',on_delete=models.DO_NOTHING,verbose_name='购物车商品',null=True)
    class Meta:
        db_table='product'

#购物车
class ShopCar(models.Model):
    Shop_user=models.OneToOneField('User',on_delete=models.CASCADE)


#订单表
class order(models.Model):
    order_id=models.OneToOneField('ShopCar',verbose_name='订单对应的产品',on_delete=models.CASCADE,null=True)
    order_price=models.FloatField(verbose_name='订单价格',default=0.0)
    user_address=models.CharField(max_length=128,verbose_name='收件人地址')
    user_phone=models.CharField(max_length=32,verbose_name='收件人电话')
    pay_way=models.PositiveIntegerField(choices=PAYWAY,default=PAY_ONE,verbose_name='支付方式')
    user_name=models.CharField(max_length=32,verbose_name='收件人姓名')

    class Meta:
        db_table='order'

#用户表
class User(models.Model):
    name=models.CharField(max_length=32,verbose_name='用户名')
    password=models.CharField(max_length=128,verbose_name='用户密码')
    store=models.OneToOneField(store,on_delete=models.CASCADE,null=True)

    class Meta:
        db_table='User'

#聊天记录表
class chat(models.Model):
    send_user=models.ManyToManyField(User,verbose_name='发送者')
    chat_time=models.DateTimeField(auto_now_add=True,verbose_name='时间')
    chat_content=models.TextField(verbose_name='聊天内容')

    class Meta:
        db_table='chat'


