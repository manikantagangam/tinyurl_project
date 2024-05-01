from flask import Flask, render_template, request, redirect, url_for
import random
import string

app = Flask(__name__)

class TinyURL:
    def __init__(self):
        self.url_map = {}

    def generate_short_url(self):
        # Generate a random short URL using alphanumeric characters
        characters = string.ascii_letters + string.digits
        short_url = ''.join(random.choice(characters) for _ in range(8))
        return short_url

    def shorten_url(self, long_url):
        # Generate a unique short URL
        while True:
            short_url = self.generate_short_url()
            if short_url not in self.url_map:
                self.url_map[short_url] = long_url
                return short_url

    def get_original_url(self, short_url):
        # Retrieve the original URL from the hash map
        return self.url_map.get(short_url, None)

tiny_url = TinyURL()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = tiny_url.shorten_url(long_url)
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_original(short_url):
    original_url = tiny_url.get_original_url(short_url)
    if original_url:
        return redirect(original_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
