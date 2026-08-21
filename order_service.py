"""
=============================================================================
BIT2083 FUNDAMENTAL OF COMPUTATIONAL THINKING: PYTHON
ASSIGNMENT 2: RESTAURANT ORDERING SYSTEM (MODULAR COMPONENT 2)
File: order_service.py
Description: Implements core computational business logic including menu display,
             cart management, tax & discount calculation, and receipt generation.
=============================================================================
"""

import datetime
from menu_data import (
    RESTAURANT_NAME,
    RESTAURANT_TAGLINE,
    RESTAURANT_LOCATION,
    SST_RATE,
    SERVICE_CHARGE_RATE,
    MEMBER_DISCOUNT_RATE,
    PROMO_CODES
)

def display_menu(menu):
    """
    Displays the entire categorized restaurant menu in a formatted tabular layout.
    Uses nested loops and formatting to present data clearly.
    """
    print("\n" + "=" * 78)
    print(f"{'*** ' + RESTAURANT_NAME + ' - FOOD & DRINK MENU ***':^78}")
    print(f"{RESTAURANT_TAGLINE:^78}")
    print("=" * 78)

    # Extract unique categories while maintaining order
    categories = []
    for item in menu.values():
        if item["category"] not in categories:
            categories.append(item["category"])

    for cat in categories:
        print(f"\n--- [ CATEGORY: {cat.upper()} ] ---")
        print(f"{'Code':<6} | {'Item Name':<35} | {'Price (RM)':<10} | {'Description'}")
        print("-" * 78)
        for code, details in menu.items():
            if details["category"] == cat:
                print(f"{code:<6} | {details['name']:<35} | RM {details['price']:>7.2f} | {details['description']}")
    print("=" * 78 + "\n")


def find_item(menu, item_code):
    """
    Case-insensitive search for an item in the menu dictionary by its code.
    Returns the item dictionary or None if not found.
    """
    code_upper = item_code.strip().upper()
    return menu.get(code_upper, None)


def add_to_cart(cart, menu, item_code, quantity):
    """
    Adds a specified quantity of a menu item into the customer's cart.
    Updates quantity if the item is already present in the cart.
    
    Parameters:
        cart (list): Current list of ordered item dictionaries.
        menu (dict): Complete menu dictionary.
        item_code (str): Item identification code.
        quantity (int): Number of portions to order.
    
    Returns:
        bool: True if successfully added, False otherwise.
    """
    code_upper = item_code.strip().upper()
    item_details = find_item(menu, code_upper)

    if not item_details:
        return False

    # Check if item is already in cart
    for cart_item in cart:
        if cart_item["code"] == code_upper:
            cart_item["quantity"] += quantity
            cart_item["subtotal"] = cart_item["quantity"] * cart_item["price"]
            return True

    # Add new item entry to cart list
    cart.append({
        "code": code_upper,
        "name": item_details["name"],
        "category": item_details["category"],
        "price": item_details["price"],
        "quantity": quantity,
        "subtotal": round(item_details["price"] * quantity, 2)
    })
    return True


def remove_from_cart(cart, item_code):
    """
    Removes an item completely from the shopping cart.
    """
    code_upper = item_code.strip().upper()
    for index, cart_item in enumerate(cart):
        if cart_item["code"] == code_upper:
            removed = cart.pop(index)
            return removed
    return None


def update_cart_quantity(cart, item_code, new_quantity):
    """
    Updates the quantity of an existing item in the cart.
    If new_quantity is 0, removes the item.
    """
    code_upper = item_code.strip().upper()
    if new_quantity <= 0:
        return remove_from_cart(cart, code_upper)

    for cart_item in cart:
        if cart_item["code"] == code_upper:
            cart_item["quantity"] = new_quantity
            cart_item["subtotal"] = round(cart_item["price"] * new_quantity, 2)
            return cart_item
    return None


def display_cart(cart):
    """
    Displays the current items in the cart with quantities and sub-totals.
    """
    if not cart:
        print("\n[!] Your order cart is currently empty.")
        return 0.0

    print("\n" + "=" * 70)
    print(f"{'CURRENT ORDER CART SUMMARY':^70}")
    print("=" * 70)
    print(f"{'No.':<4} | {'Code':<6} | {'Item Name':<30} | {'Qty':<5} | {'Price (RM)':<10} | {'Subtotal (RM)':<10}")
    print("-" * 70)

    total_units = 0
    raw_subtotal = 0.0
    for idx, item in enumerate(cart, 1):
        line_total = item["quantity"] * item["price"]
        raw_subtotal += line_total
        total_units += item["quantity"]
        print(f"{idx:<4} | {item['code']:<6} | {item['name']:<30} | {item['quantity']:<5} | RM {item['price']:>7.2f} | RM {line_total:>8.2f}")

    print("-" * 70)
    print(f"Total Items: {len(cart)} ({total_units} total portions) | Estimated Subtotal: RM {raw_subtotal:.2f}")
    print("=" * 70 + "\n")
    return raw_subtotal


