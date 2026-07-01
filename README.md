# Notes to Flashcards
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?logo=google&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=white)

An AI-powered study tool that converts raw notes and files into customized flashcards, which can be exported directly to platforms like Quizlet and Knowt.

[![Live Demo](https://img.shields.io/badge/LIVE_APP-notes--to--flashcards--generator.streamlit.app-FF4B4B?style=for-the-badge&logo=streamlit)](https://notes-to-flashcards-generator.streamlit.app/)

---

## A Look Inside
![Notes to Flashcards Screenshot](./static/cover.png)

---

## Video Demo
[![Notes to Flashcards Demo](https://img.shields.io/badge/YouTube-Watch_Demo-FF0000?logo=youtube&style=for-the-badge)](https://youtu.be/O4EYNBXZeUk)

---

## Features
* **Import Your Notes:** Upload up to 3 TXT, PDF, or DOCX files at once. The app extracts all the information, text, and images.
* **Flashcard Modes:** Customize the output style (Terms & Definitions, Practice Test, Fill-in-the-Blank) and control the number of cards generated, or let the AI decide.
* **Deck Expansions:** Need more cards? Continuously generate new flashcards with the click of a button.
* **Exporting:** Instantly generate flashcard sets in different formats, ready to import into Quizlet, Knowt, and other study platforms.

## Tech Stack
* **Frontend:** ``Streamlit``
* **AI Model:** ``Google Gemini 3.1 Flash Lite``
* **Data Validation:** ``Pydantic``
* **Document Parsing:** ``pypdf`` and ``python-docx``

---

## Run it Locally

1. Clone the repository
    ```
    git clone https://github.com/git-ishaan-kumar/notes-to-flashcards.git
    ```

2. Install the required dependencies
    ```
    pip install -r requirements.txt
    ```

3. Setup your API key by creating a ``.env`` file in the root directory and adding your Google Gemini API key
    ```
    GEMINI_API_KEY="your_api_key_here"
    ```

4. Run the Streamlit app
    ```
    streamlit run app.py
    ```