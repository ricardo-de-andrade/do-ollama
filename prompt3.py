####
#
# in the method that receives the input, take the string that was sent by the user 
# and send a request to ollama running locally by invoking its api on 
# http://localhost:11434/api/generate
#
####
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
