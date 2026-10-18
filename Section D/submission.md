# Section D — AI-Augmented Learning

**Assessment Code:** Python (M4-A1)  
**Track:** M4 — DB and Python Framework  
**Topic:** AI-Assisted Development, Automated Code Evaluation & Defensive Debugging  

---

## 1. Exact Prompt Given to the AI Tool

> "Write a Django view function that:
> 1. Accepts a GET request at `/api/menu/<restaurant_id>/` and returns a JSON list of available menu items (`name`, `price`, `category`) for that restaurant using Django ORM and `JsonResponse`.
> 2. Requires the requesting user to be authenticated; returns a JSON response with status 403 and the exact message `{'message': 'Authentication required'}` for unauthenticated requests instead of redirecting.
> 3. Filters only items where `available=True` and, if a `max_price` query parameter is provided, only items whose price is less than or equal to that value.
> 4. Handles the case where the given `restaurant_id` does not exist, returning a JSON 404 response with a descriptive error message rather than raising an unhandled `DoesNotExist` exception.
> Use the models from DineQuick (`Restaurant` and `MenuItem`)."

---

## 2. Code Comparison

### A. AI Tool's Original Code (`api_view_original.py`)
```python
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
```

### B. Corrected & Hardened Version (`api_view_corrected.py`)
```python
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from orders.models import MenuItem, Restaurant

@require_GET
def restaurant_menu_api(request, restaurant_id):
    # 1. Enforce authentication; return JSON 403 (no redirect)
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Authentication required"}, status=403)

    # 2. Safely query restaurant; return descriptive JSON 404 on DoesNotExist
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse(
            {"error": f"Restaurant with ID {restaurant_id} was not found."}, 
            status=404
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
                status=400
            )
        items = items.filter(price__lte=max_price)

    # 5. Extract requested fields and serialize
    data = list(items.values("name", "price", "category"))
    return JsonResponse(data, safe=False)
```

---

## 3. Test & Debug Note (What Was Changed and Why)

The AI’s original solution failed to sanitize the `max_price` query parameter, blindly passing raw string input into the ORM filter `price__lte=request.GET["max_price"]`. When a client passes non-numeric values (e.g. `?max_price=abc` or `?max_price=NaN`), the database adapter crashes with an unhandled `InvalidOperation` or `ValueError`, returning an internal server error (HTTP 500) rather than a clean client error. 

To fix this:
1. I introduced defensive `Decimal` conversion wrapped in exception handling to return a descriptive `HTTP 400 Bad Request` whenever `max_price` is malformed, negative, or infinite (`NaN`/`Infinity`).
2. I sanitized string whitespace with `.strip()` and retained `@require_GET` to reject unsupported HTTP methods with `405 Method Not Allowed`.
3. I wrote automated unit tests in `orders/tests.py` verifying all edge cases: unauthenticated `403`, missing restaurant `404`, valid `max_price` filtering, and malformed `max_price` `400`.
