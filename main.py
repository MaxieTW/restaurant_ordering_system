"""
=============================================================================
BIT2083 FUNDAMENTAL OF COMPUTATIONAL THINKING: PYTHON
ASSIGNMENT 2: RESTAURANT ORDERING SYSTEM (MODULAR COMPONENT 3 - MAIN DRIVER)
File: main.py
Description: Main entry point and interactive menu-driven interface for the
             Restaurant Ordering System. Handles user navigation, inputs,
             exception handling, order lifecycle, and payment processing.
=============================================================================
"""

import sys
import random
from menu_data import (
    MENU,
    RESTAURANT_NAME,
    PROMO_CODES
)
from order_service import (
    display_menu,
    find_item,
    add_to_cart,
    remove_from_cart,
    update_cart_quantity,
    display_cart,
    calculate_bill,
    generate_receipt
)

# Global Order History Tracker (for Session Statistics)
ORDER_HISTORY = []
CURRENT_ORDER_COUNTER = 1001


def print_banner():
    """Prints the main restaurant system header banner."""
    print("\n" + "=" * 70)
    print(f"{'*** ' + RESTAURANT_NAME + ' - DIGITAL POS SYSTEM ***':^70}")
    print(f"{'BIT2083 Computational Thinking: Python Project':^70}")
    print(f"{'City University Malaysia - Cyberjaya Campus':^70}")
    print("=" * 70)


def get_valid_integer(prompt, min_val=None, max_val=None):
    """
    Robust input validation function to safely retrieve integer values.
    Handles ValueError exceptions when the user enters non-numeric text.
    """
    while True:
        try:
            raw_input = input(prompt).strip()
            val = int(raw_input)
            if min_val is not None and val < min_val:
                print(f"[!] Error: Value cannot be less than {min_val}. Please try again.")
                continue
            if max_val is not None and val > max_val:
                print(f"[!] Error: Value cannot be greater than {max_val}. Please try again.")
                continue
            return val
        except ValueError:
            print("[!] Error: Invalid numeric input. Please enter a whole number.")


def get_valid_float(prompt, min_val=None):
    """
    Robust input validation function to safely retrieve decimal/currency values.
    """
    while True:
        try:
            raw_input = input(prompt).strip()
            val = float(raw_input)
            if min_val is not None and val < min_val:
                print(f"[!] Error: Value must be at least {min_val:.2f}. Please try again.")
                continue
            return val
        except ValueError:
            print("[!] Error: Invalid currency amount. Please enter a valid decimal number (e.g. 20.50).")


def get_yes_no(prompt):
    """
    Validates yes/no user inputs.
    """
    while True:
        choice = input(prompt).strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("[!] Error: Please enter 'y' for Yes or 'n' for No.")


def handle_add_item(cart):
    """Workflow to select items and add them to the cart."""
    display_menu(MENU)
    while True:
        item_code = input("\nEnter Item Code to order (e.g., M01, B01) or '0' to finish: ").strip().upper()
        if item_code == '0':
            break

        item = find_item(MENU, item_code)
        if not item:
            print(f"[!] Item code '{item_code}' not found in the menu. Please check the code and try again.")
            continue

        qty = get_valid_integer(f"Enter quantity for '{item['name']}' (Price: RM {item['price']:.2f}): ", min_val=1, max_val=50)
        add_to_cart(cart, MENU, item_code, qty)
        print(f"[+] Success: Added {qty}x '{item['name']}' to your cart.")
        
        more = get_yes_no("Would you like to add another item? (y/n): ")
        if not more:
            break


def handle_modify_cart(cart):
    """Workflow to view, change quantity, or remove items from the cart."""
    if not cart:
        print("\n[!] Your cart is empty. Nothing to modify.")
        return

    while True:
        display_cart(cart)
        if not cart:
            break

        print("Cart Management Options:")
        print("  1. Update Item Quantity")
        print("  2. Remove Item from Cart")
        print("  3. Clear Entire Cart")
        print("  4. Return to Main Menu")

        choice = get_valid_integer("Select an option (1-4): ", 1, 4)

        if choice == 1:
            code = input("Enter the Item Code to update: ").strip().upper()
            found = any(c['code'] == code for c in cart)
            if not found:
                print(f"[!] Item '{code}' is not currently in your cart.")
                continue
            new_qty = get_valid_integer("Enter new quantity (0 to remove): ", min_val=0, max_val=50)
            update_cart_quantity(cart, code, new_qty)
            print(f"[+] Quantity updated successfully.")
        elif choice == 2:
            code = input("Enter the Item Code to remove: ").strip().upper()
            removed = remove_from_cart(cart, code)
            if removed:
                print(f"[+] Removed '{removed['name']}' from cart.")
            else:
                print(f"[!] Item '{code}' not found in cart.")
        elif choice == 3:
            confirm = get_yes_no("Are you sure you want to clear all items in the cart? (y/n): ")
            if confirm:
                cart.clear()
                print("[+] Cart has been cleared.")
                break
        elif choice == 4:
            break


