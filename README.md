# Telegram Bot for Personal Finance Management
This is a Python-based Telegram bot that helps users track their spending, income, and account balance. It provides various commands to record expenses, income, and retrieve financial information.

# Features
1. Record daily spending with notes
2. Record daily income with sources
3. Retrieve spending and income details for a specific date
4. Set and update user's name and email
5. Display user's account balance and personal information
6. Send spending details to the user's email
7. Track the number of messages sent in a chat
8. Log chat conversations

# Prerequisites
    Python 3.x
    Telegram bot API token (obtain it from @BotFather)

## Installation

1. **Clone the repository to your local machine:**

    ```bash
    git clone https://github.com/giauphan/botchat-telegram.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd botchat-telegram
    ```

3. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment:**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

5. **Install the project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

# Set up the environment variables:
    Create a .env file in the root directory
    Add your Telegram bot API token: api_token=YOUR_BOT_TOKEN
    Configure any other necessary environment variables (e.g., database connection)
# Usage
Run the bot:

```
python migration.py
python bot.py
```

# In Telegram, start a conversation with your bot and use the available commands:

    /start - Start the bot and receive a welcome message
    /help - Get a list of available commands
    /spending - Record daily spending with notes
    /expense <amount> <category> - Quickly record an expense with a category
    /get_spending - Retrieve spending details for a specific date
    /income - Record daily income with sources
    /get_income - Retrieve income details for a specific date
    /set_email - Set your email address
    /set_name - Set your name
    /show_info - Display your personal information and account balance
    /statistical - Get the number of messages you've sent in the chat
    /send_spending - Send your spending details to your registered email

Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

License
This project is licensed under the MIT License.

# Fix not create record in table use orm 
    
    ```
    pip install --force-reinstall 'sqlalchemy<2.0.0'
    ```
