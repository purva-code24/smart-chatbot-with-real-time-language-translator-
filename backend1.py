from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

CORS(app)

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please set it in your .env file.")
genai.configure(api_key=gemini_api_key)                                                             ,

CHAT_MODEL = genai.GenerativeModel('gemini-2.0-flash')
TRANSLATION_MODEL = genai.GenerativeModel('gemini-2.0-flash') 

SUPPORTED_LANGUAGES = ['en', 'fr', 'hi']

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """
    Handles incoming chat messages, detects language, translates,
    interacts with Google Gemini LLM, translates the response, and returns it.
    This version is restricted to English, French, and Hindi.
    """
 
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    user_message = data.get('message')
    target_language = data.get('target_language', 'en').lower()
    if target_language not in SUPPORTED_LANGUAGES:
        print(f"Unsupported target language requested: {target_language}. Defaulting to 'en'.")
        target_language = 'en'

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    print(f"Received message: '{user_message}' (Requested Target Lang: {target_language})")

    try:
       
        lang_detection_prompt = f"Detect the ISO 639-1 language code (e.g., 'en', 'es', 'fr', 'hi') of the following text and return ONLY the code. Text: '{user_message}'"
        lang_detection_response = TRANSLATION_MODEL.generate_content(lang_detection_prompt)
        detected_lang = lang_detection_response.text.strip().lower()

        if detected_lang not in SUPPORTED_LANGUAGES:
            print(f"Detected unsupported input language: {detected_lang}. Processing in English.")
            
        else:
            print(f"Detected user language: {detected_lang}")


        translated_user_input_en = user_message
        if detected_lang != 'en':
            print(f"Translating user message from {detected_lang} to English...")
            translation_to_en_prompt = f"Translate the following text from {detected_lang} to English: '{user_message}'"
            translation_to_en_response = TRANSLATION_MODEL.generate_content(translation_to_en_prompt)
            translated_user_input_en = translation_to_en_response.text.strip()
            print(f"User message translated to English: '{translated_user_input_en}'")
        else:
            print("User message is already in English, no translation needed for LLM input.")

     
        print("Getting response from main chatbot LLM (Gemini)...")
       
        chat_session = CHAT_MODEL.start_chat(history=[])
        chatbot_response_en_raw = chat_session.send_message(translated_user_input_en)
        chatbot_response_en = chatbot_response_en_raw.text.strip()
        print(f"Chatbot response (English): '{chatbot_response_en}'")

        final_translated_response = chatbot_response_en
        if target_language != 'en':
            print(f"Translating chatbot response from English to {target_language}...")
            translation_to_target_prompt = f"Translate the following English text to {target_language}: '{chatbot_response_en}'"
            translation_to_target_response = TRANSLATION_MODEL.generate_content(translation_to_target_prompt)
            final_translated_response = translation_to_target_response.text.strip()
            print(f"Final translated response: '{final_translated_response}'")
        else:
            print("Target language is English, no translation needed for bot's response.")

        return jsonify({"response": final_translated_response}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
      
        return jsonify({"error": "An internal server error occurred with the AI model. Please try again."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
