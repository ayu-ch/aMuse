import requests
import urllib.parse
import os
import openai
from lyricsgenius import Genius
from datetime import datetime , timedelta
from flask import Flask , redirect, request, jsonify, session, render_template
import pygame


app = Flask(__name__)
app.secret_key='a35k2k3kjg46897&'
openai.api_key = "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"

mood = ''
@app.route('/')
def index():
  return render_template("index-one.html")

@app.route('/moodify')
def moodify():
   return render_template("blog-one.html")

@app.route('/mood',methods =['POST'])
def moods():
  input=request.form['mood']
  
  if input.lower() =='happy':
      mood= 'happy'
  elif input.lower() =='sad':
     mood='sad'
  elif input.lower() == 'energetic':
     mood ='dance'
  elif input.lower()=='romantic':
     mood= 'romance'
  elif  input.lower()=='sleepy':
     mood = 'sleep'
  else:
     mood = 'invalid'; 
  os.environ['MOOD'] = mood
  return redirect('/login')


#SPOTIFY

CLIENT_ID ='450c737a01d744aea47e3b91f3d43725'
CLIENT_SECRET = '15265a49b9f94d78828a6f774ae00bad'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL= 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'

    params = {
       'client_id': CLIENT_ID,
       'response_type': 'code',
       'scope': scope,
       'redirect_uri': REDIRECT_URI,
       'show_dialog': True
    }
    
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)    

@app.route('/callback')
def callback():
  if 'error' in request.args:
     return jsonify({"error": request.args['error']})
  
  if 'code' in request.args: 
    req_body = {
       'code': request.args['code'],
       'grant_type': 'authorization_code',
       'redirect_uri': REDIRECT_URI,
       'client_id': CLIENT_ID,
       'client_secret': CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=req_body)
    token_info = response.json()

    session['access_token']=token_info['access_token']
    session['refresh_token']=token_info['refresh_token']
    session['expires_at']=datetime.now().timestamp()+token_info['expires_in']

    return redirect('/recommends')
  
@app.route('/recommends')
def get_recommends():
  if 'access_token' not in session:
      return redirect('/login')
  mood = os.getenv("MOOD")
  if datetime.now().timestamp() > session['expires_at']:
      return redirect('/refresh-token')
   
  headers ={
      'Authorization' :  f"Bearer {session['access_token']}"

   }
  
  route = 'recommendations?limit=1&seed_genres='+mood
  # log(route)

  response = requests.get(API_BASE_URL + route ,headers=headers)
  track = response.json()

  stuff = {
    "song": track["tracks"][0]['name'],
    "artist": track["tracks"][0]["artists"][0]["name"],
    "link": track["tracks"][0]['external_urls']["spotify"],
    "image": track["tracks"][0]["album"]["images"][1]["url"]
  }
  prompt = f'Give a short description of the song {stuff["song"]} by {stuff["artist"]}'

  response = openai.Completion.create(
    engine = "text-davinci-002",
    prompt= prompt,
    temperature = 0.4,
    max_tokens=64
  )

  
  generated_summary = response["choices"][0]["text"]
  return render_template("blog-single.html", data = stuff,generated_summary=generated_summary)


  
  

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
      return redirect('/login')
   
    if datetime.now().timestamp() > session['expires_at']:
      req_body ={ 
         'grant_type': 'refresh_token',
         'refresh_tokenn': session['refresh_token'],
         'client_id': CLIENT_ID,
         'client_secret': CLIENT_SECRET
      }
      
      response = requests.post(TOKEN_URL, data= req_body)
      new_token_info = response.json()

      session['access_token'] = new_token_info['access_token']
      session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']



@app.route('/summary')
def sum():
    return render_template('blog-two.html')

@app.route('/generate_summary', methods=['POST'])
def input():
  song= request.form['song_name']
  artist = request.form['artist_name']
  
  prompt1 = f'write the summary of the song {song} by {artist}'

  response1 = openai.Completion.create(
    engine = "text-davinci-002",
    prompt= prompt1,
    temperature = 1,
    max_tokens=2048
  )
  
  prompt2 = f'Give the lyrics of the song {song} by {artist}'

  response2 = openai.Completion.create(
    engine = "text-davinci-002",
    prompt= prompt2,
    temperature = 0.4,
    max_tokens=64
  )
  

  generated_summary1 = response1["choices"][0]["text"]
  generated_summary2 = response2["choices"][0]["text"]

  
  return render_template('summary.html', generated_summary1=generated_summary1, generated_summary2= generated_summary2)


pygame.init()
key_to_sound = {

    '1': './static/Beat 1.wav',
    '2': './static/Beat 2.wav',
    '3': './static/Beat 3.wav',
    '4': './static/Beat 4.wav',
    '5': './static/Beat 5.wav',
    '6': './static/Beat 6.wav',
    '7': './static/Beat 7.wav',
    '8': './static/Beat 8.wav',
    '9': './static/Beat 9.wav',
    '0': './static/Beat 10.wav',
    'q': './static/Bass 1.wav',
    'w': './static/Bass 2.wav',
    'a': './static/Bass 3.wav',
    's': './static/Bass 4.wav',
    'z': './static/Syn 1.wav',
    'x': './static/Syn 2.wav',
    'c': './static/Syn 3.wav',
    'v': './static/Syn 4.wav',
    'b': './static/Syn 5.wav',
    'n': './static/Syn 6.wav',
    'm': './static/Syn 7.wav',
    'p': './static/animals.wav',
    'o': './static/blinding lights.wav',
    'l': './static/do i wanna know.wav',
    'k': './static/roses.wav',
    'i': './static/jack.wav',
    'j': './static/panda.wav',
    'u': './static/cradles.wav',
    'h': './static/bella-ciao.wav'




}

sounds = {key: pygame.mixer.Sound(sound_file) for key, sound_file in key_to_sound.items()}
sound_status = {key: False for key in key_to_sound}

@app.route('/keydm')
def hello():
    return render_template('songs-one.html')

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

@app.route('/about')
def fun():
   return render_template("about-one.html")


app.run(debug=True)
