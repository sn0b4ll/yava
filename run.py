#!/usr/bin/env python3

import json
import pyaudio
import time
import os
import pyttsx3
# import _thread
import threading

from vosk import Model, KaldiRecognizer

# Init TTS
tts_engine = pyttsx3.init()
# Sorry fur windows things here, have to check how to make it os-independend
german_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_DE-DE_HEDDA_11.0"
tts_engine.setProperty('voice', german_voice)

# Init Speech-Recog
if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

model = Model("model")
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Configs
keyword = "computer"


class TTS(threading.Thread):
    activated = False

    def run(self):
        print("Init done")

    def process(self, input):
        if self.activated:
            if "status" in input:
                tts_engine.say("Voice Assistand ist aktiv")    
        elif keyword in input:
            # Not yet activated but keyword is called
            self.activated = True
            tts_engine.say("Voice Assistand wurde aktiviert")
            
        tts_engine.runAndWait()

        


# Start the TTS in new threat to not interfere with the Speech-Recog
tts = TTS()
tts.start()

while True:
    data = stream.read(4000, exception_on_overflow = False)
    if len(data) == 0:
        break

    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())
        if res['text'] != "":
            print(res['text'])
            tts.process(res['text'])
    else:
        # print(rec.PartialResult())
        pass

print(rec.FinalResult())

