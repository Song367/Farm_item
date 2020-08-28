from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from apps.user.models import User, store, product, order, chat, product_image,ShopCar
from django.conf import settings


def add(request):
    if request.method == 'GET':
        return render(request, 'store_template/add.html')
    else:
        name = request.POST.get('product_name')
        state = request.POST.get('text_area')
        price = request.POST.get('price')
        count = request.POST.get('count')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        image = request.FILES.getlist('files')
        category = request.POST.get('check_list')
        # print(category)
        if category == 'fruit':
            category = 3
        else:
            category = 4
        user_name = request.POST.get('SName')
        s = {}
        j = 0
        # 存放到本地文件
        for i in image:
            # print(i)
            path = '{}/product_img/{}'.format(settings.MEDIA_ROOT, i)
            pic = open(path, 'wb+')
            for c in i.chunks():
                pic.write(c)
            # 创建表中的图片
            s[j] = product_image.objects.create(image=i)
            j += 1
            pic.close()
        # 创建产品对象
        # product_obj=product.objects.create(name=name,product_state=state,price=price,count=count,product_address=address,product_phone=phone)
        # 创建一个店铺对象
        # arr=[]
        User_obj = User.objects.get(name=user_name)
        product_obj = product.objects.create(store_product=User_obj.store, name=name, product_state=state, price=price,
                                             count=count, product_address=address, product_phone=phone,
                                             category=category)

        User_obj.store.product_set.add(product_obj)
        # User.store.store_product=product_obj
        User_obj.store.save()
        for v in s.values():
            product_obj.product_img.add(v)
        return redirect('/store/productManage/')


def account(request, shop_id):
    #print(shop_id)
    return render(request, 'store_template/account.html')


def fruit(request):
    if request.method == 'GET':
        return render(request, 'store_template/fruit.html')
    else:
        p_obj = product.objects.filter(category=3)
        # print(p_obj)
        name = []
        state = {}
        price = {}
        image = {}
        id={}
        for i in p_obj:
            name.append(i.name)
            state[i.name] = i.product_state
            price[i.name] = i.price
            image[i.name] = list(i.product_img.values('image'))
            id[i.name]=i.id
        content = {'name': name, 'state': state, 'price': price, 'image': image,'ids':id}
        return JsonResponse(content)


def productManage(request):
    if request.method == 'GET':
        return render(request, 'store_template/goods.html')
    else:
        names = request.POST.get('names')
        # 用户对象
        user_obj = User.objects.get(name=names)
        # 产品对象
        product_obj = product.objects.filter(store_product=user_obj.store)

        # print(product_obj)
        # 产品名
        product_name = []
        product_pic = {}
        product_id = []
        for p_obj in product_obj:
            product_id.append(p_obj.id)
            product_name.append(p_obj.name)
            for image_obj in p_obj.product_img.values():
                product_pic[p_obj.id] = image_obj['image']
        # print(product_obj,product_obj.name)
        # product_pic = product_obj.
        # product_id=product_obj.id
        # print(product_id,'\n',product_name,'\n',product_pic)
        return JsonResponse({'product_name': product_name, 'product_pic': product_pic, 'product_id': product_id})


def modify(request, modify_id):
    if request.method == 'GET':
        #print(modify_id)
        return render(request, 'store_template/modify.html')
    else:
        name = request.POST.get('product_name')
        state = request.POST.get('text_area')
        price = request.POST.get('price')
        count = request.POST.get('count')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        image = request.FILES.getlist('files')
        category = request.POST.get('check_list')
        pid = request.POST.get('pid')
        #print(name, state, price, count, address, phone, image, category, pid)
        if category == 'fruit':
            category = 3
        else:
            category = 4
        product_obj = product.objects.get(id=pid)
        pic = product_image.objects.filter(product=product_obj)
        s = {}
        x = 0
        for i in pic:
            product_obj.product_img.remove(i)
        for i in image:
            path = '{}/product_img/{}'.format(settings.MEDIA_ROOT, i)
            pic = open(path, 'wb+')
            for j in i.chunks():
                pic.write(j)
            s[x] = product_image.objects.create(image=i)
            x += 1
            pic.close()

        # print(product_obj)
        product_obj.name = name
        product_obj.product_state = state
        product_obj.price = price
        product_obj.count = count
        product_obj.product_address = address
        product_obj.category = category
        product_obj.save()
        for v in s.values():
            product_obj.product_img.add(v)
        return redirect('/store/productManage')


def orderd(request):
    if request.method=='GET':
        return render(request, 'store_template/order.html')
    else:
        name=request.POST.get('username')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        pay=request.POST.get('pay')
        price=request.POST.get('prices')
        id = request.POST.get('id')
        sname=request.POST.get('sname')
        print(name,address,phone,pay,price,id)
        if sname and name and address and phone and price and pay:
            user_obj=User.objects.get(name=sname)
            if pay=='线上付款':
                pay=1
            else:
                pay=2
            order.objects.create(order_id=user_obj.shopcar,user_name=name,user_address=address,order_price=price,user_phone=phone,pay_way=pay)

            return render(request, 'store_template/order.html')
        return render(request,'store_template/order.html')


