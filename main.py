import markdown as md
import os
import requests
import time

from flask import Flask, request, render_template

chat_history = []

os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
time.tzset()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def show_form():
    return render_template('chat.html', history=chat_history)

@app.route("/", methods=["POST"])
def process_form():
    message = request.form["user_input"]

    user_time = time.strftime('%l:%M:%S %p %Z on %b %d, %Y', time.localtime())
    user_input = message

    print("User:", message)

    prompt = '''
    You are a nice and helpful chatbot.
    Be succint and to the point, unless the user asks for more details.
    Answer the user's question, taking in consideration the conversation history.

    ***QUESTION***
    ''' + message + '''

    ***HISTORY***
    ''' + str(chat_history)

    print("Prompt: ",prompt)
    response = requests.post('http://localhost:11434/api/generate',
                             json={"model": "llama3.1", "prompt": prompt, "stream":False},
                             headers={'Content-Type': 'application/json'})
                       
    bot_text = response.json()['response']
    print("Bot:",bot_text)
    bot_text = md.markdown(bot_text)

    response_time = time.strftime('%l:%M:%S %p %Z on %b %d, %Y', time.localtime())
    chat_history.append((user_time, user_input, response_time, bot_text))

    print("History: ",chat_history)

    return render_template('chat.html', history=chat_history)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
