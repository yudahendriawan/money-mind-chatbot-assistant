# TODO --> add fitur for edit or delete expense or income

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from datetime import datetime, timedelta

# --- 1. Environment Setup and OpenAI Client ---
# Install: pip install openai python-dotenv gradio
load_dotenv(override=True) # Load .env file
MODEL = "gpt-4o-mini" # AI model
openai_client = OpenAI() # OpenAI client

# System message: AI's role and capabilities
system_message = """
    "You are MoneyMind, a polite and accurate finance assistant. I am capable of:\n"
    "- Recording expenses (e.g., 'Record 50000 for food: lunch', 'I bought clothes for 100000', 'Paid 20000 for coffee').\n"
    "- Recording income (e.g., 'Add 1000000 income from salary', 'I received 500000 from a freelance project').\n"
    "- Checking your balance (e.g., 'What's my balance?').\n"
    "- Generating transaction history reports (e.g., 'Show me food expenses this month', 'Report all transactions for 2024-05', or 'Show me all my transactions').\n"
    "At the beginning of each session, clearly state these capabilities.\n"
    "Always confirm actions. If unsure, say so politely. Be concise and helpful at all times.\n"
    "Be flexible in interpreting user requests to map them to the appropriate tool, even if phrasing isn't exact. Prioritize using tools when intent is clear.\n"
    "IMPORTANT: If a user's request contains multiple distinct expenses or income items (e.g., 'bought coffee and clothes'), call the 'record_expense' or 'record_income' tool separately for EACH item. Do not try to process multiple items in a single tool call.\n"
    "Please say that you don't know if you are asked something out of your capability as finance assistant such as three aboves"
"""

# --- 2. Simulated Database ---
# In real app, this would be a database.
transactions = []

# --- 3. Tool Definitions (Python Functions for AI) ---

def record_expense(amount: float, category: str, description: str):
    """Records an expense."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    transactions.append({
        "type": "expense",
        "amount": amount,
        "category": category.lower(),
        "description": description,
        "date": current_date
    })
    print(f"DEBUG: Expense recorded: {amount} for {category} ({description})")
    return f"An expense of Rp {amount:,.0f} for {category} ({description}) on {current_date} has been recorded."

def record_income(amount: float, category: str, description: str):
    """Records new income."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    transactions.append({
        "type": "income",
        "amount": amount,
        "category": category.lower(),
        "description": description,
        "date": current_date
    })
    print(f"DEBUG: Income recorded: {amount} from {category} ({description})")
    return f"Income of Rp {amount:,.0f} from {category} ({description}) on {current_date} has been recorded."

def check_balance():
    """Calculates current balance."""
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    balance = total_income - total_expense
    print(f"DEBUG: Current balance calculated: Rp {balance:,.0f}")
    return f"Your current balance is Rp {balance:,.0f}."

