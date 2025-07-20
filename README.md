# smart-chatbot-with-real-time-language-translator-


**Key Features:**

* **Multilingual Communication:** Supports chat in English, French, and Hindi.
* **Automatic Language Detection:** Detects the language of the user's input.
* **Real-time Translation:** Translates user messages to English for the chatbot's understanding and then translates the chatbot's English response back to the user's selected target language.
* **Google Gemini Integration:** Utilizes `gemini-2.0-flash` for efficient and accurate language processing and response generation.
* **Intuitive User Interface:** A clean and responsive web interface built with HTML and Tailwind CSS for a seamless chat experience.
* **Typing Indicator:** Provides a "Typing..." indicator to show when the bot is processing a response.

**Technical Stack:**

* **Backend:** Flask (Python)
    * Handles API requests for chat messages.
    * Integrates with the Google Gemini API.
    * Performs language detection and translation.
    * Manages communication with the Generative AI models.
* **Frontend:** HTML, CSS (Tailwind CSS), JavaScript
    * Provides the chat interface, message display, and language selection.
    * Communicates with the Flask backend to send user messages and receive bot responses.
* **Generative AI Model:** Google Gemini `gemini-2.0-flash`

**How it Works:**

1.  **User Input:** The user types a message in English, French, or Hindi and selects their desired response language from a dropdown.
2.  **Language Detection & Translation (Backend):**
    * The Flask backend receives the user's message.
    * It first detects the language of the incoming message using the `TRANSLATION_MODEL`.
    * If the detected language is not English, the message is translated into English for processing by the main chatbot model.
3.  **Chatbot Interaction (Backend):**
    * The English version of the user's message is sent to the `CHAT_MODEL` (Google Gemini) to generate a response.
4.  **Response Translation (Backend):**
    * The chatbot's English response is then translated into the user's chosen target language (English, French, or Hindi) using the `TRANSLATION_MODEL`.
5.  **Display to User (Frontend):** The final translated response is sent back to the frontend and displayed in the chat interface.

This project demonstrates a practical application of large language models for creating intelligent, multilingual conversational agents.
