import os
import speech_recognition as sr
from PIL import Image, ImageTk
import tkinter as tk

base_path = "C:\\Users\\mdufe\\Pictures\\StreamPNGs\\PNGTuber_Final_Renders\\"
output_path = "C:\\Users\\mdufe\\Pictures\\StreamPNGs\\PNGTuber_Final_Renders\\current\\"

current_set = "happy"
talking = False
size = 300
current_path = os.path.join(output_path, "temp.png")


# Function to switch images based on voice commands
def switch_image(command):
    global current_set
    global talking

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
def update_image():
    global talking
    if talking:
        activity = "_talking.png"
    else:
        activity = "_idle.png"
    img_name = current_set + activity
    img_path = base_path + img_name

    img = Image.open(img_path)
    img = img.resize((size, size))  # Adjust size as needed
    photo = ImageTk.PhotoImage(img)

    label.configure(image=photo)
    label.image = photo
    resized_img = img.resize((size, size))

    resized_img.save(current_path)


# Function to recognize voice commands
def recognize_voice():
    global talking

    print("Listening...")
    try:
        audio = recognizer.listen(source, timeout=5)

        try:
            command = recognizer.recognize_google(audio)
            print("Heard: ", command)
            talking = True
            switch_image(command)

            update_image()
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error:", e)
    except sr.WaitTimeoutError as e:
        talking = False
        update_image()


# GUI setup
root = tk.Tk()
root.configure(bg='SystemButtonFace')
root.title("Character Emotion Switcher")
label = tk.Label(root, bg='SystemButtonFace')
label.pack()

# Main code
update_image()
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Starting ambient noise adjustment")
    recognizer.adjust_for_ambient_noise(source, 10)
    print("Safe to talk now")
    # Main loop to continuously listen for voice commands
    while True:
        recognize_voice()
        root.update()
