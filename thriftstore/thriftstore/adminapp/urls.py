from django.urls import path
from . import views

urlpatterns=[
    path('',views.AdminHome,name='adminpage'),
    path('staffview',views.Staffview,name='stv'),
    path('staffreg',views.StaffReg,name='str'),
    path('stdeact/<int:did>/',views.StaffDeactivate,name='std'),
    path('stact/<int:did>/',views.Staffactivate,name='sta'),
    path('stedit/<int:eid>/',views.Staffedit,name='ste'),
    path('custview',views.Custview,name='custv'),
    path('custdlt/<int:did>/', views.CustDelete, name='custdlt'),
    path('custact/<int:did>/', views.Custactivate, name='custa'),
    path('custprofile',views.customerprofile,name='cprofile'),
    path('products', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product'),
    path('products/<int:pk>/delete/', views.product_delete, name='proddlt'),
    path('sellerproview',views.sellerproductview,name='spv'),
    path('latest_orders',views.latest_orders,name='lorders'),
    path('ca_delete/<int:oid>/',views.ca_delete,name='cadel'),
    path('courier_register',views.Courier_Registration,name='courierreg'),
    path('courier_table/<int:oid>/',views.Courier_Table,name='coutable'),
    path('courier_assign/<int:oid>/<int:cid>/',views.Courier_AssignFunction,name='courassign'),
    path('courier_deassign/<int:oid>/<int:cid>/', views.Courier_DeassignFunction, name='courdeassign'),
    path('myproductorders',views.myproductorders,name='myprodorders'),
    path('courier_orders',views.Courier_Order_Confirm,name='courierorder'),
    path('courier_confirm/<int:cid>/',views.courier_confirmation,name='couconfirmorder'),
    path('courier_completed/<int:cid>/',views.courier_completed,name='couriercompleted'),
    path('courier_rejection/<int:cid>/',views.courier_cancelling,name='courierrejecting'),
    path('confirmed_orders',views.confirmed_orders,name='confirmorderlist'),
    path('completed_orders',views.completed_orders,name='completedorderslist'),


]

