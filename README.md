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
    MongoDB (or any other supported database)

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


1. **Create a `.env` file in the project root and set the required environment variables. Example:**

    ```plaintext
    api_token=
    BOT_SCRIPT_PATH=
    
    Database_name=
    Database_host=
    Database_password=
    Database_username=
    
    SMTP_SERVER= "smtp.gmail.com"
    SMTP_PORT= 587
    SENDER_EMAIL= ""
    SMTP_PASSWORD= ""
    ```

    Update the URLs based on your specific requirements.
# Fix not create record in table use orm 
    
    ```
    pip install --force-reinstall 'sqlalchemy<2.0.0'
    ```
