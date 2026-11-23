
# ai_assistant.py

import json
import os

from openai import OpenAI
from dotenv import load_dotenv


# Load the API key from .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# Instructions given to the AI.
INSTRUCTIONS = """
You are Duka Stock Advisor.

You help small shop owners manage their stock.

Understand the user's message and identify what
they want to do.

Available actions:

1. set_stock: Set the current quantity of a product.
2. add_stock: Add new stock to a product.
3. sale: Record products sold.
4. set_threshold: Change a low-stock warning level.
5. chat: General conversation or questions.

Rules:

- Extract the product name.
- Extract the quantity.
- Extract the unit when available.
- Do not invent quantities.
- If information is missing, use null.
- Never claim a stock update has happened.
  Python will perform the actual update.
- Be friendly and helpful.
"""


# JSON structure required from the AI.
ACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": [
                "set_stock",
                "add_stock",
                "sale",
                "set_threshold",
                "chat"
            ]
        },
        "product": {
            "type": ["string", "null"]
        },
        "quantity": {
            "type": ["integer", "null"]
        },
        "unit": {
            "type": ["string", "null"]
        },
        "reply": {
            "type": "string"
        }
    },
    "required": [
        "action",
        "product",
        "quantity",
        "unit",
        "reply"
    ],
    "additionalProperties": False
}


def ask_ai(user_message, history, inventory):
    """Ask AI to understand the user's message."""

    prompt = f"""
    Current inventory:
    {json.dumps(inventory)}

    Previous conversation:
    {json.dumps(history)}

    New user message:
    {user_message}

    Understand this message using the previous
    conversation and current inventory.

    Return the appropriate JSON action.
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=INSTRUCTIONS,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "stock_action",
                "strict": True,
                "schema": ACTION_SCHEMA
            }
        }
    )

    # Convert AI response into a Python dictionary.
    result = json.loads(response.output_text)

    # Check the response structure.
    required_fields = {
        "action",
        "product",
        "quantity",
        "unit",
        "reply"
    }

    if not isinstance(result, dict):
        raise ValueError("AI response must be a JSON object.")

    if set(result.keys()) != required_fields:
        raise ValueError("Invalid AI response fields.")

    if result["action"] not in [
        "set_stock",
        "add_stock",
        "sale",
        "set_threshold",
        "chat"
    ]:
        raise ValueError("Invalid action.")

    if not isinstance(result["reply"], str):
        raise ValueError("Invalid reply.")

    if result["product"] is not None:
        if not isinstance(result["product"], str):
            raise ValueError("Invalid product name.")

    if result["quantity"] is not None:
        if type(result["quantity"]) is not int:
            raise ValueError("Invalid quantity.")

    return result


def generate_summary(history, inventory, restock_list):
    """Make the final AI summary when the session ends."""

    prompt = f"""
    Summarize this shop owner's complete session.

    Conversation:
    {json.dumps(history)}

    Final inventory:
    {json.dumps(inventory)}

    Restocking list:
    {json.dumps(restock_list)}

    Include:
    - Products discussed
    - Sales recorded
    - Current stock situation
    - Products requiring restocking
    - Helpful recommendations

    Return a clear, useful summary.
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=(
            "You are Duka Stock Advisor. "
            "Write a concise and accurate shop report."
        ),
        input=prompt
    )

    return response.output_text

# ai_assistant.py

import json
import os

from openai import OpenAI
from dotenv import load_dotenv


# Load the API key from .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# Instructions given to the AI.
INSTRUCTIONS = """
You are Duka Stock Advisor.

You help small shop owners manage their stock.

Understand the user's message and identify what
they want to do.

Available actions:

1. set_stock: Set the current quantity of a product.
2. add_stock: Add new stock to a product.
3. sale: Record products sold.
4. set_threshold: Change a low-stock warning level.
5. chat: General conversation or questions.

Rules:

- Extract the product name.
- Extract the quantity.
- Extract the unit when available.
- Do not invent quantities.
- If information is missing, use null.
- Never claim a stock update has happened.
  Python will perform the actual update.
- Be friendly and helpful.
"""


# JSON structure required from the AI.
ACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": [
                "set_stock",
                "add_stock",
                "sale",
                "set_threshold",
                "chat"
            ]
        },
        "product": {
            "type": ["string", "null"]
        },
        "quantity": {
            "type": ["integer", "null"]
        },
        "unit": {
            "type": ["string", "null"]
        },
        "reply": {
            "type": "string"
        }
    },
    "required": [
        "action",
        "product",
        "quantity",
        "unit",
        "reply"
    ],
    "additionalProperties": False
}


def ask_ai(user_message, history, inventory):
    """Ask AI to understand the user's message."""

    prompt = f"""
    Current inventory:
    {json.dumps(inventory)}

    Previous conversation:
    {json.dumps(history)}

    New user message:
    {user_message}

    Understand this message using the previous
    conversation and current inventory.

    Return the appropriate JSON action.
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=INSTRUCTIONS,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "stock_action",
                "strict": True,
                "schema": ACTION_SCHEMA
            }
        }
    )

    # Convert AI response into a Python dictionary.
    result = json.loads(response.output_text)

    # Check the response structure.
    required_fields = {
        "action",
        "product",
        "quantity",
        "unit",
        "reply"
    }

    if not isinstance(result, dict):
        raise ValueError("AI response must be a JSON object.")

    if set(result.keys()) != required_fields:
        raise ValueError("Invalid AI response fields.")

    if result["action"] not in [
        "set_stock",
        "add_stock",
        "sale",
        "set_threshold",
        "chat"
    ]:
        raise ValueError("Invalid action.")

    if not isinstance(result["reply"], str):
        raise ValueError("Invalid reply.")

    if result["product"] is not None:
        if not isinstance(result["product"], str):
            raise ValueError("Invalid product name.")

    if result["quantity"] is not None:
        if type(result["quantity"]) is not int:
            raise ValueError("Invalid quantity.")

    return result


def generate_summary(history, inventory, restock_list):
    """Make the final AI summary when the session ends."""

    prompt = f"""
    Summarize this shop owner's complete session.

    Conversation:
    {json.dumps(history)}

    Final inventory:
    {json.dumps(inventory)}

    Restocking list:
    {json.dumps(restock_list)}

    Include:
    - Products discussed
    - Sales recorded
    - Current stock situation
    - Products requiring restocking
    - Helpful recommendations

    Return a clear, useful summary.
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=(
            "You are Duka Stock Advisor. "
            "Write a concise and accurate shop report."
        ),
        input=prompt
    )

    return response.output_text
