import os
import time
import config
import requests
import playsound
import speech_recognition as sr
from gtts import gTTS

class VoiceRecognizer():
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.command_duration = 30

    def get_audio(self):
        query = ''
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, 1)
            print("Listening....")
            audio = self.recognizer.listen(source)

            try:
                print("Recognizing...")
                query = self.recognizer.recognize_google(audio, language='en-in')
                print(f"You said: {query}")

            except sr.UnknownValueError:
                pass
                print("Cannot recognize speech!")

            except sr.RequestError:
                print("HTTP connection error!")

        return query
    
    def take_command(self):
        start_time = time.time()
        while True:
            print("Receiving command....")
            text = self.get_audio()
            try:
                if "turn on the light" in text.lower():
                    self.speak("Turning on the light")
                    self.turn_light(1)
                if "turn off the light" in text.lower():
                    self.speak("Turning off the light")
                    self.turn_light(0)

                if "turn on the fan" in text.lower():
                    self.speak("Turning on the fan")
                    self.turn_fan(100)
                if "turn off the fan" in text.lower():
                    self.speak("Turning off the fan")
                    self.turn_fan(0)
            except Exception:
                self.speak("Sorry! There might be some error!")

            curr_time = time.time()
            if curr_time - start_time > self.command_duration:
                break

    def turn_light(self, value):
        data = {'data': value}
        res = requests.put(
            url="http://{}:{}/api/gateway/device/{}".format(config.SERVER_HOST, config.SERVER_PORT, config.LED_ID),
            data=data)
        return res
    
    def turn_fan(self, value):
        data = {'data': value}
        res = requests.put(
            url="http://{}:{}/api/gateway/device/{}".format(config.SERVER_HOST, config.SERVER_PORT, config.FAN_ID),
            data=data)
        return res

    def speak(self, text):
        tts = gTTS(text=text, lang="en")
        filename = "voice.mp3"
        tts.save(filename)
        playsound.playsound(filename)

    def run(self):
        while True:
            text = self.get_audio()
            if "hi siri" in text.lower():
                self.speak("Hello! How can I help you?")
                self.take_command()

if __name__=='__main__':
    assistant = VoiceRecognizer()
    assistant.run()