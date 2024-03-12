# Botchat-telegram

# Setup

## Prerequisites

Before you start, ensure you have the following prerequisites installed on your machine:

- Python 3.x

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
