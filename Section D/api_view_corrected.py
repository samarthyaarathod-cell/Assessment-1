from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from orders.models import MenuItem, Restaurant


@require_GET
def restaurant_menu_api(request, restaurant_id):
    """
    Returns a JSON list of available menu items for a restaurant.
    - Requires authentication (returns 403 JSON if anonymous).
    - Returns 404 JSON if restaurant does not exist.
    - Filters available=True.
    - Filters max_price if supplied (validates non-negative Decimal; returns 400 on error).
    """
    # 1. Enforce authentication; return JSON 403 (no redirect)
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Authentication required"}, status=403)

    # 2. Safely query restaurant; return descriptive JSON 404 on DoesNotExist
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse(
            {"error": f"Restaurant with ID {restaurant_id} was not found."},
            status=404,
        )

    # 3. Filter for available items
    items = MenuItem.objects.filter(restaurant=restaurant, available=True)

    # 4. Defensive query parameter validation for max_price
    if "max_price" in request.GET:
        raw_price = request.GET.get("max_price", "").strip()
        try:
            max_price = Decimal(raw_price)
            if not max_price.is_finite() or max_price < 0:
                raise InvalidOperation("Price must be a finite non-negative number.")
        except (InvalidOperation, ValueError):
            return JsonResponse(
                {"error": "Query parameter 'max_price' must be a valid non-negative decimal number."},
                status=400,
            )
        items = items.filter(price__lte=max_price)

    # 5. Extract requested fields and serialize
    data = list(items.values("name", "price", "category"))
    return JsonResponse(data, safe=False)
