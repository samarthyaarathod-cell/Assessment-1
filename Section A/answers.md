# Section A: Concept Application — Comprehensive Solutions & Technical Analysis

**Assessment Code:** Python (M4-A1)  
**Track:** M4 — DB and Python Framework  
**Stack:** Python 3 / Django  

---

## S1 | Scenario: Order-Cart Filtering & Memory Efficiency

### Problem Breakdown
You have a cart containing 200 items stored as a list of tuples: `[(item_name, price), ...]`. In a **single pass**, you must:
1. Display only items priced above Rs 150.
2. Count the qualifying items.
3. Calculate their subtotal.
Compare using a direct `for` loop versus slicing first, and determine which is more memory-efficient.

### Direct `for` Loop Implementation
```python
def process_cart_direct(cart: list[tuple[str, float]], threshold: float = 150.0):
    qualifying_count = 0
    subtotal = 0.0

    # Single pass iteration directly over the list
    for name, price in cart:
        if price > threshold:
            print(f"- {name}: Rs {price:.2f}")
            qualifying_count += 1
            subtotal += price

    return qualifying_count, subtotal
```

### Comparative Analysis: Direct Loop vs. List Slicing

| Evaluation Metric | Direct `for` Loop (`for item in cart`) | List Slicing (`cart[start:stop]`) |
| :--- | :--- | :--- |
| **Pass Count** | **Single pass ($O(n)$)** — filters, prints, and accumulates simultaneously. | **Two passes required** — slice creation first, then loop over the slice. |
| **Time Complexity** | **$O(n)$** where $n = 200$. Exactly 200 iterations. | **$O(k) + O(k)$** to copy and iterate (where $k$ is slice length). |
| **Auxiliary Memory** | **$O(1)$ constant space**. Only scalar accumulators (`count`, `subtotal`) are maintained. | **$O(k)$ linear space**. Allocates a new list in heap memory holding references. |
| **Filtering Feasibility**| Filters items based on condition (`price > 150`) dynamically. | **Cannot filter conditionally**. Slicing only selects fixed index ranges (`cart[0:50]`). |

### Why Direct Iteration is More Memory-Efficient
1. **Zero Intermediate Allocation:** A direct `for` loop utilizes Python’s iterator protocol (`iter(cart)` calling `__next__()`). It fetches a reference to each existing tuple in-place without creating any auxiliary data structures in memory. Auxiliary space is strictly $O(1)$.
2. **The Memory Penalty of Slicing:** In Python (CPython), slicing a list (`cart[:]` or `cart[0:k]`) creates a **new `PyListObject`** on the heap, allocating a contiguous array of $k$ pointers to the underlying tuple objects. For 200 items, slicing copies 200 64-bit object pointers (1.6 KB + list header overhead of ~56 bytes).
3. **Semantic Incompatibility:** Slicing operates solely on **indices**, not on **values** or predicate conditions. Slicing cannot determine which items are above Rs 150 unless the cart is pre-sorted by price (which would require an expensive $O(n \log n)$ sort).
4. **Conclusion:** Direct iteration is strictly superior in memory efficiency ($O(1)$ vs $O(n)$), execution speed (cache locality, single pass), and algorithmic correctness.

---

## S2 | Scenario: Nested Dictionary Comprehension for Analytics

### Problem Breakdown
Weekly sales data is stored as a nested dictionary:
- Outer key: Restaurant name (`str`)
- Inner value: Dictionary mapping dish names to units sold (`dict[str, int]`)
Requirement: A **single-line expression** yielding a flat list of all dishes sold by restaurants in Mumbai, and justification of list comprehension over nested loops for function arguments.

### Single-Line Expressions

#### Case 1: Restaurant metadata includes city (or lookup set exists)
Assuming a known set of Mumbai restaurant names `mumbai_restaurants = {"Spice Hub", "Curry Coast", "Coastal Treat"}`:
```python
mumbai_dishes = [
    dish 
    for rest_name, dishes in sales_data.items() 
    if rest_name in mumbai_restaurants 
    for dish in dishes
]
```

#### Case 2: If sales data dictionary embeds restaurant metadata
If each restaurant entry has `{"city": "Mumbai", "sales": {"Biryani": 40, "Pav Bhaji": 60}}`:
```python
mumbai_dishes = [
    dish 
    for rest_info in sales_data.values() 
    if rest_info.get("city") == "Mumbai" 
    for dish in rest_info.get("sales", {})
]
```

#### Deduplicated Variation (Set to List)
If unique dish names across all Mumbai branches are required:
```python
mumbai_unique_dishes = list({
    dish 
    for rest_name, dishes in sales_data.items() 
    if rest_name in mumbai_restaurants 
    for dish in dishes
})
```

