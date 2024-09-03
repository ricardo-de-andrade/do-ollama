# Deploying Ollama and llama 3.1 into a Digital Ocean's droplet

Our ultimate goal here is to use a LLM in order to build a LLM based chatbot and have that running as a web application in DO's platform.

Why? Because **we can** and it's **fun**.

## Create a Digital Ocean account

All new accounts come with a $200 credit (at the time of this writting)

Navigate to [Digital Ocean](https://cloud.digitalocean.com/registrations/new "Free $200 credit for new accounts")  to get started.


## Create a droplet

Follow the instrudctions in the documentation to get started, or jumpt to [the droplets page](https://cloud.digitalocean.com/droplets/new) to create a new one

For our purposes, the bigger the machine the better performance we'll be getting from the model.

In my case I have maximized what was available in my trial account for the Premium Intel options, with a 8GB/4 Intel CPU

![Droplet Spec](/assets/droplet-spec.png)

### Connect to the droplet via the console or SSH

I use the console button (right of the screen) from the browser for its ease of use approach for connecting to the droplet, 

![Console Button and IP Address](/assets/console-button-ip.png)

![Console](/assets/do-web-console.png)


or you can connect via SSH directly to your droplet's IP address (left of the screen) as well.

``ssh root@DROPLET-IP``

![SSH](/assets/ssh.png)

### Update your droplet
From your newly open access into your droplet, update its packages with:

``sudo apt update && sudo apt upgrade``

## Setting up for our application

Now we'll focus a bit more on what we need run our app.

### Install Ollama

``curl -fsSL https://ollama.com/install.sh | sh``

### Run the llama 3.1 model

``ollama run llama3.1``

### Test it

You can ask a few questions directly on the terminal with the Ollama 'interface'.

Try a few simple prompts. You should see the model responding, **and** you'll get a feel for the performance for our app later on.

You can also test via the built-in API

``/bye`` - to get out of the Ollama prompt interface

And, to invoke the Ollama API:

``curl http://localhost:11434/api/generate -d '{"model": "llama3.1", "prompt": "hello", "stream":false}'``


## Getting llama 3.1 to generate the code for us

> [!NOTE]
> LLMs are non-deterministic and as you are running your own prompts into your own installation, the code generated may look slightly different than the code I show as example here.

> [!NOTE 2]
> There are no guarantees that the code shown here, or the code generated in your attempts will run out of the box.
> The main intent here is to show the though process on how to leverag a LLM to help you build your code faster.
> You should be able to decide whether the code will work or not, and better yet, make it work after teh base is generated.


For this demo, we'll build the app as a simple conversation with the model.

Back at the Ollama prompt interface, enter the following sample prompts, in order to get their respective sample base code for our app.

### Prompt 1.

> ```
> generate a simple python webserver hello world using flask
> ```

**Generated code**

[prompt1.py](/prompt1.py)
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
```

### Prompt 2.

> ```
> please make this app present a simple html form that asks for the user input as text and sends it to the server
> ```

**Generated code**

[prompt2.py](/prompt2.py)
```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Define a simple HTML template for our form
form_template = '''
<form method="POST">
    <input type="text" name="username" placeholder="Enter your name...">
    <input type="submit" value="Submit">
</form>
'''

@app.route("/", methods=["GET"])
def show_form():
    return render_template_string(form_template)

@app.route("/", methods=["POST"])
def process_form():
    username = request.form["username"]
    return f"Hello, {username}!"

if __name__ == "__main__":
    app.run(debug=True)
```

### Prompt 3.

> ```
> in the method that receives the input, take the string that was sent by the user and send a request to ollama running locally by invoking its api on http://localhost:11434/api/generate
> ```

**Generated code**

[prompt3.py](/prompt3.py)
```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Define a simple HTML template for our form
form_template = '''
<form method="POST">
    <input type="text" name="username" placeholder="Enter your name...">
    <input type="submit" value="Submit">
</form>
'''

@app.route("/", methods=["GET"])
def show_form():
    return render_template_string(form_template)

@app.route("/generate", methods=["POST"])
def process_form():
    username = request.form["username"]
    import requests
    response = requests.post(f"http://localhost:11434/api/generate",
                             json={"input": username},
                             headers={'Content-Type': 'application/json'})
    return f"Generated Image URL: {response.json()['url']}"

if __name__ == "__main__":
    app.run(debug=True)

```
### Prompt 4.

> ```
> we are building a chatbot. the user input is what the user is asking of the bot, and the responses from the local api the bot's responses. in the same single page, display the input form as well as the chat history
> ```

**Generated code**

[prompt4.py](/prompt4.py)
```python
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
```

## Taking over the code writting from here

### A few more tweaks and 'beutification' of the app and we should end with

![Chatty Chat](/assets/chatty-chat.png)

**Manual changes implemented**
1. Separate the HTML code from the python code
2. Display the chat history on top and the user input at the bottom
3. Make the history scrollable
4. Apply some 'visual' to the app with a left column and the DO logo
5. In the history, display the text with a timestamp, and render as markdown
6. Align the model's response to the left and the user's input to the right


![](/assets/do-ollama.png)
