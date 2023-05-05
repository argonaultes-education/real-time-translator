# communication with libretranslate
import json
import requests
# text to speech
from gtts import gTTS
from playsound import playsound

# speech to text
import speech_recognition as sr


def translate_text(text):

    url = "http://0.0.0.0:5000/translate"
    payload = {
        "q": text,
        "source": "auto",
        "target": "en",
        "format": "text",
        "api_key": ""
    }
    headers = { "Content-Type": "application/json" }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()['translatedText']

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    return (r, audio)

def audio_to_text_sphinx():

    # obtain audio from the microphone
    r, audio = get_audio()

    # recognize speech using Sphinx
    try:
        result = r.recognize_sphinx(audio)
        return result
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    return ''

def audio_to_text_google():
    # obtain audio from the microphone
    r, audio = get_audio()

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        result = r.recognize_google(audio, language='fr-FR')
        print("Google Speech Recognition thinks you said " + result)
        return result
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def audio_to_text_whisper():
    # obtain audio from the microphone
    r, audio = get_audio()
    try:
        result = r.recognize_whisper(audio, language='french')
        print("Whisper thinks you said " + result)
        return result
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper")

def text_to_audio(text):
    tts = gTTS(text, lang='en') #communication with external service
    tts.save('test.mp3')
    playsound('test.mp3')

# main statements
text = audio_to_text_whisper()
result = translate_text(text)
print(result)
text_to_audio(result)