def get_transaction_report(category: str = None, period: str = None, transaction_type: str = None):
    """Generates a report of all transactions (income and expense) by category/period/type."""
    filtered_transactions = []
    current_date_obj = datetime.now()

    for t in transactions:
        include_transaction = True
        transaction_date_obj = datetime.strptime(t['date'], "%Y-%m-%d")

        # Filter by transaction type (income/expense)
        if transaction_type and t['type'] != transaction_type.lower():
            include_transaction = False

        # Filter by category (applies to both income and expense if type not specified)
        if category and t['category'] != category.lower():
            include_transaction = False

        # Filter by period
        if period:
            if period.lower() == "today":
                if transaction_date_obj.date() != current_date_obj.date():
                    include_transaction = False
            elif period.lower() == "this week":
                start_of_week_current = current_date_obj - timedelta(days=current_date_obj.weekday())
                start_of_week_transaction = transaction_date_obj - timedelta(days=transaction_date_obj.weekday())
                if start_of_week_transaction.date() != start_of_week_current.date():
                    include_transaction = False
            elif period.lower() == "this month":
                if transaction_date_obj.month != current_date_obj.month or transaction_date_obj.year != current_date_obj.year:
                    include_transaction = False
            elif "-" in period: # OSCE-MM or OSCE
                if len(period) == 7: # OSCE-MM
                    if not t['date'].startswith(period):
                        include_transaction = False
                elif len(period) == 4: # OSCE
                    if not t['date'].startswith(period):
                        include_transaction = False
            # If 'period' is provided but not recognized, it might fall through,
            # but the LLM should ideally pass a recognized format or None.
        
        if include_transaction:
            filtered_transactions.append(t)

    if not filtered_transactions:
        # Improved message for when no transactions are found, especially for 'all time'
        report_scope = ""
        if transaction_type:
            report_scope += transaction_type + "s"
        elif category:
            report_scope += category + " transactions"
        else:
            report_scope += "transactions"

        period_scope = ""
        if period:
            period_scope = f" during the period '{period}'"
        
        return f"No {report_scope} found{period_scope}."


    report_lines = [f"Transaction Report for {category if category else 'All Categories'} in Period {period if period else 'All Time'}:"]
    for trans in filtered_transactions:
        report_lines.append(f"- {trans['date']}: {trans['type'].capitalize()} Rp {trans['amount']:,.0f} ({trans['category']}) - {trans['description']}")
    
    # Calculate totals for income and expense separately for the report summary
    total_income_in_report = sum(t['amount'] for t in filtered_transactions if t['type'] == 'income')
    total_expense_in_report = sum(t['amount'] for t in filtered_transactions if t['type'] == 'expense')

    report_lines.append(f"--- Summary ---")
    report_lines.append(f"Total Income: Rp {total_income_in_report:,.0f}")
    report_lines.append(f"Total Expense: Rp {total_expense_in_report:,.0f}")
    report_lines.append(f"Net Change: Rp {(total_income_in_report - total_expense_in_report):,.0f}")


    print(f"DEBUG: Transaction report generated: {report_lines}")
    return "\n".join(report_lines)


# --- 4. Tool Descriptions for LLM ---

# 'record_expense' tool description
record_expense_desc = {
    "name": "record_expense",
    "description": "Records an expense. Use when user says 'buy', 'spent', 'record expense', 'paid', or 'add X for Y' where Y is an expense category (e.g., 'add 50000 for coffee'). If multiple distinct expenses are mentioned in one request, call this tool separately for each expense.",
    "parameters": {
        "type": "object",
        "properties": {
            "amount": {"type": "number", "description": "Amount spent."},
            "category": {"type": "string", "description": "Expense category (e.g., food, transport, clothes, entertainment, other)."},
            "description": {"type": "string", "description": "Brief expense description."}
        },
        "required": ["amount", "category", "description"],
        "additionalProperties": False
    }
}

# 'record_income' tool description
record_income_desc = {
    "name": "record_income",
    "description": "Records new income. Use when user says 'add income', 'received money', 'got paid', or 'income from X'. If multiple distinct income items are mentioned in one request, call this tool separately for each income item.",
    "parameters": {
        "type": "object",
        "properties": {
            "amount": {"type": "number", "description": "Amount of income."},
            "category": {"type": "string", "description": "Income category (e.g., salary, freelance, gift)."},
            "description": {"type": "string", "description": "Brief income description."}
        },
        "required": ["amount", "category", "description"],
        "additionalProperties": False
    }
}

# 'check_balance' tool description
check_balance_desc = {
    "name": "check_balance",
    "description": "Checks current money balance. Use when user asks about 'balance', 'money'.",
    "parameters": {"type": "object", "properties": {}, "additionalProperties": False}
}

