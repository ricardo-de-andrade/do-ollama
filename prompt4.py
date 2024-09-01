####
#
# we are building a chatbot. the user input is what the user is 
# asking of the bot, and the responses from the local api the 
# bot's responses. in the same single page, display the input 
# form as well as the chat history
#
####
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Define a simple HTML template for our form
form_template = '''
<form method="POST">
    <input type="text" name="message" placeholder="Type your message...">
    <button type="submit">Send</button>
</form>
'''

chat_history_template = '''
<div class="chat-history">
    <ul>
        {% for message in chat_history %}
            <li>{{ message }}</li>
        {% endfor %}
    </ul>
</div>
'''

@app.route("/", methods=["GET"])
def show_form():
    return render_template_string(form_template + chat_history_template, chat_history=[])

@app.route("/", methods=["POST"])
def process_form():
    message = request.form["message"]
    import requests
    response = requests.post(f"http://localhost:11434/api/generate",
                             json={"input": message},
                             headers={'Content-Type': 'application/json'})
    new_chat_history = request.json()['url']

    # Store chat history in session
    if 'chat_history' not in app.session:
        app.session['chat_history'] = []
    app.session['chat_history'].append(new_chat_history)

    return render_template_string(form_template + chat_history_template,
                                   chat_history=app.session.get('chat_history', []))

if __name__ == "__main__":
    app.run(debug=True)

