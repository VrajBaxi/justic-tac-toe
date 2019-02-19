"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, session, redirect, url_for
from flask_sessions import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def index():
    """Renders a sample page."""
    if "board" not in session:
        session["board"] = [[None,None,None],[None,None,None],[None,None,None]]
        session["turn"] = "X"
        session["winner"] = None
        
    return render_template("index.html", game=session["board"], turn=session["turn"], win=session["winner"])

@app.route('/reset')
def reset():
    session["board"] = [[None,None,None],[None,None,None],[None,None,None]]
    session["turn"] = "X"
    session["winner"] = None
    return redirect(url_for("index"))

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]

    for i in range(3):
        if session["board"][i][0] == session["board"][i][1] == session["board"][i][2] == session["turn"]:
            session["winner"] = session["turn"]
        if session["board"][0][i] == session["board"][1][i] == session["board"][2][i] == session["turn"]:
            session["winner"] = session["turn"]
        
    if session["board"][0][0] == session["board"][1][1] == session["board"][2][2] == session["turn"]:
        session["winner"] = session["turn"]
    if session["board"][0][2] == session["board"][1][1] == session["board"][2][0] == session["turn"]:
        session["winner"] = session["turn"]

    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"
    return redirect(url_for("index"))

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
