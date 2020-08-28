from django.shortcuts import render
from django.http import JsonResponse
from apps.user.models import User
from .models import product
def index(request):
    if request.method=="GET":
        return render(request,'index.html')
    else:
        fname = []
        fid = {}
        fstate = {}
        p_f_img = {}
        f_price={}
        p_f_obj = product.objects.filter(category=3)
        for i in p_f_obj:
            fname.append(i.name)
            fid[i.name] = i.id
            fstate[i.name] = i.product_state
            p_f_img[i.name] = list(i.product_img.values('image'))
            f_price[i.name]=i.price
        vname = []
        vid = {}
        vstate = {}
        p_v_img = {}
        v_price={}
        p_v_obj = product.objects.filter(category=4)
        for i in p_v_obj:
            vname.append(i.name)
            vid[i.name] = i.id
            vstate[i.name] = i.product_state
            p_v_img[i.name] = list(i.product_img.values('image'))
            v_price[i.name]=i.price

        content = {'fimage': p_f_img, 'fname': fname, 'fstate': fstate, 'fid': fid,'fprice':f_price, 'vimage': p_v_img, 'vname': vname,
                   'vstate': vstate, 'vid': vid,'v_price':v_price}

        return JsonResponse(content)


def login(request):
    if request.method=='GET':
        return render(request,'login_reg/login.html')
    else:
        user = list(User.objects.values())
        fname=request.POST.get('f_name')

        for i in user:

            if i['name'] == fname:
                return JsonResponse({'status': '1'})
        return JsonResponse({'status':'102'})


def login_pwd(request):
    names=request.POST.get('name')
    user=User.objects.filter(name=names).values()
    #print(User.objects.get(name=names))
    fpwd=request.POST.get('password')

    if user[0]['password']==fpwd:
        return JsonResponse({'status':'1'})
    return JsonResponse({'status':'103'})


def register(request):
    if request.method=='GET':
        return render(request,'login_reg/register.html')
    else:
        user=list(User.objects.values())
        name = request.POST.get('name')
        print(name)
        #print(len(user))
        if len(user)==0:
            print('为空')
            name2 = request.POST.get('names')
            password = request.POST.get('password')
            # print(name2,password)
            if name2 and password:
                User.objects.create(name=name2, password=password)
                return JsonResponse({'status': '1'})


        else:
            name2=request.POST.get('names')
            for i in user:
                #print(i['name'])
                if i['name']==name:
                    return JsonResponse({'status':'101'})
                else:
                    password=request.POST.get('password')
                    #print(name2,password)
                    if name2 and password:
                        User.objects.create(name=name2,password=password)
                        return JsonResponse({'status':'1'})
            return JsonResponse('ok',safe=False)




