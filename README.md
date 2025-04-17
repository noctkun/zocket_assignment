# AI Web Page Summarizer Agent

This project demonstrates an AI agent built with Python using AutoGen and Google Gemini to summarize the content of web pages. You provide a URL, and the application fetches the page's text, uses an AI agent to generate a summary, and displays both the extracted text and the summary via a Streamlit web interface.

## Features

*   Accepts a web page URL as input.
*   Fetches and cleans the main paragraph text content from the URL using `requests` and `BeautifulSoup`.
*   Utilizes an AutoGen `AssistantAgent` powered by Google Gemini (`gemini-1.5-pro`) to generate a concise summary.
*   Uses an AutoGen `UserProxyAgent` to manage the interaction flow.
*   Provides a simple web interface using Streamlit to input the URL and view the results.
*   Includes basic error handling for URL fetching and agent execution.

## Requirements

*   Python 3.8+
*   pip (Python package installer)
*   Internet access (for fetching URLs and contacting the Gemini API)
*   A Google Gemini API Key

## Setup and Installation

1.  **Clone or Download:** Get the project files onto your local machine.
    ```bash
    # If using Git
    git clone <repository_url>
    cd <repository_directory>

    # Or download and extract the ZIP file and navigate into the directory
    ```

2.  **Create a Virtual Environment:** It is highly recommended to use a virtual environment to avoid package conflicts.
    ```bash
    # Create the environment (use python3 if python points to Python 2)
    python -m venv venv

    # Activate the environment
    # On Linux/macOS:
    source venv/bin/activate
    # On Windows (Command Prompt):
    venv\Scripts\activate.bat
    # On Windows (PowerShell):
    venv\Scripts\Activate.ps1
    ```
    Your terminal prompt should now show `(venv)` at the beginning.

3.  **Install Dependencies:** Install the required Python packages.
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

## Configuration: Setting the API Key

This project requires a Google Gemini API key to function. You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

For ease of use in this specific demonstration project, the API key is hardcoded directly into the application file.

1.  **Open the file:** `app.py`
2.  **Locate the line:** Find the line near the top that looks like this:
    ```python
    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
    ```
3.  **Replace the placeholder:** Replace the entire string `"YOUR_GEMINI_API_KEY_HERE"` with your actual Google Gemini API key (ensure it remains within the quotes).
4.  **Save** the `app.py` file.

## Running the Application

1.  **Ensure Virtual Environment is Active:** If you haven't already, activate the virtual environment (see Step 2 in Installation).
2.  **Run Streamlit:** Execute the following command in your terminal from the project's root directory:
    ```bash
    streamlit run app.py
    ```
3.  **Access the Web App:** Streamlit will typically open the application automatically in your web browser, or it will provide a URL (usually `http://localhost:8501`) that you can navigate to.
4.  **Use the App:**
    *   Enter the full URL of the web page you want to summarize into the "Web Page URL" input field.
    *   Click the "Generate Summary" button.
    *   Wait while the application fetches the content and the AI agent generates the summary.
    *   The extracted content and the generated summary will be displayed on the page.


## NOTE: Hardcoded API Key

⚠️ **Important Security Consideration:** ⚠️

Please be aware that the Google Gemini API key is **intentionally hardcoded** directly within the `app.py` file in this project. This was done for simplified setup and execution in this particular instance, removing the need for environment variable configuration or other secrets management during testing/demonstration.

**This is NOT a recommended practice for production environments or any code that might be shared or committed to version control.** Exposing API keys directly in source code poses a significant security risk.
