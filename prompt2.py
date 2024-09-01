####
#
# please make this app present a simple html form that asks for the 
# user input as text and sends it to the server
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

@app.route("/", methods=["POST"])
def process_form():
    username = request.form["username"]
    return f"Hello, {username}!"

if __name__ == "__main__":
    app.run(debug=True)
