from django.http import JsonResponse
from django.views.decorators.http import require_GET
from orders.models import MenuItem, Restaurant

@require_GET
def restaurant_menu_api(request, restaurant_id):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Authentication required"}, status=403)
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({"error": f"Restaurant {restaurant_id} was not found."}, status=404)
    items = MenuItem.objects.filter(restaurant=restaurant, available=True)
    if "max_price" in request.GET:
        items = items.filter(price__lte=request.GET["max_price"])
    return JsonResponse(list(items.values("name", "price", "category")), safe=False)
