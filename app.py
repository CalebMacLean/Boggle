# Imports
from boggle import Boggle
from flask import Flask, render_template, redirect, request, session, flash 
from flask_debugtoolbar import DebugToolbarExtension

# Application Configurations and Global Features
boggle_game = Boggle()
app = Flask(__name__)

CURRENT_BOARD_KEY = 'current_board'

app.config['SECRET_KEY'] = 'CanY0uGue551t'
app.config['TESTING'] = True
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.debug = True
toolbar = DebugToolbarExtension(app)

# Application
# Home Page
@app.route('/')
def show_board():
    """Loads Boggle Board and Saves it to Session"""
    board = boggle_game.make_board()
    session[CURRENT_BOARD_KEY] = board

   
    return render_template('start-game.html',
                           board = board)
