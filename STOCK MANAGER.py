
# stock_manager.py

# This dictionary stores all shop products.
inventory = {}


def set_stock(product, quantity, unit, threshold=5):
    """Set the current stock of a product."""

    product = product.lower()

    inventory[product] = {
        "quantity": quantity,
        "unit": unit,
        "threshold": threshold
    }

    return f"{product} stock set to {quantity} {unit}."


def add_stock(product, quantity, unit):
    """Add new stock to an existing product."""

    product = product.lower()

    if product not in inventory:
        return "Product not found. Set its stock first."

    if quantity <= 0:
        return "Quantity must be greater than zero."

    inventory[product]["quantity"] += quantity

    return f"Added {quantity} {unit} of {product}."


def record_sale(product, quantity):
    """Subtract sold products from stock."""

    product = product.lower()

    if product not in inventory:
        return "Product not found. Please record its stock first."

    if quantity <= 0:
        return "Sale quantity must be greater than zero."

    current = inventory[product]["quantity"]

    if quantity > current:
        return f"Not enough {product} in stock."

    inventory[product]["quantity"] -= quantity

    return f"Recorded sale of {quantity} {product}."


def set_threshold(product, threshold):
    """Change the low-stock warning level."""

    product = product.lower()

    if product not in inventory:
        return "Product not found."

    if threshold < 0:
        return "Threshold cannot be negative."

    inventory[product]["threshold"] = threshold

    return f"Low-stock threshold updated for {product}."


def get_low_stock():
    """Find products that need restocking."""

    low_stock = []

    for product, details in inventory.items():

        if details["quantity"] <= details["threshold"]:
            low_stock.append({
                "product": product,
                "quantity": details["quantity"],
                "unit": details["unit"],
                "threshold": details["threshold"]
            })

    return low_stock


def get_restock_list():
    """Arrange products according to restocking priority."""

    products = get_low_stock()

    # Products with the lowest stock compared to
    # their threshold receive the highest priority.
    products.sort(
        key=lambda item: (
            item["quantity"] / max(item["threshold"], 1)
        )
    )

    restock_list = []

    for item in products:
        restock_list.append({
            "product": item["product"],
            "current_stock": item["quantity"],
            "unit": item["unit"],
            "suggested_restock": max(
                0,
                (item["threshold"] * 2) - item["quantity"]
            )
        })

    return restock_list
