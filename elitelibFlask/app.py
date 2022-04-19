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


# GET one music by catalog number
@app.route('/music/<int:catno>')
def getOneMusic(catno):
    try:
        jsonMusic = Music.getMusicByCatNo(catno)

        if len(jsonMusic)>0:
            output = {"Music": jsonMusic}
            return jsonify(output), 200     # OK
        else:
            output = {}
            return jsonify(output), 404     # Not found
    except Exception as err:
        print(err)
        return {}, 500      # internal server error


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


# SEARCH music by substring
@app.route('/search/music',methods=['GET'])
def getMusicBySubstring():
    try:
        substring = request.args['substring']   # will be request.form for POST method
        music = Music.getMusicBySubstring(substring)
        if len(music) > 0:
            output = {"Music": music}
            return jsonify(output), 200      # OK
        else:
            output = {}
            return jsonify(output), 404      # Not Found
    except Exception as err:
        print(err)
        return {}, 500       # Internal Server Error