import os
import requests
import config
import time
import torch
import torchaudio
import sounddevice as sd
import wavio as wv
import playsound
from gtts import gTTS

class GreedyCTCDecoder(torch.nn.Module):
    def __init__(self, labels, blank=0):
        super().__init__()
        self.labels = labels
        self.blank = blank

    def forward(self, emission: torch.Tensor) -> str:
        """Given a sequence emission over labels, get the best path string
        Args:
          emission (Tensor): Logit tensors. Shape `[num_seq, num_label]`.

        Returns:
          str: The resulting transcript
        """
        indices = torch.argmax(emission, dim=-1)  # [num_seq,]
        indices = torch.unique_consecutive(indices, dim=-1)
        indices = [i for i in indices if i != self.blank]
        return "".join([self.labels[i] for i in indices])


class VoiceRecognizer:
    def __init__(self):
        self.bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
        print("Sample Rate:", self.bundle.sample_rate)
        print("Labels:", self.bundle.get_labels())

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.bundle.get_model().to(self.device)
        self.decoder = GreedyCTCDecoder(labels=self.bundle.get_labels())
    
    def get_freq(self):
        return self.bundle.sample_rate

    def recognize(self, speech_file):
        waveform, sample_rate = torchaudio.load(speech_file)
        waveform = waveform.to(self.device)
        if sample_rate != self.bundle.sample_rate:
            waveform = torchaudio.functional.resample(waveform, sample_rate, self.bundle.sample_rate)

        with torch.inference_mode():
            emission, _ = self.model(waveform)
            transcript = self.decoder(emission[0])
        return transcript

class VoiceAssistant:
    def __init__(self, duration=5):
        self.recognizer = VoiceRecognizer()
        self.freq = self.recognizer.get_freq()
        self.duration = duration
        self.speech_file = 'voice.wav'
        self.command_duration = 30
    
    def get_audio(self):
        recording = sd.rec(int(self.duration * self.freq), samplerate=self.freq, channels=2)
        sd.wait()
        wv.write(self.speech_file, recording, self.freq, sampwidth=2)
    
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
        try:
            tts = gTTS(text=text, lang="en")
            filename = "voice.mp3"
            tts.save(filename)
            playsound.playsound(filename)
        except Exception as err:
            print('Cannot generate speech: ', err)

    def check_token(self, tokens, ref):
        res = True
        ref = ref.lower()
        for token in tokens:
            tk_res = False
            for syn in token:
                tk_res = tk_res or (syn in ref)
            res = res and tk_res
        return res

    def run(self):
        while True:
            print('Listening...')
            self.get_audio()
            text = self.recognizer.recognize(self.speech_file)
            if text != '':
                text = text.replace('|', ' ')
                print(text)
                if self.check_token([['hi', 'hih', 'high', 'heh', 'hey'], ['ciri', 'siri', 'seeri', 'seri', 'sere', 'sire', 'seere']], text):
                    self.speak('Hello! How can I help you?')
                    self.take_command()

    def take_command(self):
        start_time = time.time()
        while True:
            print('Listening...')
            self.get_audio()
            print('Recognizing Command...')
            text = self.recognizer.recognize(self.speech_file)
            try:
                text = text.replace('|', ' ')

                if self.check_token([['turn'], ['on'], ['light']], text):
                    self.speak("Turning on the light")
                    self.turn_light(1)
                if self.check_token([['turn'], ['off'], ['light']], text):
                    self.speak("Turning off the light")
                    self.turn_light(0)

                if self.check_token([['turn'], ['on'], ['fan']], text):
                    self.speak("Turning on the fan")
                    self.turn_fan(100)
                if self.check_token([['turn'], ['off'], ['fan']], text):
                    self.speak("Turning off the fan")
                    self.turn_fan(0)

            except:
                print('Cannot recognize command!')
            curr_time = time.time()
            if curr_time - start_time > self.command_duration:
                break

if __name__=='__main__':
    voice_assistant = VoiceAssistant()
    voice_assistant.run()