from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa
from io import BytesIO


# Create your views here.
def TotalItem(request):
    try:
        itc = len(Items.objects.filter(cart__user=request.user))
    except:
        itc = ''
    return itc


def Home(request):
    sct = Subcategory.objects.order_by('?')
    prod = Seller_Product.objects.order_by('?')[:6]
    prodall = Seller_Product.objects.order_by('?')
    # items = Items.objects.filter(cart__paid=True).values_list('products_id',flat=True)
    # print("Sold Items = ",items)

    return render(request, 'index.html', {'sct': sct, 'prod': prod, 'itc': TotalItem(request), 'prodall': prodall})


def Gender_filter(request):
    gen = request.GET.get('gender')
    print('Gender  =', gen)
    prod = Seller_Product.objects.filter(gender=gen).order_by('?')[:4]
    if prod:
        prodall = prod
    else:
        prodall = Seller_Product.objects.order_by('?')[:4]
    return render(request, 'filteredproducts.html', {'prodall': prodall})


def contact_page(request):
    return HttpResponse('Contact Page')


@login_required(login_url='login')
def signout(request):
    logout(request)
    return redirect('homepage')


def disp(request):
    return render(request, 'register.html')


# Personal Details
def Custregistration(request):
    if request.method == 'POST':
        um = request.POST['um']
        nm = request.POST['fm']
        lm = request.POST['lm']
        gen = request.POST['gen']
        cimg = request.FILES['cimg']
        em = request.POST['em']
        ph = request.POST['ph']
        dob = request.POST['dob']
        pw = request.POST['pw']
        cpw = request.POST['pw2']
        seller_customers = request.POST['userRole']
        print('password1 = ', pw)
        print('password2 = ', cpw)
        if pw == cpw:
            print("Password verified")
        if pw == cpw:
            if seller_customers == 'seller':
                s_c = True
            else:
                s_c = False
            if User.objects.filter(username=um, email=em).exists():
                print('User already exist')
                messages.info(request, 'User already exist')
            else:
                user = User.objects.create_user(username=um, email=em, password=pw)
                user.save()
                cust = customer(user=user, fname=nm, lname=lm, email=em, phone=ph, gender=gen,
                                cimage=cimg, dob=dob, is_seller=s_c)
                cust.save()
                messages.info(request, "Personnel Deatils added ..!")
                return redirect('cdel', id=cust.id)
        else:
            print("Password not matching")
            messages.info(request, 'Password not matching')
            return redirect('startreg')
    return render(request, 'register.html')


# Delivery details

def Delivery_address(request, id):
    if request.method == "POST":
        hname = request.POST['address']
        city = request.POST['city']
        landmark = request.POST['landmark']
        district = request.POST['district']
        pin = request.POST['pin']
        state = request.POST['state']
        cus = CustomerDetails(customer_id=id, housename=hname, city=city, pincode=pin, landmark=landmark,
                              district=district, state=state)
        cus.save()
        messages.info(request, "Registration Completed..!")
        return redirect('/')
    return render(request, 'custreg.html', {'itc': TotalItem(request)})


def shop(request):
    pro = Seller_Product.objects.all()
    sct = Subcategory.objects.all()
    return render(request, 'shop.html', {'prod': pro, 'sct': sct, 'itc': TotalItem(request)})