def handle_discounts(current_session):
    """Allows setting membership status and promotional voucher codes."""
    print("\n--- [ DISCOUNT & PROMOTIONS SETUP ] ---")
    current_session["is_member"] = get_yes_no("Is the customer a Citadel VIP Loyalty Member (10% Discount)? (y/n): ")
    if current_session["is_member"]:
        print("[+] VIP Member status applied!")

    has_promo = get_yes_no("Do you have a promotional discount voucher code? (y/n): ")
    if has_promo:
        print(f"Available Demo Codes: {', '.join(PROMO_CODES.keys())}")
        promo = input("Enter Promo Code: ").strip().upper()
        if promo in PROMO_CODES:
            current_session["promo_code"] = promo
            print(f"[+] Valid Promo Applied: {PROMO_CODES[promo]['desc']}")
        else:
            print("[!] Invalid promo code. No discount applied.")
            current_session["promo_code"] = ""
    else:
        current_session["promo_code"] = ""


def handle_checkout(cart, current_session):
    """Handles the billing, calculation, payment, and receipt generation."""
    global CURRENT_ORDER_COUNTER
    if not cart:
        print("\n[!] Cannot proceed to checkout: Cart is empty.")
        return False

    display_cart(cart)
    bill = calculate_bill(cart, current_session["is_member"], current_session["promo_code"])

    print("\n" + "=" * 50)
    print(f"{'BILLING SUMMARY BREAKDOWN':^50}")
    print("=" * 50)
    print(f"Subtotal                     : RM {bill['raw_subtotal']:>8.2f}")
    if bill['is_member']:
        print(f"VIP Member Discount (10%)    :-RM {bill['member_discount']:>8.2f}")
    if bill['promo_discount'] > 0:
        print(f"Promo Code ({bill['promo_code']})       :-RM {bill['promo_discount']:>8.2f}")
    if bill['total_discount'] > 0:
        print(f"Taxable Subtotal             : RM {bill['taxable_amount']:>8.2f}")
    print(f"Service Charge (10%)         : RM {bill['service_charge']:>8.2f}")
    print(f"Govt SST (6%)                : RM {bill['sst_amount']:>8.2f}")
    print("-" * 50)
    print(f"FINAL GRAND TOTAL            : RM {bill['grand_total']:>8.2f}")
    print("=" * 50)

    confirm = get_yes_no("\nProceed to payment processing? (y/n): ")
    if not confirm:
        print("[!] Payment canceled. Returning to main menu.")
        return False

    # Payment Methods
    print("\nSelect Payment Method:")
    print("  1. Cash")
    print("  2. Credit / Debit Card")
    print("  3. DuitNow QR / E-Wallet")
    
    pay_choice = get_valid_integer("Enter payment method choice (1-3): ", 1, 3)
    payment_info = {}

    if pay_choice == 1:
        payment_info["method"] = "Cash"
        while True:
            cash = get_valid_float(f"Grand Total is RM {bill['grand_total']:.2f}. Enter cash tendered: RM ", min_val=0.0)
            if cash < bill['grand_total']:
                diff = bill['grand_total'] - cash
                print(f"[!] Insufficient cash! Short by RM {diff:.2f}. Please provide enough cash.")
            else:
                change = cash - bill['grand_total']
                payment_info["tendered"] = cash
                payment_info["change"] = round(change, 2)
                break
    elif pay_choice == 2:
        payment_info["method"] = "Credit/Debit Card"
        payment_info["ref_id"] = f"CRD-{random.randint(100000, 999999)}"
        print(f"[+] Card payment approved! Authorization Ref: {payment_info['ref_id']}")
    elif pay_choice == 3:
        payment_info["method"] = "DuitNow QR / E-Wallet"
        payment_info["ref_id"] = f"DN-{random.randint(10000000, 99999999)}"
        print(f"[+] QR Scan detected. Payment approved! Ref: {payment_info['ref_id']}")

    # Generate Receipt
    order_id = f"ORD-{CURRENT_ORDER_COUNTER}"
    generate_receipt(
        cart=cart,
        bill_details=bill,
        payment_info=payment_info,
        order_id=order_id,
        order_type=current_session["order_type"],
        table_no=current_session["table_no"]
    )

    # Save to history
    ORDER_HISTORY.append({
        "order_id": order_id,
        "items_count": len(cart),
        "total_amount": bill["grand_total"],
        "payment_method": payment_info["method"]
    })
    CURRENT_ORDER_COUNTER += 1

    return True


