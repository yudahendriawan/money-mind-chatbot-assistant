# Build MoneyMind: Your AI ChatBot Sidekick for Super Smart Spending! 💰 Tools: LLM Tools, OpenAI API, and Gradio

## Why MoneyMind? (The "Problem" & The "Magic")

Ever wonder where all your money goes? Poof! Gone like magic? 💸 You're not alone! Tracking expenses can feel like a chore, and who has time for endless spreadsheets?

Introduce **MoneyMind** – your personal AI finance assistant! No more guessing games; just tell it what you spent, and it'll keep track, check your balance, and even generate neat reports. Easy peasy!

But how does **MoneyMind** do it? Is it magic? Nope! It's powered by a super cool AI concept called 'Tools'. Think of it like giving our AI a special utility belt, packed with superpowers to actually do things, not just chat!

Here the examples of the AI that we want to build:

![alt text](<CleanShot 2025-06-03 at 07.30.14@2x.png>)

## Let's Get Started! 🧪 - Setting Up Your AI Lab

Before we dive into the code, let's get your workstation ready. Don't worry, it's quicker than brewing a perfect cup of coffee!

Here's what you'll need:
- Python 3: We'll be coding in Python, you can use any compiler such as Jupyter Notebook or Visual Studio Code.
- An OpenAI API Key: This is your AI's "brain power" key.

Step-by-step Setup (Fun & Simple):
1. **Python Power!**
    First off, you'll need Python installed. Most computers already have it, but if not, it's a quick download from [Python.org](python.org). We're using Python 3 for this project.

2. **Clone the Project and Create Virtual Environment** - Your Project's Cozy Corner
    It's like giving your project its own clean room, so its ingredients don't mix with other Python projects. Open your terminal or command prompt, navigate to where you want to create your project folder, and type:

    ```bash
    # Go to your project folder (or create one)
    mkdir moneymind_project
    cd moneymind_project

    # Clone the project 
    git clone https://github.com/yudahendriawan/money-mind-chatbot-assistant.git

    # Go to project 
    cd money-mind-chatbot-assistant

    # Create a virtual environment named 'venv'
    python -m venv venv

    # Activate it!
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

    You'll know it's activated when you see (`venv`) at the start of your command line!

3. **Installing Libraries** - Gathering Our AI Ingredients
    Now that your cozy corner is ready, let's get the Python libraries (like tools for our tools!) we need:

    ```bash
    pip install -r requirements.txt
    ```

    When you open the `requirements.txt`, you will see `openai, python-dotenv,` and `gradio` as the listed libraries you should install in order to run the `MoneyMind.py` code:

    - `openai`: This library lets your Python code talk to OpenAI's powerful AI models.

    - `python-dotenv`: Helps us load environment variables (like our secret API key) from a .env file.

    - `gradio`: This amazing library lets us create a beautiful, interactive web-based chat interface with just a few lines of Python!

4. **API Key Setup** - Your AI's Secret Handshake
    To make calls to OpenAI's super-smart models, you need a secret handshake: an API key! This key links your requests to your OpenAI account and handles billing (don't worry, these small interactions are usually very cheap).
    - **Get your key**: Head to the [OpenAI Platform](https://openai.com/api/) and create an account (if you don't have one). Once logged in, find your API keys under "API keys" in your settings (usually in the top right menu).
    - **Create a `.env` file**: In the very same `moneymind_project` folder where your Python script will be, create a new file named `.env` (yes, just `.env`!).
    - **Add your key**: Inside .env, add this line (replace your_openai_api_key_here with your actual key):

    ```bash
    OPENAI_API_KEY=your_openai_api_key_here
    ```

    **Super Important**: Never share this key with anyone or upload it to public code repositories (like GitHub) without proper security measures! The `.env` file keeps it safe locally.

5. **Running the Code** - Ready, Set, Go!
    Phew! You're all set up. Now, save the `MoneyMind` code (which I'll provide in the next section) as MoneyMind.py in your moneymind_project folder.

    Then, back in your activated terminal, run:

    ```bash
    python moneymind.py
    ```

    Gradio will start the web server and give you a local link (usually something like `http://127.0.0.1:7860`). Open that link in your web browser, and say hello to MoneyMind!

