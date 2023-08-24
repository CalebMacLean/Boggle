from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"

boggle_game = Boggle()


@app.route("/")
def homepage():
    """Show board."""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("base.html", board=board,
                           highscore=highscore,
                           nplays=nplays)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)








# # Imports
# from boggle import Boggle
# from flask import Flask, render_template, redirect, request, session, flash 
# from flask_debugtoolbar import DebugToolbarExtension

# # Application Configurations and Global Features
# boggle_game = Boggle()
# app = Flask(__name__)

# CURRENT_BOARD_KEY = 'current_board'

# app.config['SECRET_KEY'] = 'CanY0uGue551t'
# app.config['TESTING'] = True
# # app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# app.debug = True
# toolbar = DebugToolbarExtension(app)

# # Application
# # Home Page
# @app.route('/')
# def show_board():
#     """Loads Boggle Board and Saves it to Session"""
#     board = boggle_game.make_board()
#     session[CURRENT_BOARD_KEY] = board

   
#     return render_template('start-game.html',
#                            board = board)

# # Game Page
# @app.route('/play')
# def play_game():
#     """Provide Board and Form for Guessing"""
#     board = session[CURRENT_BOARD_KEY]
    
#     return render_template('play-game.html',
#                            board = board)
