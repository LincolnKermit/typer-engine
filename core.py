import os
from flask import Flask, request, jsonify, render_template
import logging


log = logging.getLogger('werkzeug')
app = Flask(__name__)
data_path = "sources/data/"
log.setLevel(logging.ERROR)

debug=False
host = "localhost"
port = 5000



app.config.update(
    debug=debug,
    HOST=host,
    PORT=port
)


def find_next_words(target_word, directory_path=data_path, max_results=3): # max 3 words
    next_words = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                words = file.read().split()  # Lit le contenu du fichier et sépare les mots
                for i, word in enumerate(words):
                    if word == target_word and i < len(words) - 1:
                        next_word = words[i + 1]
                        if next_word not in next_words:
                            next_words.append(next_word)
                        if len(next_words) == max_results: # max 3 words
                            print(next_word)
                            return next_words
    print(next_words)
    return next_words
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_next_words', methods=['GET'])
def get_next_words():
    target_word = request.args.get('target_word', '')
    if target_word:
        next_words = find_next_words(target_word)
        return jsonify(next_words)
    return jsonify([])

if __name__ == '__main__':
    os.system("clear")
    print("App is running on "+app.config['HOST']+":"+str(app.config['PORT']))
    app.run()
