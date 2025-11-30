import asyncio
import speech_recognition as sr
import pyttsx3
import platform
from npmai import Gemini
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import streamlit as st
from gtts import gTTS
import os

text = None

recognizer = sr.Recognizer()

async def listen_and_convert():
    global text
    with sr.Microphone() as source:
        st.write("Mic on(for 10 secons)")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            st.write("Audio captured,now converting to text")
            raw_text = recognizer.recognize_google(audio, language="hi-IN")
            text = transliterate(raw_text, sanscript.DEVANAGARI, sanscript.IAST) + " (provide response in roman lipi, not devanagari)"
            st.write(f"Text (Roman lipi with prompt): {text}")
            return text
        except sr.UnknownValueError:
            st.write("did not understood you audio sorry ")
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


def text_to_speech(output_text: str):
    if platform.system() != "Emscripten" and os.environ.get("STREAMLIT_CLOUD") is None:
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            engine.say(output_text)
            engine.runAndWait()
            st.write("Audio output played!")
        except Exception as e:
            st.write(f"pyttsx3 error: {e}")
    else:
        try:
            tts = gTTS(text=output_text, lang='hi')
            tts.save("output.mp3")
            st.audio("output.mp3")
            st.write("Audio output available as MP3!")
        except Exception as e:
            st.write(f"gTTS error: {e}")


async def main():
    await listen_and_convert()
    return text


st.title("Voice AI App")
st.write("Click the button to start listening to voice input.")

if st.button("Start Mic"):
    # Run based on platform
    if platform.system() == "Emscripten":
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())


    if text and "Error" not in text and "Could not" not in text:
        prompts=text
        llm=Gemini()
        print(llm.invoke(prompts))

    else:
        st.write(f"No valid query to process: {text}")
        text_to_speech(f"No valid query to process: {text}")
