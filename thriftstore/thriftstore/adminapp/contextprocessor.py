from demo.models import *


def seller_status(request):
    try:
        seller = customer.objects.get(user=request.user)
        if seller.is_seller == True:
            status = 'sel'
        else:
            status = 'cust'
    except:
        pass
        status = ''
    return {'status': status}
