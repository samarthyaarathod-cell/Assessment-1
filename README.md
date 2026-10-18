# Python Assessment (M4-A1) — Submission Portfolio

**Program:** Python  
**Assessment Code:** M4-A1  
**Module:** M4 — DB and Python Framework  
**Stack:** Python 3 / Django 5.2  

---

## Portfolio Structure & Component Map

| Section | Description | Location | Status |
| :--- | :--- | :--- | :--- |
| **Section A** | 6 Concept Application Real-World Scenarios | [`Section A/answers.md`](file:///d:/programming/Assessment/Assessment-1/Section%20A/answers.md) | Completed |
| **Section B — Task 1** | Order Cart Calculator (Tuples, GST, Loops) | [`Section B/task1_order_cart.py`](file:///d:/programming/Assessment/Assessment-1/Section%20B/task1_order_cart.py) | Completed & Tested |
| **Section B — Task 2** | Restaurant Menu Organiser (Dicts, Comprehensions, Random) | [`Section B/task2_menu_organiser.py`](file:///d:/programming/Assessment/Assessment-1/Section%20B/task2_menu_organiser.py) | Completed & Tested |
| **Section B — Task 3** | Delivery Agent Manager (OOP, Inheritance, Log Handling) | [`Section B/task3_delivery_agents.py`](file:///d:/programming/Assessment/Assessment-1/Section%20B/task3_delivery_agents.py) | Completed & Tested |
| **Section B — Task 4** | DineQuick Menu CRUD App (Django CBVs, Auth Mixin) | [`Section B/dinequick_crud/`](file:///d:/programming/Assessment/Assessment-1/Section%20B/dinequick_crud/) | Completed & 7 Tests Passing |
| **Section C** | DineQuick Full-Stack Food Ordering Portal (Mini Capstone) | [`Section C/dinequick_portal/`](file:///d:/programming/Assessment/Assessment-1/Section%20C/dinequick_portal/) | Completed & 9 Tests Passing |
| **Section D** | AI-Augmented Learning (Prompt, Comparison, Debug Note) | [`Section D/submission.md`](file:///d:/programming/Assessment/Assessment-1/Section%20D/submission.md) | Completed & Tested |

---

## Pre-configured Test Accounts

### Section B (`dinequick_crud`)
- **Admin Panel:** `http://127.0.0.1:8000/panel/`
- **Username:** `sam` | **Password:** *(Existing local superuser)*

### Section C (`dinequick_portal`)
- **Portal URL:** `http://127.0.0.1:8001/`
- **Admin Panel:** `http://127.0.0.1:8001/panel/`
- **Superuser:** `admin` | **Password:** `admin123`
- **Demo Customer:** `rahul_sharma` | **Password:** `customer123`

---

## Quick Start & Verification Instructions

### 1. Section B Console Programs
Run each script using Python 3:
```powershell
# Task 1: Order Cart Calculator
py "Section B/task1_order_cart.py"

# Task 2: Restaurant Menu Organiser
py "Section B/task2_menu_organiser.py"

# Task 3: Delivery Agent Manager & Log Writer
py "Section B/task3_delivery_agents.py"
```

### 2. Section B: DineQuick Menu CRUD Django App
```powershell
cd "Section B/dinequick_crud"
py manage.py migrate
py manage.py test menuapp      # Runs all 7 automated unit tests
py manage.py runserver 8000   # Accessible at http://127.0.0.1:8000/menu/
```

Key URLs:
- Menu Items List: `http://127.0.0.1:8000/menu/`
- Add Menu Item (Requires Login): `http://127.0.0.1:8000/menu/add/`
- Edit Menu Item: `http://127.0.0.1:8000/menu/<pk>/edit/`
- Delete Menu Item: `http://127.0.0.1:8000/menu/<pk>/delete/`
- Admin Panel: `http://127.0.0.1:8000/panel/`

### 3. Section C: DineQuick Full-Stack Food Ordering Portal
```powershell
cd "Section C/dinequick_portal"
py manage.py migrate
py manage.py seed_portal       # Seeds 4 restaurants, 24 menu items & accounts
py manage.py test orders       # Runs all 9 automated unit tests (including Section D)
py manage.py runserver 8001   # Accessible at http://127.0.0.1:8001/
```

Key URLs:
- Restaurant Listings (Public): `http://127.0.0.1:8001/`
- Restaurant Menu (Public Browse / Auth Order): `http://127.0.0.1:8001/restaurants/1/`
- Customer Registration: `http://127.0.0.1:8001/register/`
- Customer Sign In: `http://127.0.0.1:8001/accounts/login/`
- Customer Profile & Photo Upload: `http://127.0.0.1:8001/profile/`
- Section D JSON API: `http://127.0.0.1:8001/api/menu/1/?max_price=300`
- Jazzmin Admin Panel: `http://127.0.0.1:8001/panel/`

---

## Automated Test Results

Both Django applications contain complete unit test suites testing all security, validation, CRUD, pagination, and API requirements:
- **Section B (`menuapp`):** 7 / 7 tests passing.
- **Section C (`orders`):** 9 / 9 tests passing.
Total: **16 passed tests**.

---

## Submission Checklist for Assessor
- [x] **Section A:** In-depth written solutions covering all 6 technical scenarios with code examples, time/space complexity, and SOLID principles.
- [x] **Section B (Task 1):** Console cart calculator with iterative pricing and GST tiers.
- [x] **Section B (Task 2):** Menu organiser with list comprehension, random picks, and category averages.
- [x] **Section B (Task 3):** Delivery agent inheritance, custom `MaxOrdersExceeded` exception, and safe `try/except/finally` logging to `agents_log.txt`.
- [x] **Section B (Task 4):** Django CRUD app with 4 CBVs, `LoginRequiredMixin`, Bootstrap 5 inheritance, and pre-seeded database.
- [x] **Section C:** Full-stack portal with authentication, Django admin configuration, Python bill calculation, `orders_log.txt` logging, email backend, customer profile with photo upload, and pre-seeded database.
- [x] **Section D:** AI-augmented development documentation, original vs corrected view comparison, 3-4 line debug note, and live integration.
