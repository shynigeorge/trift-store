from django.urls import path
from . import views


urlpatterns=[
    path('',views.Home,name='homepage'),
    path('register',views.disp,name='reg'),
    path('login',views.login_page,name='login'),
    path('signout',views.signout,name='signout'),
    path('Registration',views.Custregistration,name='startreg'),
    path('productdesc/<int:pk>/',views.ProductDescription,name='productdesc'),
    path('productreg',views.ProductReg,name='productreg'),
    path('cusdeliver/<int:id>/',views.Delivery_address,name='cdel'),
    path('catviews/<int:pk>/',views.Category_views,name='catview'),
    path('catchildviews/<int:pk>/', views.Childcategory_views, name='catchildview'),
    path('catchgenderview/<str:gen>/',views.CatGenderviews,name='catgenderview'),
    path('addcart/<int:pid>/',views.add_cart,name='addcart'),
    path('cartshow',views.cartshow,name='cartshow'),
    path('card',views.Carddtls,name='card'),
    path('itmdelete/<int:id>/',views.itemdelete,name='itmdel'),
    path('deladdress',views.delivery_address,name='deladd'),
    path('cardselect',views.cardselect,name='cardselect'),
    path('myorder',views.My_Orders,name='myorder'),
    path('shop',views.shop,name='shop'),
    path('search',views.Search,name='search'),
    path('genfilter',views.Gender_filter,name='genfilter'),
    path('invoicepdf/<int:id>/',views.generate_invoice_pdf,name='invcpdf'),
    path('pricerange',views.price_range,name='pricerange'),
    path('genratecomp_pdf',views.generate_complete_pdf,name='gcomppdf'),



]

