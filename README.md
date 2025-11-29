# 🌍 Autonomous Sustainability Research Agent

An AI-powered multi-agent system that performs parallel research on sustainable technologies and synthesizes a professional report. Built using **Google Gemini 2.0 Flash**, the **Google Agent Development Kit (ADK)**, and **Streamlit**.

## 🚀 Key Features

* **Parallel Execution:** Runs three specialized research agents simultaneously (Renewable Energy, EVs, Carbon Capture) to speed up information gathering.
* **Structured Synthesis:** A dedicated synthesis agent combines findings into a cohesive, non-hallucinated report.
* **Dynamic UI:** A clean web interface built with Streamlit.
* **State Management:** Uses session-based memory to isolate user data.

## 🏗️ Architecture

The system uses a **Parallel-then-Sequential** workflow:

1.  **User Input:** Defines the research scope.
2.  **Phase 1 (Parallel):**
    * 🤖 **Agent A:** Researches Renewable Energy.
    * 🤖 **Agent B:** Researches Electric Vehicles.
    * 🤖 **Agent C:** Researches Carbon Capture.
3.  **Phase 2 (Sequential):**
    * 📝 **Writer Agent:** Collects all summaries from Phase 1 and compiles a final formatted report.

## 🛠️ Prerequisites

* **Python 3.10** or higher (Required for Google ADK).
* A **Google Cloud API Key** (from [Google AI Studio](https://aistudio.google.com/)).

## 📦 Installation

1.  **Clone or Download this repository:**
    ```bash
    git clone https://github.com/Sagar-Hatankar/sustainability-agent.git
    cd sustainability-agent
    ```

2.  **Create a Virtual Environment:**
    * *Windows:*
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * *Mac/Linux:*
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If the install hangs, try using `uv pip install -r requirements.txt`)*

## 🔑 Configuration

1.  Create a file named `.env` in the root directory.
2.  Add your Google API key inside it. Do not use quotes or spaces around the `=` sign.

**File: `.env`**
```env
GOOGLE_API_KEY=AIzaSyYourKeyHere...
GEMINI_MODEL=gemini-2.0-flash