# 'get_transaction_report' tool description
get_transaction_report_desc = {
    "name": "get_transaction_report",
    "description": "Generates a report of all transactions (income and expense). Can be filtered by category (optional), time period (optional: 'today', 'this week', 'this month', 'YYYY-MM', 'YYYY'), or transaction type (optional: 'income' or 'expense'). If no period or category is specified, it provides a full history of all transactions.",
    "parameters": {
        "type": "object",
        "properties": {
            "category": {"type": "string", "description": "Report category (optional).", "enum": ["food", "transportation", "entertainment", "shopping", "bills", "education", "health", "other", "salary", "freelance", "gift"]},
            "period": {"type": "string", "description": "Report period (optional).", "pattern": "^(today|this week|this month|\\d{4}(-\\d{2})?)$"},
            "transaction_type": {"type": "string", "description": "Type of transaction to report (optional: 'income' or 'expense').", "enum": ["income", "expense"]}
        },
        "required": [], # All parameters are optional for this report
        "additionalProperties": False
    }
}

# All available tools for the AI
tools_available = [
    {"type": "function", "function": record_expense_desc},
    {"type": "function", "function": record_income_desc},
    {"type": "function", "function": check_balance_desc},
    {"type": "function", "function": get_transaction_report_desc}
]

# --- 5. Handle Tool Calls ---

def handle_tool_call(llm_message_with_tool_calls): # Changed parameter name to reflect multiple calls
    """Executes AI-requested Python functions and returns all results."""
    tool_outputs = [] # List to store results from multiple tool calls

    for tool_call in llm_message_with_tool_calls.tool_calls: # Iterate through all tool calls
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print(f"DEBUG: AI wants tool: {function_name} with inputs: {arguments}")

        tool_result = None
        try:
            if function_name == "record_expense":
                amount = float(arguments.get('amount'))
                category = arguments.get('category')
                description = arguments.get('description')
                tool_result = record_expense(amount, category, description)
            elif function_name == "record_income":
                amount = float(arguments.get('amount'))
                category = arguments.get('category')
                description = arguments.get('description')
                tool_result = record_income(amount, category, description)
            elif function_name == "check_balance":
                tool_result = check_balance()
            elif function_name == "get_transaction_report":
                category = arguments.get('category')
                period = arguments.get('period')
                transaction_type = arguments.get('transaction_type')
                tool_result = get_transaction_report(category, period, transaction_type)
            else:
                print(f"ERROR: Unknown tool requested: {function_name}")
                tool_result = "Sorry, I don't recognize that command."
        except Exception as e:
            print(f"ERROR: Error running tool {function_name}: {e}")
            tool_result = f"Sorry, an error occurred: {e}"
        
        # Format tool output for AI and add to list
        tool_outputs.append({
            "role": "tool",
            "content": json.dumps({"result": tool_result}),
            "tool_call_id": tool_call.id # Crucial for matching outputs to calls
        })
    return tool_outputs # Return the list of all tool outputs

# --- 6. Main Chat Function ---

def chat(message, history):
    """Manages AI conversation and tool integration."""
    # 1. Prepare messages for first LLM call
    messages_for_llm = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]

    # 2. First LLM call: AI responds, aware of tools
    first_response = openai_client.chat.completions.create(
        model=MODEL,
        messages=messages_for_llm,
        tools=tools_available
    )

    # 3. Check if AI called a tool
    if first_response.choices[0].finish_reason == "tool_calls":
        print("DEBUG: AI decided to call a tool.")
        llm_tool_call_message = first_response.choices[0].message # This message contains ALL tool calls

        # Execute ALL tools and get ALL results
        tool_outputs = handle_tool_call(llm_tool_call_message) # Now expects and returns a list

        # 4. Append AI's tool request AND ALL tool outputs to history (CRUCIAL)
        messages_for_llm.append(llm_tool_call_message) # The message where LLM requested tools
        messages_for_llm.extend(tool_outputs) # Use extend() to add all outputs from the list

        # 5. Second LLM call: AI generates final response with all tool results
        final_response = openai_client.chat.completions.create(
            model=MODEL,
            messages=messages_for_llm
        )
        return final_response.choices[0].message.content
    else:
        # If no tool call, return first response
        print("DEBUG: AI did not call a tool this time.")
        return first_response.choices[0].message.content

# --- 7. Gradio Chat Interface ---
gr.ChatInterface(
    fn=chat,
    type="messages"
).launch(inbrowser=True)
