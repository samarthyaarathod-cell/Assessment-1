"""Section B - Task 3: Delivery Agent Manager with File Logging.

Demonstrates Object-Oriented Programming (OOP) inheritance, method overriding,
custom exception handling, and robust try-except-finally file operations.
"""

from datetime import datetime, timezone
from typing import List

LOG_FILENAME = "agents_log.txt"


class MaxOrdersExceeded(Exception):
    """Custom exception raised when an agent has reached the maximum of 5 active orders."""
    pass


class DeliveryAgent:
    """Base class modeling a standard delivery agent."""

    def __init__(self, name: str, phone: str):
        self.name: str = name
        self.phone: str = phone
        self.orders: List[str] = []

    def assign_order(self, order_id: str) -> str:
        """Assigns an order to the agent, enforcing the limit of active orders."""
        if len(self.orders) >= 5:
            raise MaxOrdersExceeded(
                f"Agent '{self.name}' already has {len(self.orders)} active orders (Maximum allowed: 5)."
            )
        self.orders.append(order_id)
        return f"Order '{order_id}' successfully assigned to Agent '{self.name}' (Active: {len(self.orders)}/5)."


class SeniorAgent(DeliveryAgent):
    """Subclass modeling a senior delivery agent with an audit-logged performance score."""

    def __init__(self, name: str, phone: str, performance_score: float):
        super().__init__(name, phone)
        self.performance_score: float = float(performance_score)

    def assign_order(self, order_id: str) -> str:
        """Overrides assign_order to display performance score before assigning."""
        print(f"[SENIOR AGENT DISPATCH] Senior Partner '{self.name}' Current Performance Score: {self.performance_score:.2f}")
        return super().assign_order(order_id)


def write_to_log(entry: str) -> None:
    """Appends an audit entry to agents_log.txt wrapped in try/except/finally."""
    file_handle = None
    try:
        file_handle = open(LOG_FILENAME, mode="a", encoding="utf-8")
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        file_handle.write(f"[{timestamp}] {entry}\n")
        file_handle.flush()
    except OSError as err:
        print(f"[ERROR] Failed to write to log file '{LOG_FILENAME}': {err}")
    finally:
        # The finally block strictly ensures the file handle is closed
        if file_handle is not None and not file_handle.closed:
            file_handle.close()


def process_order_assignment(agent: DeliveryAgent, order_id: str) -> None:
    """Handles order assignment, catches MaxOrdersExceeded separately, and logs the outcome."""
    try:
        success_msg = agent.assign_order(order_id)
        print(f"✔ {success_msg}")
        write_to_log(f"SUCCESS: {success_msg}")
    except MaxOrdersExceeded as exc:
        error_msg = str(exc)
        print(f"✖ [REJECTED] {error_msg}")
        # Log the error message to the file rather than crashing
        write_to_log(f"REJECTED: {error_msg}")


def main() -> None:
    """Interactive CLI runner for delivery agent management."""
    print("=" * 55)
    print("        DINEQUICK DELIVERY AGENT DISPATCHER         ")
    print("=" * 55)

    name = input("Enter Agent Name [Default: Arjun Sharma]: ").strip() or "Arjun Sharma"
    phone = input("Enter Phone Number [Default: +91 9876543210]: ").strip() or "+91 9876543210"
    
    agent = SeniorAgent(name=name, phone=phone, performance_score=4.85)
    print(f"\nInitialized Senior Agent: {agent.name} | Phone: {agent.phone} | Score: {agent.performance_score}")
    print("Enter Order IDs to assign (Max capacity: 5). Type 'done' to finish.\n")

    while True:
        order_id = input("Enter Order ID (or 'done'): ").strip()
        if order_id.lower() == "done":
            break
        if not order_id:
            print("[!] Please enter a non-empty order ID.")
            continue

        process_order_assignment(agent, order_id)

    print("\n" + "=" * 55)
    print(f"Final Active Orders for {agent.name}: {agent.orders}")
    print(f"Audit log saved to: {LOG_FILENAME}")
    print("=" * 55)


if __name__ == "__main__":
    main()