def calculate_bill(cart, is_member=False, promo_code_str=""):
    """
    Performs complete financial computations:
    - Raw subtotal calculation
    - Membership discount (10%)
    - Promotional coupon code deduction
    - 10% Service Charge
    - 6% SST Government Tax
    - Final Grand Total
    
    Returns a comprehensive breakdown dictionary.
    """
    raw_subtotal = sum(item["quantity"] * item["price"] for item in cart)
    
    # 1. Member Discount
    member_discount = round(raw_subtotal * MEMBER_DISCOUNT_RATE, 2) if is_member else 0.0
    
    # 2. Promo Code Validation and Calculation
    promo_discount = 0.0
    promo_desc = "None"
    promo_code_clean = promo_code_str.strip().upper()
    
    if promo_code_clean in PROMO_CODES:
        promo_info = PROMO_CODES[promo_code_clean]
        promo_desc = promo_info["desc"]
        if promo_info["type"] == "percent":
            promo_discount = round(raw_subtotal * promo_info["value"], 2)
        elif promo_info["type"] == "fixed":
            promo_discount = min(raw_subtotal, promo_info["value"])

    total_discount = round(member_discount + promo_discount, 2)
    # Ensure total discount does not exceed raw subtotal
    total_discount = min(raw_subtotal, total_discount)

    taxable_amount = round(max(0.0, raw_subtotal - total_discount), 2)
    
    # 3. Service Charge (10%)
    service_charge = round(taxable_amount * SERVICE_CHARGE_RATE, 2)
    
    # 4. SST (6%)
    sst_amount = round(taxable_amount * SST_RATE, 2)
    
    # 5. Grand Total
    grand_total = round(taxable_amount + service_charge + sst_amount, 2)

    return {
        "raw_subtotal": raw_subtotal,
        "is_member": is_member,
        "member_discount": member_discount,
        "promo_code": promo_code_clean if promo_code_clean in PROMO_CODES else "N/A",
        "promo_desc": promo_desc,
        "promo_discount": promo_discount,
        "total_discount": total_discount,
        "taxable_amount": taxable_amount,
        "service_charge": service_charge,
        "sst_amount": sst_amount,
        "grand_total": grand_total
    }


def generate_receipt(cart, bill_details, payment_info, order_id, order_type="Dine-In", table_no=1):
    """
    Generates and prints a professional, formatted tax invoice / customer receipt.
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    receipt_lines = []
    receipt_lines.append("\n" + "=" * 55)
    receipt_lines.append(f"{RESTAURANT_NAME:^55}")
    receipt_lines.append(f"{RESTAURANT_TAGLINE:^55}")
    receipt_lines.append(f"{RESTAURANT_LOCATION:^55}")
    receipt_lines.append("=" * 55)
    receipt_lines.append(f" INVOICE / RECEIPT: #{order_id}")
    receipt_lines.append(f" Date & Time      : {current_time}")
    receipt_lines.append(f" Order Type       : {order_type.upper()}")
    if order_type.lower() == "dine-in":
        receipt_lines.append(f" Table Number     : Table {table_no}")
    receipt_lines.append("-" * 55)
    receipt_lines.append(f"{'Item':<28} {'Qty':<4} {'Price':<8} {'Total':>10}")
    receipt_lines.append("-" * 55)

    for item in cart:
        item_total = item['quantity'] * item['price']
        name_trunc = item['name'][:26]
        receipt_lines.append(f"{name_trunc:<28} {item['quantity']:<4} {item['price']:>7.2f} {item_total:>10.2f}")

    receipt_lines.append("-" * 55)
    receipt_lines.append(f"{'Subtotal':<35}: RM {bill_details['raw_subtotal']:>10.2f}")

    if bill_details['is_member']:
        receipt_lines.append(f"{'VIP Member Discount (10%)':<35}:-RM {bill_details['member_discount']:>10.2f}")

    if bill_details['promo_discount'] > 0:
        receipt_lines.append(f"{'Promo (' + bill_details['promo_code'] + ')':<35}:-RM {bill_details['promo_discount']:>10.2f}")

    if bill_details['total_discount'] > 0:
        receipt_lines.append(f"{'Net Taxable Amount':<35}: RM {bill_details['taxable_amount']:>10.2f}")

    receipt_lines.append(f"{'Service Charge (10%)':<35}: RM {bill_details['service_charge']:>10.2f}")
    receipt_lines.append(f"{'Govt SST (6%)':<35}: RM {bill_details['sst_amount']:>10.2f}")
    receipt_lines.append("=" * 55)
    receipt_lines.append(f"{'GRAND TOTAL (MYR)':<35}: RM {bill_details['grand_total']:>10.2f}")
    receipt_lines.append("=" * 55)

    receipt_lines.append(f" Payment Method   : {payment_info['method'].upper()}")
    if payment_info['method'].lower() == "cash":
        receipt_lines.append(f" Cash Tendered    : RM {payment_info['tendered']:>10.2f}")
        receipt_lines.append(f" Change Due       : RM {payment_info['change']:>10.2f}")
    elif payment_info['method'].lower() in ["card", "duitnow qr", "e-wallet"]:
        receipt_lines.append(f" Transaction Ref  : {payment_info['ref_id']}")
        receipt_lines.append(f" Payment Status   : APPROVED / PAID")

    receipt_lines.append("-" * 55)
    receipt_lines.append(f"{'Thank you for dining with us!':^55}")
    receipt_lines.append(f"{'Please visit again soon!':^55}")
    receipt_lines.append("=" * 55 + "\n")

    receipt_output = "\n".join(receipt_lines)
    print(receipt_output)
    return receipt_output
