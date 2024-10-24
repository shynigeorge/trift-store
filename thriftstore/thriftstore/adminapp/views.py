from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from demo.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
@login_required(login_url='login')
def AdminHome(request):
    try:
        seller = customer.objects.get(user=request.user)
        if seller.is_seller == True:
            status = 'sel'
        else:
            status = 'cust'
    except:
        pass
        status = ''
    print('status = ', status)

    return render(request, 'admindash.html', {'status': status})


# Staff View

def Staffview(request):
    data = staff.objects.all()
    return render(request, 'staffview.html', {'st': data})


# Staff Registration

def StaffReg(request):
    if request.method == 'POST':
        um = request.POST['um']
        nm = request.POST['nm']
        em = request.POST['em']
        ph = request.POST['ph']
        pw = request.POST['psd']
        cpw = request.POST['cpsd']
        hn = request.POST['hn']
        dist = request.POST['dis']
        street = request.POST['st']
        state = request.POST['state']
        gen = request.POST['gen']
        if pw == cpw:
            if User.objects.filter(username=um, email=em).exists():
                print('User already exist')
                messages.info(request, "Staff already exists ..!")
            else:
                user = User.objects.create_user(username=um, email=em, password=pw, is_staff=True)
                user.save()
                staf = staff(user=user, staff_name=nm, staff_email=em, staff_ph=ph, staff_gender=gen,
                             staff_status=True, staff_house_name=hn, staff_street=street, staff_district=dist,
                             staff_state=state)
                staf.save()
                messages.info(request, "Registartion Succesfful ..!")
                return redirect('stv')
    return render(request, 'staffreg.html')


# Staff Deactivate Func

def StaffDeactivate(request, did):
    st = staff.objects.get(id=did)
    st.staff_status = False
    st.save()
    messages.info(request, "Staff Deactivate ..!")
    return redirect('stv')


def Staffactivate(request, did):
    st = staff.objects.get(id=did)
    st.staff_status = True
    st.save()
    messages.info(request, "Staff activated ..!")
    return redirect('stv')


# Staff Edit
@login_required(login_url='login')
def Staffedit(request, eid):
    st = staff.objects.get(id=eid)
    if request.method == 'POST':
        um = request.POST['um']
        nm = request.POST['nm']
        em = request.POST['em']
        ph = request.POST['ph']
        hn = request.POST['hn']
        dist = request.POST['dis']
        street = request.POST['st']
        state = request.POST['state']
        gen = request.POST['gen']
        st.user.username = um
        st.staff_name = nm
        st.staff_email = em
        st.staff_phone = ph
        st.staff_house_name = hn
        st.staff_district = dist
        st.staff_street = street
        st.staff_state = state
        st.staff_gender = gen
        st.save()
        return redirect('stv')
    return render(request, 'stredit.html', {'st': st})


# Customer View
def Custview(request):
    data = CustomerDetails.objects.all()
    return render(request, 'custview.html', {'cust': data})


# Customer Deactivate

def CustDelete(request, did):
    cust = customer.objects.get(id=did).delete()
    return redirect('custv')


# Customer Activate

def Custactivate(request, did):
    cust = customer.objects.get(id=did)
    cust.customer_status = True
    cust.save()
    return redirect('custv')


# Customer Registration


# Sell product

def Prodsell(request):
    if request.method == 'POST':
        um = request.POST['um']
        nm = request.POST['nm']
        em = request.POST['em']
        ph = request.POST['ph']
        pw = request.POST['psd']
        cpw = request.POST['cpsd']
        hn = request.POST['hn']
        dist = request.POST['dis']
        street = request.POST['st']
        state = request.POST['state']
        gen = request.POST['gen']
        if pw == cpw:
            if User.objects.filter(username=um, email=em).exists():
                print('User already exist')
                messages.info(request, "Alreday exists ..!")
            else:
                user = User.objects.create_user(username=um, email=em, password=pw, is_staff=True)
                user.save()
                staf = staff(user=user, staff_name=nm, staff_email=em, staff_ph=ph, staff_gender=gen,
                             staff_status=True, staff_house_name=hn, staff_street=street, staff_district=dist,
                             staff_state=state)
                staf.save()
                messages.info(request,"Registered successful ..!")
                return redirect('stv')
    return render(request, 'staffreg.html')


# Customer View / Edit Profile
@login_required(login_url='login')
def customerprofile(request):
    u = customer.objects.get(user=request.user)
    if request.method == 'POST':
        um = request.POST['uname']
        fn = request.POST['fn']
        ln = request.POST['ln']
        em = request.POST['em']
        ph = request.POST['ph']
        gen = request.POST['gen']
        dob = request.POST['dob']
        u.user.username = um
        u.fname = fn
        u.lname = ln
        u.email = em
        u.phone = ph
        u.gender = gen
        u.dob = dob
        u.save()
        return redirect('/')
    return render(request, 'customer_profile.html', {'u': u})


def product_list(request):
    products = Seller_Product.objects.all()
    return render(request, 'prodview.html', {'products': products})


def product_detail(request, pk):
    product = Seller_Product.objects.get(id=pk)
    return render(request, 'prodv.html', {'product': product})