def display_sales_statistics():
    """Displays manager/cashier daily sales statistics."""
    print("\n" + "=" * 60)
    print(f"{'DAILY SALES & ORDER STATISTICS':^60}")
    print("=" * 60)
    if not ORDER_HISTORY:
        print("[!] No completed orders recorded in this session yet.")
        print("=" * 60 + "\n")
        return

    total_revenue = sum(order["total_amount"] for order in ORDER_HISTORY)
    print(f"Total Completed Orders : {len(ORDER_HISTORY)}")
    print(f"Total Revenue Collected: RM {total_revenue:.2f}")
    print(f"Average Order Value    : RM {total_revenue / len(ORDER_HISTORY):.2f}")
    print("-" * 60)
    print(f"{'Order ID':<12} | {'Items':<8} | {'Method':<20} | {'Amount (RM)'}")
    print("-" * 60)
    for ord_record in ORDER_HISTORY:
        print(f"{ord_record['order_id']:<12} | {ord_record['items_count']:<8} | {ord_record['payment_method']:<20} | RM {ord_record['total_amount']:>8.2f}")
    print("=" * 60 + "\n")


def main():
    """Main execution loop for the Restaurant Ordering System."""
    print_banner()

    # Configure initial order session
    while True:
        current_session = {
            "order_type": "Dine-In",
            "table_no": 1,
            "is_member": False,
            "promo_code": ""
        }
        cart = []

        print("\n--- [ NEW CUSTOMER ORDER INITIALIZATION ] ---")
        print("Select Order Type:")
        print("  1. Dine-In")
        print("  2. Takeaway / Takeout")
        type_choice = get_valid_integer("Enter choice (1-2): ", 1, 2)
        if type_choice == 1:
            current_session["order_type"] = "Dine-In"
            current_session["table_no"] = get_valid_integer("Enter Table Number (1-50): ", 1, 50)
        else:
            current_session["order_type"] = "Takeaway"
            current_session["table_no"] = 0

        # Sub-loop for active customer order
        while True:
            print("\n" + "=" * 50)
            print(f"  ORDER #{CURRENT_ORDER_COUNTER} ({current_session['order_type']}) - MAIN MENU")
            print("=" * 50)
            print("  1. View Food & Beverage Menu")
            print("  2. Add Items to Cart")
            print("  3. View Current Cart Summary")
            print("  4. Modify / Remove Cart Items")
            print("  5. Apply Membership & Promo Codes")
            print("  6. Proceed to Checkout & Print Receipt")
            print("  7. Clear & Cancel Current Order")
            print("  8. View System Sales Report (Admin/Manager)")
            print("  9. Exit System")
            print("=" * 50)

            choice = get_valid_integer("Enter your choice (1-9): ", 1, 9)

            if choice == 1:
                display_menu(MENU)
            elif choice == 2:
                handle_add_item(cart)
            elif choice == 3:
                display_cart(cart)
            elif choice == 4:
                handle_modify_cart(cart)
            elif choice == 5:
                handle_discounts(current_session)
            elif choice == 6:
                success = handle_checkout(cart, current_session)
                if success:
                    print("\n[+] Order fulfilled successfully!")
                    break
            elif choice == 7:
                confirm = get_yes_no("Are you sure you want to cancel and discard the current order? (y/n): ")
                if confirm:
                    print("[-] Current order has been cancelled.")
                    break
            elif choice == 8:
                display_sales_statistics()
            elif choice == 9:
                print(f"\nThank you for using the {RESTAURANT_NAME} Ordering System.")
                print("System shutting down. Goodbye!")
                sys.exit(0)

        # Ask to handle another customer
        next_order = get_yes_no("\nWould you like to start an order for the next customer? (y/n): ")
        if not next_order:
            display_sales_statistics()
            print(f"\nThank you for using the {RESTAURANT_NAME} Ordering System.")
            print("System shutting down. Have a wonderful day!")
            break


if __name__ == "__main__":
    main()
