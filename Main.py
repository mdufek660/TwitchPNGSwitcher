import os
import threading

import sounddevice as sd
import speech_recognition as sr
from PIL import Image
import numpy as np

base_path = "C:\\PNGTuber_Final_Renders\\"
output_path = "C:\\PNGTuber_Final_Renders\\current\\"

current_set = "happy"
size = 300
current_path = os.path.join(output_path, "temp.png")
ambientTime = 3


# Function to switch images based on voice commands
def switch_image(command):
    global current_set

    if "angry dot exe" in command or "angry dot EXE" in command or "angry EXE" in command:
        current_set = "angry"
    elif "anger dot exe" in command or "anger dot EXE" in command or "anger EXE" in command:
        current_set = "angry"

    elif "excited dot exe" in command or "excited dot EXE" in command or "excited EXE" in command:
        current_set = "excited"

    elif "happy dot exe" in command or "happy dot EXE" in command or "happy EXE" in command:
        current_set = "happy"
    elif "joy dot exe" in command or "joy dot EXE" in command or "joy EXE" in command:
        current_set = "happy"

    elif "confused dot exe" in command or "confused dot EXE" in command or "confused EXE" in command:
        current_set = "confused"
    elif "confuse dot exe" in command or "confuse dot EXE" in command or "confuse EXE" in command:
        current_set = "confused"
    elif "confused that exe" in command or "confused that EXE" in command or "confused EXE" in command:
        current_set = "confused"
    elif "confuse that exe" in command or "confuse that EXE" in command or "confuse EXE" in command:
        current_set = "confused"


# Function to update the displayed image
def update_image_set():
    img_talking = Image.open(base_path + current_set + "_talking.png")
    img_idle = Image.open(base_path + current_set + "_idle.png")

    img_talking = img_talking.resize((size, size))
    img_idle = img_idle.resize((size, size))

    img_talking.save(output_path + "current_talking.png")
    img_idle.save(output_path + "current_idle.png")
    updateTempImage()


# Function to recognize voice commands
def recognize_voice():
    print("Listening...")
    try:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

        try:
            command = recognizer.recognize_google(audio)
            print("Heard: ", command)
            switch_image(command)

            update_image_set()
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error:", e)
    except sr.WaitTimeoutError as e:
        pass

def speechDetector():
# Callback function to process audio data
    def callback(indata, frames, time, status):
        global volumeTracker
        audio_data = np.array(indata[:, 0])
        volumeTracker.extend(audio_data)

    def calculate_sound_level():
        global volumeTracker
        # Convert the accumulated samples to a NumPy array
        samples_array = np.array(volumeTracker)

        # Calculate the average sound level
        db_temp = 20 * np.log10(np.sqrt(np.mean(samples_array**2)))
        volumeTracker=[]
        return db_temp

    global volumeTracker
    duration = 1  # Duration of audio recording in seconds
    samplerate = 44100  # Sample rate
    channels = 1  # Mono audio

    global talking

    print("* Listening for audio presence...")
    # Start audio capture
    while True:
        with sd.InputStream(channels=channels, samplerate=samplerate, callback=callback):
            sd.sleep(int(duration * 1000))
        db = calculate_sound_level()
        print(db)
        if db > -38:
            if not talking:
                talking=True
                updateTempImage()
        else:
            if talking:
                talking=False
                updateTempImage()


def updateTempImage():
    if talking:
        img = Image.open(output_path + "current_talking.png")
        img.save(output_path + "temp.png")
    else:
        img = Image.open(output_path + "current_idle.png")
        img.save(output_path + "temp.png")


# Main code
talking = False
update_image_set()
recognizer = sr.Recognizer()
listener = sr.Recognizer()
volumeTracker = []

with sr.Microphone() as source, sr.Microphone() as source2:
    print("Starting ambient noise adjustment")
    recognizer.adjust_for_ambient_noise(source, ambientTime)
    listener.adjust_for_ambient_noise(source2, ambientTime)
    print("Safe to talk now")
    # Main loop to continuously listen for voice commands
    listener_thread = threading.Thread(target=speechDetector, daemon=True)
    listener_thread.start()
    while True:
        recognize_voice()
