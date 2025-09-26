import speech_recognition as sr
import os
import pyttsx3
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import time
import streamlit as st

# Initialize global text variable
text = None

# Initialize recognizer
recognizer = sr.Recognizer()

# Async function to listen and convert audio to text
async def listen_and_convert():
    global text
    with sr.Microphone() as source:
        st.write("Mic on! Bolna shuru karo... (5 seconds sunega)")
        # Adjust for ambient noise (2 seconds for rural noise)
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            st.write("Audio captured! Converting to text...")
            raw_text = recognizer.recognize_google(audio, language="hi-IN")
            text = transliterate(raw_text, sanscript.DEVANAGARI, sanscript.IAST) 
            st.write(f"Text (Roman lipi): {text}")
            return text
        except sr.UnknownValueError:
            st.write("Audio nahi samjha!")
            text = "Could not understand audio"
            return text
        except sr.RequestError as e:
            st.write(f"Google API error: {e}")
            text = "Error in recognition"
            return text
        except Exception as e:
            st.write(f"Unexpected error: {e}")
            text = "Something went wrong"
            return text

# Function to convert text to speech with pyttsx3
def text_to_speech(output_text: str):
    try:
        engine = pyttsx3.init()
        # Adjust voice properties for clarity
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        engine.say(output_text)
        engine.runAndWait()
        st.write("Audio output played!")
    except Exception as e:
        st.write(f"pyttsx3 error: {e}")

# Async main function for Pyodide compatibility
async def main():
    await listen_and_convert()
    return text

# Streamlit app
st.title("Voice AI App")
st.write("Click the button to start listening to voice input.")

if st.button("Start Mic"):
    # Run based on platform
    if platform.system() == "Emscripten":
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())

    # Selenium part (runs after async completes)
    if text and "Error" not in text and "Could not" not in text:
        userq = text
        # Setup Selenium with headless mode
        options = Options()
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless=new")  # Headless mode for efficiency
        options.add_argument("--disable-gpu")  # Disable GPU for headless
        options.add_argument("--no-sandbox")  # For Streamlit Cloud
        options.add_argument("--disable-dev-shm-usage")  # For Streamlit Cloud
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
            """
        })
        
        try:
            driver.get("https://www.google.com")
            # Wait for AI mode button
            aimode = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[class*='plR5qb']"))
            )
            aimode.click()
            
            # Wait for query input
            query = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='ITIRGe']"))
            )
            query.send_keys(userq)
            query.send_keys(Keys.RETURN)
            
            # Wait for result (optimized timeout)
            result = WebDriverWait(driver, 20).until(  # Reduced timeout for efficiency
                EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='pWvJNd']"))
            )
            gemini_output = result.text
            st.write(f"Gemini Output: {gemini_output}")
            
            # Convert Gemini output to audio
            text_to_speech(gemini_output)
        except Exception as e:
            st.write(f"Selenium error: {e}")
            text_to_speech("Error fetching Gemini result")
        finally:
            driver.quit()
    else:
        st.write(f"No valid query to process: {text}")
        text_to_speech(f"No valid query to process: {text}")
