🛒 Duka Stock Advisor
AI-Powered Smart Stock Management Assistant
1. Project Description

Duka Stock Advisor is an AI-powered chatbot developed using Python and the OpenAI API. It helps small shop owners manage inventory, record daily sales, monitor stock levels, and identify products that need restocking.

The assistant uses conversation memory to remember information shared by the shop owner during a session. It also generates low-stock alerts and a final restocking report.

2. Main Features
Stock Management: Record and update product quantities.
Sales Tracking: Record daily sales and automatically deduct sold quantities.
Conversation Memory: Remembers previous messages during a session.
Low-Stock Alerts: Warns shop owners when products reach their warning thresholds.
Restocking Priority: Creates a prioritized list of products that need restocking.
JSON Responses: Structures and validates AI responses.
Session Summary: Generates and saves a final conversation report.
3. Technologies Used
Python
OpenAI API
JSON
python-dotenv
4. Project Files
main.py – Runs the chatbot application.
stock_manager.py – Manages inventory and sales calculations.
ai_assistant.py – Connects the application to the OpenAI API.
requirements.txt – Contains the required Python packages.
.env – Stores the private OpenAI API key (not uploaded to GitHub).
.gitignore – Prevents private and unnecessary files from being uploaded.
reports/ – Stores generated conversation summaries.
5. Requirements
Python 3.10 or newer
An OpenAI API key
Internet connection
6. Installation and Setup
Step 1: Clone the repository
bash
git clone YOUR_GITHUB_REPOSITORY_URL


Replace the example with your actual GitHub repository URL.

Step 2: Open the project folder
bash
cd DukaStockAdvisor

Step 3: Install required packages
bash
pip install -r requirements.txt

Step 4: Set up the API key

Create a file named .env in the project folder.

Add:

env
OPENAI_API_KEY=your_openai_api_key_here


.

Step 5: Run the application
bash
python main.py


The chatbot will start in your terminal.

7. Example Usage

The shop owner can enter messages such as:

"I have 20 packets of sugar."
"I have 15 packets of rice."
"I sold 5 packets of sugar."
"How much sugar do I have left?"

To end the session and generate the final report, type:

text
exit

8. Project Team

Group Name: [Enter Your Group Name]

Group Members:

[Member 1 Name none]
[Member 2 Name none]
[Member 3 Name none]
[Member 4 Name none]
9. Project Purpose
Project Purpose
Duka Stock Advisor helps small shop owners improve inventory management, reduce stock shortages, monitor daily sales, and make better restocking decisions using artificial intelligence.

Duka Stock Advisor – Making Shop Management Smarter with AI.
Duka Stock Advisor helps small shop owners improve inventory management, reduce stock shortages, monitor daily sales, and make better restocking decisions using artificial intelligence.

Duka Stock Advisor – Making Shop Management Smarter with AI.
