"""Section B - Task 1: Order Cart Calculator.

A console-based food ordering cart that utilizes lists, tuples, loops,
and functions to calculate orders with progressive GST tiers.
"""

from typing import List, Tuple

# At least 6 menu items stored as a list of tuples: (item_name, price)
MENU: List[Tuple[str, float]] = [
    ("Veg Burger", 120.0),
    ("Paneer Wrap", 180.0),
    ("Arbiata Pasta", 240.0),
    ("Crispy French Fries", 90.0),
    ("Margherita Pizza", 350.0),
    ("Chocolate Brownie", 110.0),
    ("Greek Green Salad", 160.0),
]


def calculate_total(cart: List[Tuple[str, float]]) -> float:
    """Iterates through the cart list and returns the sum of all item prices."""
    total: float = 0.0
    for item_name, price in cart:
        total += price
    return total


def display_menu() -> None:
    """Displays the available restaurant menu in a formatted table."""
    print("=" * 45)
    print("               DINEQUICK MENU                ")
    print("=" * 45)
    print(f"{'No.':<5} {'Item Name':<25} {'Price (Rs)':>10}")
    print("-" * 45)
    for number, (name, price) in enumerate(MENU, 1):
        print(f"{number:<5} {name:<25} {price:>10.2f}")
    print("=" * 45)


def print_order_summary(cart: List[Tuple[str, float]]) -> None:
    """Calculates tax tiers and prints a formatted order summary."""
    print("\n" + "=" * 45)
    print("                ORDER SUMMARY                ")
    print("=" * 45)

    if not cart:
        print("Cart is empty! No items were selected.")
        print("=" * 45)
        return

    # Print individual items
    print(f"{'Item':<30} {'Price (Rs)':>12}")
    print("-" * 45)
    for name, price in cart:
        print(f"{name:<30} {price:>12.2f}")
    print("-" * 45)

    base_total = calculate_total(cart)

    # Apply 5% GST if > Rs 300, 18% GST if > Rs 600
    if base_total > 600.0:
        gst_rate = 18
    elif base_total > 300.0:
        gst_rate = 5
    else:
        gst_rate = 0

    gst_amount = (base_total * gst_rate) / 100.0
    final_payable = base_total + gst_amount

    print(f"{'Base Total:':<30} Rs {base_total:>9.2f}")
    print(f"{f'GST Applied ({gst_rate}%):':<30} Rs {gst_amount:>9.2f}")
    print("=" * 45)
    print(f"{'FINAL PAYABLE AMOUNT:':<30} Rs {final_payable:>9.2f}")
    print("=" * 45)
    print("Thank you for ordering with DineQuick!\n")


def main() -> None:
    """Main interactive ordering loop."""
    cart: List[Tuple[str, float]] = []
    display_menu()

    print("\nInstructions:")
    print("- Enter the item number (1 to {}) to add an item to your cart.".format(len(MENU)))
    print("- Type 'done' when you have finished ordering.\n")

    while True:
        user_input = input("Choose item number or type 'done': ").strip()
        if user_input.lower() == "done":
            break

        try:
            item_num = int(user_input)
            if not 1 <= item_num <= len(MENU):
                print(f"[!] Invalid selection. Please enter a number between 1 and {len(MENU)}.")
                continue
            selected_item = MENU[item_num - 1]
            cart.append(selected_item)
            print(f" -> Added '{selected_item[0]}' (Rs {selected_item[1]:.2f}) to cart.")
        except ValueError:
            print("[!] Invalid input. Please enter a valid menu number or 'done'.")

    print_order_summary(cart)


if __name__ == "__main__":
    main()
