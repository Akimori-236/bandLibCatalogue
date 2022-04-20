from flask import Flask, request, jsonify, render_template
from model.Music import Music

app = Flask(__name__)

# home page
@app.route('/')
@app.route("/index")
@app.route("/home")
def sanityCheck():
    return render_template("index.html", title="SAF Band Library")
    # return "Hello World"

# # ERRORS
@app.errorhandler(500)
def error500(e):
    print(e)
    return render_template("500.html"), 500

@app.errorhandler(404)
def error404(e):
    print(e)
    return render_template("404.html"), 404

###########################################

# GET all Music
@app.route('/music')
def getAllMusic():
    try:
        jsonMusic = Music.getAllMusic()
        output = {"Music": jsonMusic}
        return jsonify(output), 200     # OK
    except Exception as err:
        print(err)
        return {}, 500      # internal server error


# GET one music by musicID
@app.route('/music/<int:musicID>')
def getOneMusic(musicID):
    try:
        jsonMusic = Music.getMusicByID(musicID)

        if len(jsonMusic)>0:
            output = {"Music": jsonMusic}
            return jsonify(output), 200     # OK
        else:
            output = {}
            return jsonify(output), 404     # Not found
    except Exception as err:
        print(err)
        return {}, 500      # internal server error


# SEARCH music by title
@app.route('/search/title',methods=['GET'])
def searchMusicByTitle():
    try:
        substring = request.args['substring']   # will be request.form for POST method
        music = Music.searchMusicByTitle(substring)
        if len(music) > 0:
            output = {"Music": music}
            return jsonify(output), 200      # OK
        else:
            output = {}
            return jsonify(output), 404      # Not Found
    except Exception as err:
        print(err)
        return {}, 500       # Internal Server Error


# INSERT new music
@app.route('/music', methods=['POST'])
def insertMusic():
    try:
        jsonMusic = request.json
        rows = Music.insertMusic(jsonMusic)
        output = {"Music Inserted": rows}
        return jsonify(output), 201     # Successful creation
    except Exception as err:
        print(err)
        return {},500


#DELETE music with specified musicid
@app.route('/music/<int:musicid>',methods=['DELETE'])
# @requireAdmin
def deleteMusic(musicid):
    try:
        rows = Music.deleteMusic(musicid)
        output = {"Rows Affected": rows}
        return jsonify(output), 200
    except Exception as err:
        print(err)
        return {}, 500


