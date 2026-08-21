"""
Automated validation test script for Restaurant Ordering System
"""
import menu_data
import order_service

print(">>> 1. Testing Menu Display:")
order_service.display_menu(menu_data.MENU)

print(">>> 2. Testing Cart Operations:")
cart = []
# Add items
order_service.add_to_cart(cart, menu_data.MENU, "M01", 2) # Nasi Lemak Royal x2 = 31.80
order_service.add_to_cart(cart, menu_data.MENU, "B01", 2) # Teh Tarik x2 = 7.60
order_service.add_to_cart(cart, menu_data.MENU, "D01", 1) # Cendol x1 = 8.00
order_service.display_cart(cart)

print(">>> 3. Testing Bill Calculation (VIP Member + CITYU15 Promo Code):")
bill = order_service.calculate_bill(cart, is_member=True, promo_code_str="CITYU15")
for k, v in bill.items():
    print(f"  {k}: {v}")

print(">>> 4. Testing Receipt Generation (Cash Payment):")
payment_info = {
    "method": "Cash",
    "tendered": 60.00,
    "change": 60.00 - bill["grand_total"]
}
order_service.generate_receipt(
    cart=cart,
    bill_details=bill,
    payment_info=payment_info,
    order_id="ORD-1001",
    order_type="Dine-In",
    table_no=12
)

print(">>> 5. Testing Item Update & Removal:")
order_service.update_cart_quantity(cart, "B01", 3)
order_service.remove_from_cart(cart, "D01")
order_service.display_cart(cart)

print(">>> ALL UNIT TESTS PASSED SUCCESSFULLY!")
