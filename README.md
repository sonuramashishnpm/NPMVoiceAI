Project Overview
This is a Voice AI App built with Streamlit for rural users in India. It listens to voice input in Hindi/Urdu, converts it to Roman script text, queries Google AI (Gemini) for responses, and plays the output as audio. Designed for simple accessibility – click a button, speak, get Roman text and spoken reply. High-level goal: Help farmers/students with quick info (e.g., crop risks, weather), no typing needed.
Key Features

Voice Input: Mic button starts listening (5 seconds, adjustable for noise).
Transliteration: Hindi/Urdu speech to Roman lipi (e.g., "Patna mein..." instead of Devanagari script).
AI Query: Selenium fetches Google AI (Gemini) responses in Roman format.
Audio Output: pyttsx3 plays responses aloud (offline, adjustable speed/volume).
Error Handling: Handles no audio, recognition errors, Selenium issues with user-friendly messages.
Streamlit UI: Web-based app with button, real-time feedback, and text display.
Efficiency: Headless Chrome for backend queries, no visible browser.

Installation

Clone the repo: git clone <your-repo-url>.
Install dependencies: pip install -r requirements.txt.
Run locally: streamlit run app.py.

Usage

Open the app in browser (localhost:8501).
Click "Start Mic" button.
Speak your query (Hindi/Urdu, e.g., "Patna mein rice crop ka risk kya hai?").
App shows Roman text, Gemini response, and plays audio.
Errors like "Audio nahi samjha!" are handled with messages.
