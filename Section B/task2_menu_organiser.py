"""Section B - Task 2: Restaurant Menu Organiser.

A menu-management utility using nested dictionaries, list comprehensions,
the random module, and dictionary grouping to filter and analyze offerings.
"""

import random
from typing import Dict, List, Tuple, Any

# Menu stored as a dictionary mapping item name -> nested dict with 'price' and 'category'
MENU: Dict[str, Dict[str, Any]] = {
    "Tomato Basil Soup": {"price": 120, "category": "Starter"},
    "Paneer Tikka": {"price": 220, "category": "Starter"},
    "Veg Spring Rolls": {"price": 180, "category": "Starter"},
    "Veg Hyderabadi Biryani": {"price": 280, "category": "Main"},
    "Dal Makhani & Naan": {"price": 240, "category": "Main"},
    "Paneer Butter Masala": {"price": 260, "category": "Main"},
    "Warm Gulab Jamun": {"price": 90, "category": "Dessert"},
    "Chocolate Walnut Brownie": {"price": 150, "category": "Dessert"},
    "Mango Lassi": {"price": 80, "category": "Beverage"},
    "Fresh Lime Soda": {"price": 70, "category": "Beverage"},
}


def filter_by_budget(menu: Dict[str, Dict[str, Any]], budget: int) -> List[str]:
    """Uses list comprehension to produce a filtered list of item names priced below budget."""
    return [name for name, details in menu.items() if details["price"] < budget]


def get_chefs_pick(menu: Dict[str, Dict[str, Any]]) -> str:
    """Uses random.choice() to suggest one random item from the menu."""
    return random.choice(list(menu.keys()))


def group_and_display_categories(menu: Dict[str, Dict[str, Any]]) -> None:
    """Groups items by category using a loop and displays names and rounded average price."""
    categories: Dict[str, List[Tuple[str, int]]] = {}

    # Grouping using a loop
    for item_name, details in menu.items():
        cat = details["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((item_name, details["price"]))

    print("\n" + "=" * 50)
    print("           MENU GROUPED BY CATEGORY           ")
    print("=" * 50)

    for category, items in categories.items():
        total_price = sum(price for _, price in items)
        avg_price = total_price / len(items)
        print(f"\n[{category.upper()}] — Average Price: Rs {avg_price:.2f}")
        for item_name, price in items:
            print(f"  • {item_name:<30} Rs {price}")
    print("=" * 50)


def main() -> None:
    """Interactive execution of Task 2."""
    print("=" * 50)
    print("         DINEQUICK MENU ORGANISER & ANALYTICS ")
    print("=" * 50)

    # Prompt user for budget
    while True:
        try:
            budget_input = input("Enter your maximum budget in Rs (e.g., 200): ").strip()
            budget = int(budget_input)
            if budget < 0:
                print("[!] Please enter a positive number.")
                continue
            break
        except ValueError:
            print("[!] Invalid input. Please enter a whole number.")

    # 1. Budget Picks using list comprehension
    budget_picks = filter_by_budget(MENU, budget)
    print("\n" + "-" * 50)
    print(f"BUDGET PICKS (Items strictly below Rs {budget}):")
    if budget_picks:
        for pick in budget_picks:
            print(f"  ✔ {pick} (Rs {MENU[pick]['price']})")
    else:
        print("  (No items found below your budget.)")
    print("-" * 50)

    # 2. Chef's Pick of the Day using random.choice()
    chefs_pick = get_chefs_pick(MENU)
    print(f"\nCHEF'S PICK OF THE DAY: ⭐ {chefs_pick} (Rs {MENU[chefs_pick]['price']} - {MENU[chefs_pick]['category']})")

    # 3. Category grouping and averages
    group_and_display_categories(MENU)


if __name__ == "__main__":
    main()