def login_page(request):
    try:
        cou = list(Courier.objects.all().values_list('user', flat=True))
    except:
        cou = ''
        pass
    if request.method == 'POST':
        uname = request.POST['username']
        password = request.POST['password']
        role = request.POST['userRole']
        print('role = ', role)
        user = authenticate(username=uname, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('adminpage')
            elif user.is_staff:
                return redirect('adminpage')
            elif role == 'seller':
                try:
                    c = customer.objects.get(user=request.user)
                    if c.is_seller == True:
                        return redirect('adminpage')
                except:
                    if request.user.id in cou:
                        return redirect('adminpage')
                    else:
                        return redirect('/')
            else:
                return redirect('/')
        else:
            print("Invalid user")
            messages.info(request, "Invalid User..!")
    return render(request, 'login.html')


def ProductDescription(request, pk):
    prod = Seller_Product.objects.get(id=pk)
    return render(request, 'proddesc.html', {'p': prod, 'itc': TotalItem(request)})


sp = 100
lp = 800


def Category_views(request, pk):
    prod = Seller_Product.objects.filter(subcategory=pk).order_by('?')
    pc = len(prod)
    sc = Subcategory.objects.all()
    cat = Category.objects.all()

    return render(request, 'categoryv.html',
                  {'cat': cat, 'prod': prod, 'pc': pc, 'sc': sc, 'itc': TotalItem(request), 'sp': sp, 'lp': lp,
                   'pk': pk})


def price_range(request):
    global sp, lp
    if request.method == 'POST':
        pk = request.POST['primary']
        sp = request.POST['starting-price']
        lp = request.POST['limit-percentage']
        print('Price range = ', sp, lp)

    price_range_condition = Q(price__gte=sp, price__lte=lp)
    category_condition = Q(category=pk)
    subcategory_condition = Q(subcategory=pk)
    prod = Seller_Product.objects.filter(price_range_condition & category_condition | subcategory_condition)
    pc = len(prod)
    sc = Subcategory.objects.all()
    cat = Category.objects.all()
    return render(request, 'categoryv.html',
                  {'cat': cat, 'prod': prod, 'pc': pc, 'sc': sc, 'itc': TotalItem(request), 'sp': sp, 'lp': lp,
                   'pk': pk})


def Childcategory_views(request, pk):
    cat = Category.objects.all()
    prod = Seller_Product.objects.filter(category=pk)
    sc = Subcategory.objects.all()
    pc = len(prod)
    return render(request, 'categoryv.html',
                  {'cat': cat, 'prod': prod, 'pc': pc, 'sc': sc, 'itc': TotalItem(request), 'sp': sp, 'lp': lp,
                   'pk': pk})


def CatGenderviews(request, gen):
    prod = Seller_Product.objects.filter(gender=gen)
    pc = len(prod)
    cat = Category.objects.all()
    pk = cat.first().id
    sc = Subcategory.objects.all()
    return render(request, 'categoryv.html',
                  {'cat': cat, 'prod': prod, 'pc': pc, 'sc': sc, 'itc': TotalItem(request), 'sp': sp, 'lp': lp,
                   'pk': pk})


@login_required(login_url='login')
def ProductReg(request):
    scat = Subcategory.objects.all()
    if request.method == 'POST':

        nm = request.POST['productName']
        desc = request.POST['productDescription']
        pimg = request.FILES['productImage']
        gender = request.POST['productGender']
        size = request.POST['productSize']
        color = request.POST['productColour']
        material = request.POST['clothMaterial']
        price = request.POST['productPrice']
        brand = request.POST['brand']
        subcat = request.POST.get('subcategory')
        c = Subcategory.objects.get(id=subcat)
        catid = c.category.id
        cat = Category.objects.get(id=catid)
        if Seller_Product.objects.filter(name=nm).exists():
            print('Product already exists')
            messages.info(request, "Product already exists...!")
        else:
            pro = Seller_Product(seller=request.user, category=cat, subcategory=c, name=nm, description=desc,
                                 product_Image=pimg
                                 , gender=gender, size=size, color=color, cloth_Material=material,
                                 price=price, brand=brand)
            pro.save()
            if request.user.is_superuser:
                return redirect('product_list')
            else:
                return redirect('spv')
    return render(request, 'productreg.html', {'scat': scat})


# Adding products to the cart
@login_required(login_url='login')
def add_cart(request, pid):
    prod = Seller_Product.objects.get(id=pid)
    cart, ct = Cart.objects.get_or_create(user=request.user)
    print('status', ct)
    if Cart.objects.filter(user=request.user).exists():
        if Items.objects.filter(cart=cart, products=prod).exists():
            print("Item already exists in your cart")
            messages.info(request, "Item already exists in your cart..!")
            return redirect('cartshow')
        else:
            item = Items(cart=cart, products=prod)
            item.save()
            return redirect('cartshow')
    else:
        print("Error")
        messages.info(request, "Error..!")
        return redirect('/')


# Cart View
@login_required(login_url='login')
def cartshow(request):
    try:
        items = Items.objects.filter(cart__user=request.user, products__sold=False)
        ct = Cart.objects.get(user=request.user)
        print("items = ", items)

        tot = 0
        for i in items:
            tot += i.products.price
    except:
        items = ''
        tot = ''
        ct = ''
        pass
    return render(request, 'cart.html',
                  {'items': items, 'np': TotalItem(request), 'tot': tot, 'ct': ct, 'itc': TotalItem(request)})


def total(request):
    try:
        items = Items.objects.filter(cart__user=request.user)
        print("items = ", items)
        np = len(items)
        tot = 0
        for i in items:
            tot += i.products.price
        return tot
    except:
        tot = 0
        return tot


# Cart Item Delete
def itemdelete(request, id):
    item = Items.objects.get(id=id)
    item.delete()
    return redirect('cartshow')


# Re-Ensuring Delivery Address
@login_required(login_url='login')
def delivery_address(request):
    try:
        deliveryadd = CustomerDetails.objects.get(customer__user=request.user)
    except:
        deliveryadd = ''
        pass
    if request.method == 'POST':
        hname = request.POST['address']
        city = request.POST['city']
        landmark = request.POST['landmark']
        district = request.POST['district']
        pin = request.POST['pin']
        state = request.POST['state']
        deliveryadd.housename = hname
        deliveryadd.city = city
        deliveryadd.pincode = pin
        deliveryadd.landmark = landmark
        deliveryadd.district = district
        deliveryadd.state = state
        deliveryadd.save()
        return redirect('card')

    return render(request, 'delivery_address.html', {'delad': deliveryadd, 'itc': TotalItem(request)})


@login_required(login_url='login')
def Carddtls(request):
    try:
        cd = Card.objects.filter(user=request.user).order_by('-id').first()
    except:
        cd = ''
    cds = Card.objects.filter(user=request.user).order_by('-id')
    if request.method == 'POST':
        cowner = request.POST['owner']
        cn = request.POST['cnum']
        ex = request.POST['exp']
        cv = request.POST['cvv']
        if Card.objects.filter(name=cowner, number=cn, expdate=ex, cvv=cv, user=request.user).exists():
            cart = Cart.objects.get(user=request.user)
            cart.paid = True
            cart.total_amount = total(request)
            print("total = ", total(request))
            cart.profit_amount = total(request) * 20 / 100
            print("profit = ", total(request) * 20 / 100)
            cart.seller_amount = total(request) - total(request) * 20 / 100
            print("seller_amount = ", total(request) - total(request) * 20 / 100)
            cart.save()
            for i in Items.objects.filter(cart=cart):
                i.products.sold = True
                i.products.save()
                i.save()
            order = Order(user=request.user, pay=True, total_amount=total(request))
            order.save()
            for i in Items.objects.filter(cart=cart):
                pro = Seller_Product.objects.get(id=i.products.id)
                order.products.add(pro)
                order.save()
            for i in Items.objects.filter(cart=cart):
                i.delete()
            messages.info(request, "Payment Successful And Order Placed ..!")
            return redirect('/')
        else:
            card = Card(name=cowner, number=cn, expdate=ex, cvv=cv, user=request.user)
            card.save()
            cart = Cart.objects.get(user=request.user)
            cart.paid = True
            cart.total_amount = total(request)
            print("total = ", total(request))
            # Here Taking 20% as admin profit of the overall price
            cart.profit_amount = total(request) * 20 / 100
            print("profit = ", total(request) * 20 / 100)
            cart.seller_amount = total(request) - total(request) * 20 / 100
            print("seller_amount = ", total(request) - total(request) * 20 / 100)
            cart.save()
            for i in Items.objects.filter(cart=cart):
                i.products.sold = True
                i.save()
            order = Order(user=request.user, pay=True, total_amount=total(request))
            order.save()
            for i in Items.objects.filter(cart=cart):
                pro = Seller_Product.objects.get(id=i.products.id)
                order.products.add(pro)
                order.save()
            for i in Items.objects.filter(cart=cart):
                i.delete()
            messages.info(request, "Payment Successful And Order Placed ..!")
            return redirect('/')
    return render(request, 'card.html', {'cd': cd, 'cds': cds, 'tot': total(request), 'itc': TotalItem(request)})


@login_required(login_url='login')
def cardselect(request):
    card = request.GET.get('card')
    cd = Card.objects.get(id=card)
    return render(request, 'cardselect.html', {'cd': cd, 'itc': TotalItem(request)})


@login_required(login_url='login')
def My_Orders(request):
    tot = 0
    count = 1100
    orders = Order.objects.filter(user=request.user).order_by('-id')
    for i in orders:
        tot += i.total_amount
        count += 360

    return render(request, 'myorder.html', {'order': orders, 'tot': tot, 'count': count})


def Search(request):
    query = request.GET.get('q')
    if query:
        pro = Seller_Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(gender__icontains=query) | Q(
                color__icontains=query) | Q(cloth_Material__icontains=query) | Q(brand__icontains=query) | Q(
                price__icontains=query))
    else:
        pro = Seller_Product.objects.all()
    return render(request, 'shop2.html', {'prod': pro})


