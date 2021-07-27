from basket.models import Basket


def basket(request):
    baskets = []

    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user)

    return {
        'basket': baskets,
    }