### Why List Comprehension is Preferred Over Nested `for` Loops
1. **Expression vs. Statement (Composability):**
   - A list comprehension is a **first-class Python expression**. It evaluates directly to a list object, meaning it can be passed inline as an argument to another function (e.g., `process_dishes([dish for ...])` or `len([...])`).
   - Nested `for` loops are **statements**. They cannot be passed inline; you must declare an accumulator variable (`dishes = []`), execute multiple indented lines, and then pass the variable.
2. **Bytecode Optimization (CPython Performance):**
   - In Python 3, list comprehensions execute at C-level speed using the specialized `LIST_APPEND` bytecode instruction.
   - Traditional nested loops repeatedly look up and call `.append()` on the list object in Python VM space, incurring attribute lookup overhead on every iteration.
3. **Immutability and Readability:**
   - List comprehensions encourage functional, declarative programming: they describe *what* transformation is desired rather than *how* to step through indices, minimizing mutable state bugs.

---

## S3 | Scenario: OOP Modeling & Method Overriding for Delivery Partners

### Problem Breakdown
- Base class: `DeliveryPartner` (name, phone, active orders list).
- Subclass: `SeniorPartner` (additional `performance_score` affecting priority).
- Behavior: Senior partner’s `assign_order()` must log their score before assignment; base partner does not.
- Question: Justify inheritance over an optional field, and explain the problem method overriding solves.

### Python Code Architecture
```python
class DeliveryPartner:
    """Base delivery partner class handling common attributes and order management."""
    def __init__(self, name: str, phone: str):
        self.name = name
        self.phone = phone
        self.orders: list[str] = []

    def assign_order(self, order_id: str) -> None:
        self.orders.append(order_id)
        print(f"Order {order_id} assigned to partner {self.name}.")


class SeniorPartner(DeliveryPartner):
    """Specialized delivery partner with performance metrics and audit logging."""
    def __init__(self, name: str, phone: str, performance_score: float):
        super().__init__(name, phone)
        self.performance_score = float(performance_score)

    def assign_order(self, order_id: str) -> None:
        # Specialized behavior: log performance score to audit log
        print(f"[AUDIT LOG] Senior Partner {self.name} (Score: {self.performance_score:.2f}) assigned to order {order_id}.")
        # Reuse robust base implementation via super()
        super().assign_order(order_id)
```

### Justification: Inheritance vs. Optional Field (`performance_score = None`)

1. **Adherence to Single Responsibility & Open/Closed Principles (SOLID):**
   - A regular partner should not be burdened with attributes or business logic that only apply to senior tiers.
   - If an optional field is used on a single monolithic class, every consumer module must write defensive conditionals:
     ```python
     if partner.performance_score is not None:
         # Treat as senior partner
     ```
   - With inheritance, new partner tiers (e.g., `VIPPartner`, `TraineePartner`) can be added without modifying the stable base class.
2. **Preventing Invalid Domain States:**
   - An optional attribute allows semantic bugs: a partner could be marked "Senior" but have a `None` score, or a standard partner could accidentally have an invalid score assigned. Subclassing enforces required attributes in `__init__`.
3. **Liskov Substitution Principle (LSP):**
   - Anywhere the system expects a `DeliveryPartner`, a `SeniorPartner` can be passed seamlessly without breaking caller expectations.

### What Problem Method Overriding Solves
- **Polymorphism without Conditional Branching:**
  - Without method overriding, an order dispatcher would need type-inspection logic:
    ```python
    if isinstance(partner, SeniorPartner):
        log_senior_score(partner)
        partner.assign_order(order)
    else:
        partner.assign_order(order)
    ```
  - Method overriding solves this by binding the behavior dynamically at runtime based on the actual object type. Callers simply execute `partner.assign_order(order_id)`.
  - For standard partners, it cleanly appends the order; for senior partners, it logs the performance score and invokes `super().assign_order(order_id)` to complete the standard assignment workflow.

---

## S4 | Scenario: Robust Order-Log File Writer & Exception Hierarchy

### Problem Breakdown
DineQuick’s backend appends completed orders to `orders_log.txt`. Crashes occurred when:
1. File path did not exist.
2. Disk space ran out mid-write (`ENOSPC`).
Requirements: Restructure conceptually using `try`, `except`, and `finally`. Define a custom `DiskWriteError` wrapping `OSError`. Explain the purpose of `finally` and the business risk of silently swallowing exceptions.