def generate_invoice_pdf(request, id):
    order = Order.objects.get(id=id)
    reg = customer.objects.all()
    ca = Courier_Assign.objects.all()

    # Get data for your template, you can replace it with your own dynamic data retrieval logic
    context = {
        'i': order,
        'reg': reg,
        'ca': ca,
    }

    # Render the template
    template = get_template('invoice.html')
    html_content = template.render(context)

    # Create a PDF file
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename="your_pdf_filename.pdf"'
        return response

    return HttpResponse('Error generating PDF: %s' % pdf.err)


######### Admin Pdf #############


def generate_complete_pdf(request):
    tot=0
    courier = list(Courier_Assign.objects.filter(status='accepted',completed=True).values_list('order_id',flat=True))
    orders = []
    for i in courier:
        orders.append(Order.objects.get(id=i))
    com=2
    ca = list(Courier_Assign.objects.all().values_list('order_id', flat=True))
    print(ca)
    for k in orders:
        tot += k.total_amount
    cas = Courier_Assign.objects.all()

    # Get data for your template, you can replace it with your own dynamic data retrieval logic
    context = {
        'orders': orders,
        'ca': ca,
        'cas': cas,
        'com': com,
        'tot':tot
    }

    # Render the template
    template = get_template('complete_pdf.html')
    html_content = template.render(context)

    # Create a PDF file
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename="your_pdf_filename.pdf"'
        return response

    return HttpResponse('Error generating PDF: %s' % pdf.err)




