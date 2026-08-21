"""
=============================================================================
BIT2083 FUNDAMENTAL OF COMPUTATIONAL THINKING: PYTHON
ASSIGNMENT 2: RESTAURANT ORDERING SYSTEM (MODULAR COMPONENT 1)
File: menu_data.py
Description: Contains restaurant configuration settings, categorized menu data,
             promotional discount codes, and tax parameters.
=============================================================================
"""

# Restaurant Metadata and Financial Parameters
RESTAURANT_NAME = "CITADEL GOURMET BISTRO"
RESTAURANT_TAGLINE = "Authentic Taste, Exceptional Quality"
RESTAURANT_LOCATION = "Cyberjaya Campus, City University Malaysia"
SST_RATE = 0.06           # 6% Sales & Services Tax (Malaysian SST)
SERVICE_CHARGE_RATE = 0.10 # 10% Service Charge
MEMBER_DISCOUNT_RATE = 0.10 # 10% Loyalty Member Discount

# Valid Promotional Discount Codes (Code: Percentage / Fixed Deduction)
PROMO_CODES = {
    "CITYU15": {"type": "percent", "value": 0.15, "desc": "15% City University Special Discount"},
    "SAVER10": {"type": "percent", "value": 0.10, "desc": "10% Smart Saver Promo"},
    "WELCOME5": {"type": "fixed", "value": 5.00, "desc": "RM 5.00 Welcome Voucher"}
}

# Categorized Restaurant Menu Catalog
# Structure: Dictionary with Item Code as unique key
MENU = {
    # --- Appetizers ---
    "A01": {"name": "Crispy Spring Rolls (4 pcs)", "category": "Appetizers", "price": 8.50, "description": "Vegetable spring rolls served with sweet chili dip"},
    "A02": {"name": "Chicken Satay (6 skewers)", "category": "Appetizers", "price": 12.00, "description": "Grilled marinated chicken skewers with peanut sauce"},
    "A03": {"name": "Mushroom Garlic Bruschetta", "category": "Appetizers", "price": 9.50, "description": "Toasted baguette topped with sauteed garlic mushrooms"},

    # --- Main Courses ---
    "M01": {"name": "Signature Nasi Lemak Royal", "category": "Main Courses", "price": 15.90, "description": "Fragrant coconut rice with spiced fried chicken, sambal & egg"},
    "M02": {"name": "Char Kway Teow Special", "category": "Main Courses", "price": 13.50, "description": "Wok-fried flat rice noodles with fresh prawns and cockles"},
    "M03": {"name": "Grilled Chicken Chop with Black Pepper", "category": "Main Courses", "price": 18.90, "description": "Juicy chicken chop served with fries and garden salad"},
    "M04": {"name": "Citadel Beef Burger & Fries", "category": "Main Courses", "price": 21.00, "description": "Handcrafted beef patty with cheddar cheese and brioche bun"},
    "M05": {"name": "Creamy Seafood Carbonara", "category": "Main Courses", "price": 19.50, "description": "Fettuccine pasta with squid, prawns in rich parmesan sauce"},

    # --- Beverages ---
    "B01": {"name": "Teh Tarik Special (Iced/Hot)", "category": "Beverages", "price": 3.80, "description": "Traditional frothy Malaysian pulled milk tea"},
    "B02": {"name": "Iced Lemon Tea", "category": "Beverages", "price": 4.50, "description": "Refreshing black tea with fresh lemon slices"},
    "B03": {"name": "Fresh Orange Juice", "category": "Beverages", "price": 6.50, "description": "100% freshly squeezed pure orange juice"},
    "B04": {"name": "Artisan Caramel Latte", "category": "Beverages", "price": 9.90, "description": "Espresso with steamed milk and caramel drizzle"},

    # --- Desserts ---
    "D01": {"name": "Classic Cendol Durian", "category": "Desserts", "price": 8.00, "description": "Shaved ice with pandan jelly, coconut milk and gula melaka"},
    "D02": {"name": "Warm Molten Lava Cake", "category": "Desserts", "price": 12.50, "description": "Rich chocolate lava cake served with vanilla gelato"},
    "D03": {"name": "New York Baked Cheesecake", "category": "Desserts", "price": 10.50, "description": "Creamy cheesecake slice topped with strawberry compote"}
}
