
# main.py

import json
import os
from datetime import datetime

from stock_manager import (
    inventory,
    set_stock,
    add_stock,
    record_sale,
    set_threshold,
    get_low_stock,
    get_restock_list
)

from ai_assistant import ask_ai, generate_summary


# Conversation memory.
conversation_history = []


def validate_response(data):
    """Check the JSON shown to the user."""

    required_fields = {
        "reply",
        "inventory",
        "low_stock",
        "success"
    }

    if not isinstance(data, dict):
        raise ValueError("Response must be a JSON object.")

    if set(data.keys()) != required_fields:
        raise ValueError("Response has missing or extra fields.")

    if not isinstance(data["reply"], str):
        raise ValueError("Reply must be text.")

    if not isinstance(data["inventory"], dict):
        raise ValueError("Inventory must be a dictionary.")

    if not isinstance(data["low_stock"], list):
        raise ValueError("Low stock must be a list.")

    if not isinstance(data["success"], bool):
        raise ValueError("Success must be true or false.")

    # Ensure the whole response can be converted to JSON.
    json.dumps(data)

    return data


def process_action(ai_result):
    """Execute the action selected by the AI."""

    action = ai_result["action"]
    product = ai_result["product"]
    quantity = ai_result["quantity"]
    unit = ai_result["unit"]

    if action == "chat":
        return ai_result["reply"], True

    if not product:
        return "Please specify the product name.", False

    if quantity is None or quantity <= 0:
        return "Please provide a valid positive quantity.", False

    if action == "set_stock":

        result = set_stock(
            product,
            quantity,
            unit or "units"
        )

    elif action == "add_stock":

        if product.lower() not in inventory:
            return "Product not found. Set its stock first.", False

        stored_unit = inventory[product.lower()]["unit"]

        result = add_stock(
            product,
            quantity,
            stored_unit
        )

    elif action == "sale":

        result = record_sale(product, quantity)

    elif action == "set_threshold":

        result = set_threshold(product, quantity)

    else:
        return "Sorry, I could not understand that action.", False

    # Error messages are returned without claiming success.
    if (
        result.startswith("Product not found")
        or result.startswith("Not enough")
        or result.startswith("Quantity must")
        or result.startswith("Sale quantity")
        or result.startswith("Threshold")
    ):
        return result, False

    return result, True


def make_response(reply, success):
    """Create and validate the JSON response."""

    response = {
        "reply": reply,
        "inventory": inventory,
        "low_stock": get_low_stock(),
        "success": success
    }

    return validate_response(response)


def save_summary():
    """Generate and save the final session report."""

    print("\nGenerating your final shop report...")

    restock_list = get_restock_list()

    summary = generate_summary(
        conversation_history,
        inventory,
        restock_list
    )

    os.makedirs("reports", exist_ok=True)

    filename = (
        "reports/summary_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".txt"
    )

    with open(filename, "w", encoding="utf-8") as file:

        file.write("DUKA STOCK ADVISOR REPORT\n")
        file.write("=========================\n\n")

        file.write("FINAL AI SUMMARY\n")
        file.write(summary + "\n\n")

        file.write("RESTOCKING PRIORITY LIST\n")
        file.write("------------------------\n")

        if restock_list:
            for number, item in enumerate(restock_list, 1):
                file.write(
                    f"{number}. {item['product']} - "
                    f"Current: {item['current_stock']} "
                    f"{item['unit']} - "
                    f"Suggested restock: "
                    f"{item['suggested_restock']} "
                    f"{item['unit']}\n"
                )
        else:
            file.write("No products currently need restocking.\n")

        file.write("\nFINAL INVENTORY\n")
        file.write(json.dumps(inventory, indent=4))

        file.write("\n\nCOMPLETE CONVERSATION\n")
        file.write(json.dumps(conversation_history, indent=4))

    print("\nYour report has been saved!")
    print("File:", filename)


def main():

    print("=" * 45)
    print("       DUKA STOCK ADVISOR")
    print("=" * 45)

    print("Welcome! I am your AI stock assistant.")
    print("Tell me your stock levels and daily sales.")
    print("Type 'exit' when you want to finish.")
    print("-" * 45)

    while True:

        user_message = input("\nShop Owner: ").strip()

        if not user_message:
            continue

        if user_message.lower() == "exit":

            try:
                save_summary()
                print("\nThank you for using Duka Stock Advisor!")
            except Exception as error:
                print("Could not save the report:", error)

            break

        try:

            # Send the message and memory to AI.
            ai_result = ask_ai(
                user_message,
                conversation_history,
                inventory
            )

            # Python performs the actual stock action.
            reply, success = process_action(ai_result)

            # Remember the conversation.
            conversation_history.append({
                "role": "user",
                "content": user_message
            })

            conversation_history.append({
                "role": "assistant",
                "content": reply
            })

            # Construct and validate JSON.
            final_response = make_response(
                reply,
                success
            )

            # Show JSON only after validation.
            print("\nDuka Stock Advisor:")
            print(json.dumps(final_response, indent=4))

            # Display a warning when stock is low.
            if final_response["low_stock"]:
                print("\nWARNING: Some products are running low!")

        except Exception as error:

            print("\nAn error occurred:", error)
            print("Please try again.")


if __name__ == "__main__":
    main()