def shop(request, shop_id):
    if request.method=="GET":
        return render(request, 'store_template/shop.html')
    else:
        p_obj=product.objects.get(id=shop_id)
        p_val = list(product.objects.filter(id=shop_id).values())
        #print(p_val)
        image={}

        image[p_obj.name]=list(p_obj.product_img.values('image'))
        #print(image)
        return JsonResponse({'val':p_val,'image':image})


def shopCar(request,shop_id):
    if request.method=='GET':

        return render(request, 'store_template/shopcar.html')
    else:
        product_obj=product.objects.get(id=shop_id)
        print(product_obj)
        #product_obj.Shop_product.add()
        name=request.POST
        #print(name)
        user_obj=User.objects.get(name=name['name'])
        #print(user_obj)
        user_id=[i["Shop_user"] for i in list(ShopCar.objects.values('Shop_user'))]
        print(list(ShopCar.objects.values('Shop_user')))
        if user_obj.id in user_id:     #判断ShopCar中是否有数据
            #shop_obj=ShopCar.objects.create(Shop_user=user_obj)
            shop_obj=user_obj.shopcar
            #print(shop_obj)
            shop_obj.product_set.add(product_obj)
            shop_obj.save()
            product_obj.save()
        else:    #没数据就创建对象
            shop_obj = ShopCar.objects.create(Shop_user=user_obj)
            shop_obj.product_set.add(product_obj)
            shop_obj.save()
            product_obj.save()
            print(11)

        return HttpResponse('ok')


def shopRegister(request):
    return render(request, 'store_template/shopregister.html')


def vegetable(request):
    if request.method == 'GET':
        return render(request, 'store_template/vegetable.html')
    else:
        p_obj = product.objects.filter(category=4)
        # print(p_obj)
        name = []
        state = {}
        price = {}
        image = {}
        id={}
        for i in p_obj:
            name.append(i.name)
            state[i.name] = i.product_state
            price[i.name] = i.price
            image[i.name] = list(i.product_img.values('image'))
            id[i.name]=i.id
        content = {'name': name, 'state': state, 'price': price, 'image': image,'ids':id}
        return JsonResponse(content)


def userhelp(request):
    return render(request, 'store_template/userhelp.html')


def getStroe(request):
    getdata = request.POST.get('name')
    data = User.objects.filter(name=getdata).values('store')

    if data[0]['store'] is None:
        return JsonResponse({'status': 104})

    return JsonResponse({'status': 105})


def Store_reg(request):
    data = request.POST
    # print(data)
    ss = store.objects.create(name=data['name'], store_state=data['state'], store_address=data['address'],
                              store_phone=data['phone'])
    User.objects.filter(name=data['pre_name']).update(store=ss)
    return JsonResponse('ok', safe=False)


def tran_shopCar(request):
    data=request.POST.get('name')
    user_obj=User.objects.get(name=data)
    try:
        user_obj.shopcar
    except:
        return JsonResponse({'status':401})

    val=list(user_obj.shopcar.product_set.values('name', 'price'))
    img=user_obj.shopcar.product_set.all()
    image={}
    id={}
    for i in img:
        image[i.name]=list(i.product_img.values('image'))
        id[i.name]=i.id
    return JsonResponse({'data':val,'image':image,'id':id})

def del_shopCar(request):
    id=request.POST.get('id')
    name=request.POST.get('name')
    user_obj=User.objects.get(name=name)
    p_obj=product.objects.get(id=id)
    #print(p_obj)
    user_obj.shopcar.product_set.remove(p_obj)
    user_obj.shopcar.save()
    #product.save()

    return JsonResponse('ok',safe=False)


def tran_order(request):

    if request.method=='GET':
        return render(request,'index.html')

    if request.method=='POST':
        name=request.POST.get('name')
        user_obj=User.objects.get(name=name)
        try:
            if user_obj.shopcar:
                print('没有购物车')
        except:
            return JsonResponse({'status':401})#没有购物车
        try:
            if not user_obj.shopcar.order:
                print('没有订单')
        except:
            return JsonResponse({'status':402})#没有订单
        username=user_obj.shopcar.order.user_name
        price = user_obj.shopcar.order.order_price
        address = user_obj.shopcar.order.user_address
        phone = user_obj.shopcar.order.user_phone
        pro_name_old = list(user_obj.shopcar.product_set.values('name'))
        pro_name=[i['name'] for i in pro_name_old]
        return JsonResponse({'username':username,'price':price,'address':address,'phone':phone,'pro_name':pro_name,'status':1})

def del_order(request):
    name=request.GET.get('name')
    user_obj=User.objects.get(name=name)
    #user_obj.shopcar.order.delete()
    user_obj.shopcar.delete()

    return JsonResponse('ok',safe=False)



