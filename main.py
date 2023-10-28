import requests
import urllib.parse
import os
import openai
from lyricsgenius import Genius
from datetime import datetime , timedelta
from flask import Flask , redirect, request, jsonify, session, render_template


app = Flask(__name__)
app.secret_key='a35k2k3kjg46897&'
openai.api_key = "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"

mood = ''
@app.route('/')
def index():
  return render_template("home.html")

@app.route('/moodify')
def moodify():
   return render_template("moodify.html")

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
     mood = 'fuck'; 
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
  
  return render_template("index.html", data = stuff)


  
  

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
    return render_template('sum.html')

@app.route('/generate_summary', methods=['POST'])
def input():
  song= request.form['song_name']
  artist = request.form['artist_name']
  prompt = f'write a approx long summary for the song {song} by {artist}'

  response = openai.Completion.create(
    engine = "text-davinci-002",
    prompt= prompt,
    temperature = 0.4,
    max_tokens=2048
  )
  generated_summary = response["choices"][0]["text"]
  return render_template('result.html', generated_summary=generated_summary)


app.run(debug=True)