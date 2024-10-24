from django.contrib.auth.models import User
from django.db import models
from month.models import MonthField

roles = (('none', 'none'), ('female', 'female'), ('male', 'male'), ('unisex', 'unisex'))


class staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    staff_name = models.CharField(max_length=30)
    staff_email = models.EmailField(null=True)
    staff_ph = models.CharField(max_length=10)
    staff_gender = models.CharField(max_length=10, choices=roles)
    staff_status = models.BooleanField(default=True)
    staff_house_name = models.CharField(max_length=100, null=True)
    staff_street = models.CharField(max_length=100, null=True)
    staff_district = models.CharField(max_length=50, null=True)
    staff_state = models.CharField(max_length=30, null=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.staff_name


class customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=25)
    dob = models.DateField(null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=10)
    cimage = models.ImageField(upload_to='customer_images', null=True)
    gender = models.CharField(max_length=10, choices=roles)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.fname + ' ' + self.lname


class CustomerDetails(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE, null=True)
    housename = models.CharField(max_length=100)
    city = models.CharField(max_length=80)
    pincode = models.CharField(max_length=6)
    landmark = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=30)
    state = models.CharField(max_length=20)

    def __str__(self):
        return self.customer.fname + ' ' + self.customer.lname


class Category(models.Model):
    name = models.CharField(max_length=30)
    catimage = models.ImageField(upload_to='category_images', null=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=30)
    subimage = models.ImageField(upload_to='subcategory_images', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Seller_Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    product_Image = models.ImageField(upload_to='product_images', null=True)
    gender = models.CharField(max_length=10, choices=roles)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=30, default='')
    cloth_Material = models.CharField(max_length=30)
    price = models.IntegerField()
    brand = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True, null=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField(null=True)
    profit_amount = models.FloatField(null=True)
    seller_amount = models.FloatField(null=True)
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Items(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    products = models.ForeignKey(Seller_Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.cart.user.username


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20)
    number = models.CharField(max_length=16)
    expdate = MonthField("Month Value", help_text='Enter month and year only', null=True)
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Seller_Product)
    total_amount = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    pay = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Courier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    district = models.CharField(max_length=30)
    state = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username


class Courier_Assign(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20,choices=(('accepted','accepted'),('pending','pending'),('rejected','rejected')),default='pending')
    assigned_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(null=True)

    def __str__(self):
        return self.order.user.username
