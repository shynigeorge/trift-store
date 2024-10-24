from .models import *


def itemcount(request):
    try:
        itcount = len(Items.objects.filter(cart__user=request.user))
    except:
        itcount = 0

    return itcount