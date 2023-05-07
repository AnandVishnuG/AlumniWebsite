from .models import Cart

def cartCount(request):
    count = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, isPaid=False).first()
    else:
        cart  = None
    if cart:
        count = cart.count
    return {'cartCount':count}