### Implementation
```python
import os
from pathlib import Path

class DiskWriteError(Exception):
    """Custom exception raised when writing an order audit record to disk fails."""
    def __init__(self, message: str, original_error: Exception | None = None):
        super().__init__(message)
        self.original_error = original_error


def write_order_log(order_details: str, log_path: str = "orders_log.txt") -> None:
    """Safely appends an order entry to the audit log with guaranteed resource cleanup."""
    file_handle = None
    target_path = Path(log_path)

    try:
        # Guarantee directory existence to prevent FileNotFoundError
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Open in append mode with explicit UTF-8 encoding
        file_handle = open(target_path, mode="a", encoding="utf-8")
        file_handle.write(order_details + "\n")
        
        # Force write buffers to physically flush to the storage subsystem
        file_handle.flush()
        os.fsync(file_handle.fileno())

    except OSError as err:
        # Wrap system/OS error (e.g. No space left on device, permission denied)
        raise DiskWriteError(
            f"Failed to write order record to '{log_path}': {err.strerror or err}",
            original_error=err
        ) from err

    finally:
        # The finally block executes unconditionally
        if file_handle is not None and not file_handle.closed:
            file_handle.close()
```

### Critical Questions Answered

#### 1. What MUST go in the `finally` block?
- **File Descriptor Deallocation (`file_handle.close()`):**
  - Operating systems maintain a strict limit on open file descriptors per process (`RLIMIT_NOFILE` / `ulimit -n`).
  - If an exception occurs during `write()` (e.g., disk full) and `close()` is not called in `finally`, the file descriptor remains leaked in an uncollected state until garbage collection triggers.
  - The `finally` block guarantees that `file_handle.close()` executes regardless of whether the `try` block succeeds, raises an `OSError`, or encounters an unexpected interrupt.

#### 2. Why is silently swallowing exceptions (`except: pass`) dangerous in a billing context?
- **Phantom Financial Transactions:** A customer's credit card may be charged by the payment gateway, but if the local write fails silently, no audit log exists on the server.
- **Inability to Reconcile Ledgers:** Financial audits require non-repudiation logs. If billing discrepancies arise, engineers cannot verify order delivery or contents.
- **Data Inconsistency & False Success:** Downstream fulfillment workers will never see the order, causing delivery failures while the customer is billed.
- **Silent Cascading Outages:** Running out of disk space (`ENOSPC`) is a critical infrastructure alert. Swallowing the exception conceals the disk failure until the operating system or database crashes completely.

---

## S5 | Scenario: Django Database Layer & MVT Architecture Migration

### Problem Breakdown
Entities: `Restaurant`, `MenuItem`, and `Order`.
- Restaurant has many menu items.
- Order contains multiple menu items in varying quantities.
Questions:
1. Define Django relationships (`ForeignKey`, `ManyToManyField`, or through model) and justify each.
2. Explain why query logic belongs in the view rather than the template.
3. Detail the operational benefit of this separation when migrating from SQLite to MySQL.

### Django Model Architecture
```python
from django.db import models
from django.conf import settings

class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    class Category(models.TextChoices):
        STARTER = "Starter", "Starter"
        MAIN = "Main", "Main"
        DESSERT = "Dessert", "Dessert"
        BEVERAGE = "Beverage", "Beverage"

    # Many-to-One: Each MenuItem belongs to exactly one Restaurant
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE, 
        related_name="menu_items"
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=Category.choices)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


class Order(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="orders"
    )
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.PROTECT, 
        related_name="orders"
    )
    placed_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Many-to-Many relationship linked via an explicit intermediary through-model
    items = models.ManyToManyField(
        MenuItem, 
        through="OrderItem", 
        related_name="orders"
    )


class OrderItem(models.Model):
    """Intermediate 'through' model storing quantity and price snapshot at purchase time."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT, related_name="order_lines")
    quantity = models.PositiveIntegerField(default=1)
    
    # Financial snapshot: price of item at the moment of order
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def line_total(self) -> float:
        return self.quantity * self.unit_price
```

### Relationship Justifications
1. **`Restaurant` to `MenuItem` (`ForeignKey`, 1:N):**
   - Each menu item is owned by one restaurant. If a restaurant is deleted, cascading deletion (`on_delete=models.CASCADE`) safely removes its associated dishes.
2. **`Order` to `MenuItem` (`ManyToManyField` with `through="OrderItem"`, M:N):**
   - An order can contain multiple menu items, and a single menu item can appear across thousands of historical orders.
   - A plain `ManyToManyField` creates an internal joining table with only `order_id` and `menuitem_id`. However, real-world orders require **payload attributes on the relationship itself**: specifically `quantity` and `unit_price`.
   - **Crucial Pricing Snapshot:** If the restaurant updates a pizza price from Rs 250 to Rs 300 next week, historical order bills must NOT change. The through model stores the captured `unit_price` at the exact instant the transaction occurred.

