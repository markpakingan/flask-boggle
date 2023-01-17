from boggle import Boggle
from flask import Flask, session, render_template, request, jsonify



app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"

boggle_game = Boggle()


@app.route('/')
def create_board():

    """Show the board"""
     
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    no_of_play = session.get("no_of_play", 0)

    return render_template("index.html", board=board,
                           highscore=highscore,
                           no_of_play=no_of_play)

@app.route("/check-word")
def check_word():
    """Check the submitted word from the Dictionary"""

    word = request.args["word"]
    board = session ["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    no_of_play = session.get("no_of_play", 0)

    session['no_of_play'] = no_of_play + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)

