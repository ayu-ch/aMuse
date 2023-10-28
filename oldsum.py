#lyrics

token = "WnH5RtGSD-JQk9kxJwYySrwu6RpBkIBFDip5pKL21V285E22pxIt73JEI1RoTWWg"
genius = Genius(token)


@app.route('/lyrics')
def lyrics():
    return render_template('lyrics.html')

@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    song_name = request.form['song_name']
    artist_name = request.form['artist_name']

    song = genius.search_song(song_name, artist_name)
    lyrics = song.lyrics

    r = requests.post(
        "https://api.deepai.org/api/text-generator",
        files={'text': lyrics},
        headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
    )

    generated_summary = r.json()['output']
    return render_template('result.html', generated_summary=generated_summary)

response["choices"][0]["text"]