### Why Query Logic Belongs in Views, Not Templates
1. **Separation of Concerns:** Django's Model-View-Template (MVT) pattern enforces clean decoupling. The Model defines data structures, the View encapsulates business/query logic, and the Template handles user presentation.
2. **Template Security and Sandboxing:** Django template language intentionally lacks arbitrary Python evaluation or database execution syntax. Allowing SQL or ORM queries inside templates would expose the presentation layer to data leaks, unauthorized access, and accidental cross-tenant data exposure.
3. **Prevention of the $N+1$ Query Problem:**
   - In views, developers optimize data access using `.select_related()` and `.prefetch_related()`.
   - If templates perform queries during rendering loops, they trigger hundreds of repetitive database queries ($N+1$), severely degrading response times.

### Operational Benefit During SQLite to MySQL Migration
- **Zero Template Refactoring:** Because templates receive prepared Python context dictionaries and QuerySets, switching databases from SQLite (`sqlite3`) to MySQL (`mysqlclient` / `PyMySQL`) in `settings.py` requires **0 modifications to template files**.
- **Dialect Abstraction:** Differences in SQL dialects (such as datetime handling, boolean representations, full-text indexing, or locking mechanisms like `SELECT FOR UPDATE`) are handled transparently by Django's database backend drivers in Python code.
- **Performance Tuning in a Single Layer:** Any database-specific tuning (indexes, transaction isolation levels, connection pooling) is managed exclusively in models and views without touching UI markup.

---

## S6 | Scenario: Query Optimization, Pagination, and Security Risks of Raw SQL

### Problem Breakdown
- Restaurant-admin order listing page.
- Requirements:
  1. Only show the admin’s own restaurant orders.
  2. Filter by status (`Preparing`, `Out for delivery`).
  3. Sort by placement time (most recent first).
  4. Paginate with 20 orders per page.
- Identify one security risk and one maintenance risk of raw SQL over Django ORM.

### Django ORM Query Chain & Pagination Implementation
```python
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest
from django.shortcuts import render
from .models import Order

def restaurant_orders_view(request: HttpRequest):
    # Retrieve page number from query params (e.g. ?page=2)
    page_number = request.GET.get("page", 1)
    
    # 1 & 2 & 3: Filter by tenant restaurant, status, and sort newest first
    # select_related avoids N+1 queries when rendering customer details
    orders_queryset = (
        Order.objects
        .filter(
            restaurant=request.user.restaurant,
            status__in=["Preparing", "Out for delivery"]
        )
        .select_related("customer")
        .order_by("-placed_at")
    )

    # 4: Paginate with 20 orders per page
    paginator = Paginator(orders_queryset, per_page=20)
    
    # get_page safely handles non-integer, negative, or out-of-range page numbers
    page_obj = paginator.get_page(page_number)

    return render(request, "admin/orders_list.html", {
        "page_obj": page_obj,
        "orders": page_obj.object_list,
    })
```

### Comparison: Django ORM vs. Raw SQL

#### 1. Security Risk: SQL Injection (SQLi)
- **The Danger of Raw SQL:**
  When a junior developer constructs raw SQL, they frequently use Python string formatting or f-strings:
  ```python
  # CRITICAL VULNERABILITY: SQL Injection
  status = request.GET.get("status")
  raw_sql = f"SELECT * FROM orders_order WHERE restaurant_id = {admin_rest_id} AND status = '{status}'"
  cursor.execute(raw_sql)
  ```
  An attacker can pass `status = "' OR '1'='1"` or `status = "'; DROP TABLE orders_order; --"`, bypassing tenant isolation or dropping database tables.
- **How Django ORM Protects You:**
  The ORM automatically parameterizes all inputs (`filter(status__in=...)`), passing query variables to the database engine separately via safe bind parameters (`%s` placeholders), rendering SQL injection impossible.

#### 2. Maintenance Risk: Schema Drift & Database Portability Loss
- **The Problem with Raw SQL:**
  - Raw SQL queries are hardcoded strings decoupled from Django’s schema migrations. If an engineer renames the field `placed_at` to `created_at` or updates foreign key table names, raw SQL queries fail at runtime with `OperationalError: no such column`.
  - Raw SQL ties your application to a specific SQL dialect (e.g., SQLite `LIMIT 20 OFFSET 40` vs Oracle/MSSQL pagination syntax).
- **How Django ORM Protects You:**
  - Django ORM uses Python attributes directly tied to models (`Order.objects.filter(...)`). Field renames can be caught with IDE static analysis, linters, and unit tests.
  - When migrating between databases (SQLite $\rightarrow$ PostgreSQL/MySQL), Django automatically compiles QuerySets into the correct target SQL dialect without modifying application code.

---
*End of Section A Solutions*
