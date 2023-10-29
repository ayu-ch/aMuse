
from flask import Flask, render_template, request
import pygame

app = Flask(__name__)
pygame.init()

key_to_sound = {

    '1': 'Beat 1.wav',
    '2': 'Beat 2.wav',
    '3': 'Beat 3.wav',
    '4': 'Beat 4.wav',
    '5': 'Beat 5.wav',
    '6': 'Beat 6.wav',
    '7': 'Beat 7.wav',
    '8': 'Beat 8.wav',
    '9': 'Beat 9.wav',
    '0': 'Beat 10.wav',
    'q': 'Bass 1.wav',
    'w': 'Bass 2.wav',
    'a': 'Bass 3.wav',
    's': 'Bass 4.wav',
    'z': 'Syn 1.wav',
    'x': 'Syn 2.wav',
    'c': 'Syn 3.wav',
    'v': 'Syn 4.wav',
    'b': 'Syn 5.wav',
    'n': 'Syn 6.wav',
    'm': 'Syn 7.wav',
    'p': 'animals.wav',
    'o': 'blinding lights.wav',
    'l': 'do i wanna know.wav',
    'k': 'roses.wav',
    'i': 'jack.wav',
    'j': 'panda.wav',
    'u': 'cradles.wav',
    'h': 'bella-ciao.wav',




}

sounds = {key: pygame.mixer.Sound(sound_file) for key, sound_file in key_to_sound.items()}
sound_status = {key: False for key in key_to_sound}

@app.route('/')
def index():
    return render_template('keydm.html')

@app.route('/play_sound', methods=['POST'])
def play_sound():
    key = request.form['key']
    if key == " ":  # Check if the space key is pressed
        stop_all_sounds()
        return "All sounds stopped."
    elif key in key_to_sound:
        if sound_status[key]:
            sounds[key].stop()
            sound_status[key] = False
            return "Sound stopped."
        else:
            sounds[key].play(loops=-1)
            sound_status[key] = True
            return "Sound played."
    else:
        return "Key not mapped to a sound."

def stop_all_sounds():
    for key in key_to_sound:
        if sound_status[key]:
            sounds[key].stop()
            sound_status[key] = False

if __name__ == '__main__':
    app.run(debug=True)