def product_delete(request, pk):
    product = Seller_Product.objects.get(id=pk)
    product.delete()
    messages.info(request, "Deleted")
    if request.user.is_superuser:
        return redirect('product_list')
    else:
        return redirect('spv')


# Seller Product View
@login_required(login_url='login')
def sellerproductview(request):
    try:
        prod = Seller_Product.objects.filter(seller=request.user).order_by('-id')
    except:
        prod = ''
    return render(request, 'prodview.html', {'products': prod})


@login_required(login_url='login')
def myproductorders(request):
    ord = Order.objects.filter(pay=True)
    k = []
    for i in ord:
        g = [k.append(x) for x in i.products.filter(seller=request.user).order_by('-id')]
        print(g)
    print('k =====', k)
    return render(request, 'myproductorder.html', {'pro': k, 'orders': ord})


@login_required(login_url='login')
def latest_orders(request):
    orders = Order.objects.all().order_by('-id')
    ca = list(Courier_Assign.objects.all().values_list('order_id', flat=True))
    print(ca)
    com = 0
    cas = Courier_Assign.objects.all()
    return render(request, 'latest_orders.html', {'orders': orders, 'ca': ca, 'cas': cas,'com':com})


def ca_delete(request, oid):
    ca = Courier_Assign.objects.get(order_id=oid)
    ca.delete()
    messages.info(request, "Courier rejeccted")
    print(ca)
    return redirect('lorders')


def Courier_Registration(request):
    if request.method == 'POST':
        um = request.POST['um']
        cnm = request.POST['cnm']
        em = request.POST['em']
        ph = request.POST['ph']
        dis = request.POST['dis']
        st = request.POST['st']
        pw = request.POST['pw']
        pw2 = request.POST['pw2']
        if pw == pw2:
            if User.objects.filter(username=um, email=em).exists():
                print("username already taken")
                messages.info(request, "username taken ..!")
            else:
                u = User.objects.create_user(username=um, email=em, password=pw)
                u.save()
                c = Courier(user=u, company_name=cnm, email=em, phone=ph, district=dis, state=st)
                c.save()
                messages.info(request, "Registered")
                return redirect('adminpage')

    return render(request, 'courier_register.html')


def Courier_Table(request, oid):
    c = Courier.objects.all()
    ca = Courier_Assign.objects.filter(order_id=oid)
    print('cassign = ', ca)
    return render(request, 'courier_table.html', {'c': c, 'oid': oid, 'ca': ca})


def Courier_AssignFunction(request, oid, cid):
    if Courier_Assign.objects.filter(courier_id=cid, order_id=oid, status='pending').exists():
        pass
    else:
        ca = Courier_Assign(courier_id=cid, order_id=oid, status='pending')
        ca.save()
        messages.info(request, "Courier Assigned")
    return redirect('coutable', oid)


def Courier_DeassignFunction(request, oid, cid):
    ca = Courier_Assign.objects.get(courier_id=cid, order_id=oid)
    ca.delete()
    messages.info(request, "Courier Deassigned")
    return redirect('coutable', oid)


def Courier_Order_Confirm(request):
    ca = Courier_Assign.objects.filter(courier__user=request.user).order_by('-id')
    cust = CustomerDetails.objects.all()
    custp = customer.objects.all()
    return render(request, 'courier_assign.html', {'orders': ca, 'cust': cust, 'cp': custp})


def courier_confirmation(request, cid):
    ca = Courier_Assign.objects.get(id=cid)
    if request.method == 'POST':
        date = request.POST['date']
        ca.delivery_date = date
        ca.status = 'accepted'
        ca.save()
        messages.info(request, "Courier Confirmed..!")
        return redirect('courierorder')


def courier_completed(request, cid):
    ca = Courier_Assign.objects.get(id=cid)
    ca.completed = True
    ca.order.delivered = True
    ca.order.save()
    ca.save()
    messages.info(request, "Order completed..!")
    return redirect('courierorder')


def courier_cancelling(request, cid):
    ca = Courier_Assign.objects.get(id=cid)
    ca.status = 'rejected'
    ca.save()
    messages.info(request, "Order rejected..!")
    return redirect('courierorder')


def confirmed_orders(request):
    courier = list(Courier_Assign.objects.filter(status='accepted').values_list('order_id',flat=True))
    orders = []
    for i in courier:
        orders.append(Order.objects.get(id=i))
    com=1
    ca = list(Courier_Assign.objects.all().values_list('order_id', flat=True))
    print(ca)
    cas = Courier_Assign.objects.all()
    return render(request, 'latest_orders.html', {'orders': orders, 'ca': ca, 'cas': cas,'com':com})


def completed_orders(request):
    courier = list(Courier_Assign.objects.filter(status='accepted',completed=True).values_list('order_id',flat=True))
    orders = []
    for i in courier:
        orders.append(Order.objects.get(id=i))
    com=2
    ca = list(Courier_Assign.objects.all().values_list('order_id', flat=True))
    print(ca)
    cas = Courier_Assign.objects.all()
    return render(request, 'latest_orders.html', {'orders': orders, 'ca': ca, 'cas': cas,'com':com})

