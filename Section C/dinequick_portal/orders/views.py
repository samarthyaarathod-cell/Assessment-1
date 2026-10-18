import logging
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from .forms import ProfileForm, RegistrationForm
from .models import CustomerProfile, MenuItem, Order, OrderItem, Restaurant

logger = logging.getLogger(__name__)


def restaurant_list(request):
    """Public view: Browse all partner restaurants and their cities."""
    restaurants = Restaurant.objects.all().order_by("name")
    return render(request, "orders/restaurant_list.html", {"restaurants": restaurants})


def restaurant_menu(request, pk):
    """Public view: Browse available menu items for a selected restaurant."""
    restaurant = get_object_or_404(Restaurant, pk=pk)
    items = restaurant.menu_items.filter(available=True).order_by("category", "name")

    # Group items by category for cleaner display
    categorized_items = {}
    for item in items:
        categorized_items.setdefault(item.category, []).append(item)

    return render(
        request,
        "orders/menu.html",
        {
            "restaurant": restaurant,
            "items": items,
            "categorized_items": categorized_items,
        },
    )


@login_required
@require_POST
def place_order(request, pk):
    """
    Authenticated order placement flow:
    1. Extracts selected items and quantities.
    2. Creates an Order linked to customer.
    3. Creates OrderItem records for each selected dish.
    4. Calculates total bill using Python logic before saving.
    5. Sends confirmation email using Django email backend.
    6. Appends log entry to orders_log.txt with try/except/finally.
    """
    restaurant = get_object_or_404(Restaurant, pk=pk)
    selected_quantities = {}

    try:
        for key, value in request.POST.items():
            if key.startswith("qty_"):
                qty = int(value)
                if qty > 0:
                    item_id = int(key.removeprefix("qty_"))
                    selected_quantities[item_id] = qty
    except (ValueError, TypeError):
        return HttpResponseBadRequest("Invalid item quantity provided.")

    if not selected_quantities:
        messages.error(request, "Please select at least one dish with quantity greater than zero.")
        return redirect("restaurant-menu", pk=pk)

    # Verify selected items belong to this restaurant and are available
    items = list(
        MenuItem.objects.filter(
            pk__in=selected_quantities.keys(),
            restaurant=restaurant,
            available=True,
        )
    )

    if len(items) != len(selected_quantities):
        messages.error(request, "Some selected dishes are no longer available.")
        return redirect("restaurant-menu", pk=pk)

    # Create Order and OrderItems in an atomic transaction
    with transaction.atomic():
        order = Order.objects.create(customer=request.user, restaurant=restaurant)

        # Python bill calculation logic
        calculated_total = Decimal("0.00")
        for item in items:
            qty = selected_quantities[item.pk]
            line_total = item.price * qty
            calculated_total += line_total

            OrderItem.objects.create(
                order=order,
                menu_item=item,
                quantity=qty,
                unit_price=item.price,
            )

        order.total = calculated_total
        order.save(update_fields=["total"])

    # 1. Send confirmation email
    send_order_confirmation_email(order, request.user.email)

    # 2. Append order log with try/except/finally
    log_order_to_file(order)

    messages.success(
        request,
        f"Order #{order.pk} successfully placed! Total payable: Rs {order.total:.2f}.",
    )
    return redirect("order-detail", pk=order.pk)


@login_required
def order_detail(request, pk):
    """Displays order confirmation and summary for the customer."""
    order = get_object_or_404(
        Order.objects.select_related("restaurant", "customer").prefetch_related("items__menu_item"),
        pk=pk,
        customer=request.user,
    )
    return render(request, "orders/order_detail.html", {"order": order})


def send_order_confirmation_email(order, recipient_email):
    """Sends confirmation email using Django's configured email backend."""
    if not recipient_email:
        return

    subject = f"DineQuick Order Confirmation — Order #{order.pk}"
    items_list = "\n".join(
        [f"- {line.menu_item.name} x {line.quantity} = Rs {line.line_total:.2f}" for line in order.items.all()]
    )
    message = (
        f"Dear {order.customer.get_full_name() or order.customer.username},\n\n"
        f"Thank you for ordering with DineQuick!\n"
        f"Your order from {order.restaurant.name} has been placed successfully.\n\n"
        f"Order ID: #{order.pk}\n"
        f"Order Status: {order.status}\n"
        f"Order Items:\n{items_list}\n\n"
        f"Total Bill: Rs {order.total:.2f}\n\n"
        f"We hope you enjoy your meal!"
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
    except Exception as exc:
        logger.warning(f"Could not deliver order confirmation email: {exc}")


def log_order_to_file(order):
    """Appends order details to orders_log.txt using explicit try/except/finally."""
    log_file_handle = None
    log_path = Path(settings.BASE_DIR) / "orders_log.txt"
    try:
        log_file_handle = open(log_path, mode="a", encoding="utf-8")
        entry = (
            f"order_id={order.pk} | "
            f"customer='{order.customer.username}' | "
            f"restaurant='{order.restaurant.name}' | "
            f"total=Rs {order.total:.2f} | "
            f"placed_at={order.placed_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        log_file_handle.write(entry)
        log_file_handle.flush()
    except OSError as exc:
        logger.error(f"Failed to append to orders_log.txt: {exc}")
    finally:
        # Guarantee file descriptor closure
        if log_file_handle is not None and not log_file_handle.closed:
            log_file_handle.close()


def register(request):
    """User registration view using Django's built-in authentication."""
    if request.user.is_authenticated:
        return redirect("restaurant-list")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to DineQuick, {user.first_name or user.username}! Your account has been created.")
            return redirect("restaurant-list")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    """Customer profile page with editable name, phone, and photo upload."""
    profile_obj, _ = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been successfully updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile_obj, user=request.user)

    recent_orders = (
        Order.objects.filter(customer=request.user)
        .select_related("restaurant")
        .prefetch_related("items__menu_item")
        .order_by("-placed_at")[:10]
    )

    return render(
        request,
        "orders/profile.html",
        {
            "form": form,
            "profile": profile_obj,
            "orders": recent_orders,
        },
    )


# ==============================================================================
# SECTION D API VIEW INTEGRATION
# ==============================================================================
@require_GET
def restaurant_menu_api(request, restaurant_id):
    """
    Section D GET API endpoint for /api/menu/<restaurant_id>/
    - Authenticated access required (returns 403 JSON instead of redirect).
    - Checks restaurant existence (returns 404 JSON).
    - Filters available=True.
    - Filters max_price if supplied (validates non-negative Decimal; returns 400 on error).
    """
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Authentication required"}, status=403)

    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse(
            {"error": f"Restaurant with ID {restaurant_id} was not found."},
            status=404,
        )

    items = MenuItem.objects.filter(restaurant=restaurant, available=True)

    if "max_price" in request.GET:
        try:
            max_price = Decimal(request.GET["max_price"])
            if not max_price.is_finite() or max_price < 0:
                raise InvalidOperation
        except (InvalidOperation, ValueError):
            return JsonResponse(
                {"error": "max_price must be a valid non-negative decimal value."},
                status=400,
            )
        items = items.filter(price__lte=max_price)

    data = list(items.values("name", "price", "category"))
    return JsonResponse(data, safe=False)
