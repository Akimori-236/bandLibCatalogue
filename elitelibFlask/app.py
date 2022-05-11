from flask import Flask, request, jsonify, render_template, g, redirect, url_for, flash
import os
from model.Music import Music
from model.User import User
from config.Settings import Settings
import functools
import jwt
import re

app = Flask(__name__)
app.config.from_pyfile('config/Settings.py')

if __name__ == "__main__":
    app.run(debug=True)



##################################################
# VALIDATOR WRAPPERS
def requireLogin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #BEFORE
        auth = False
        output = []
        auth_header = request.headers.get("Authorization")

        if auth_header:
            jwtToken = auth_header.split(" ")[1] # Select Token itself
            print("JWT TOKEN: " + jwtToken)
        else:
            jwtToken = None

        if jwtToken: # if there is a JWT Token
            try:
                payload = jwt.decode(jwtToken, Settings.SECRET_KEY, algorithms="HS256") #decode Token with Key by Algo
                auth = True # Decoding was successful

                username = payload['username']
                userid = payload['userid']
                g.username = username
                g.userid = userid
            except (jwt.InvalidSignatureError, jwt.ExpiredSignatureError) as err:
                print(err)
                output.append(err)

        if auth == False:
            # output = {"Message": "Please log in."}
            # return jsonify(output), 400
            output.append("Unauthorized Access: Please log in.")
            return render_template("index.html", errors=output), 401 # not logged in


        value = func(*args, **kwargs)
        return value
        #AFTER
    return wrapper
##################################################



# home page
@app.route('/')
@app.route("/index")
@app.route("/home")
def sanityCheck():
    return render_template("index.html", title="Band Library Catalogue")
    # return "Hello World"

# ADMIN Tools
@app.route('/admin')
@requireLogin
def admin():
    return render_template("admin.html", title="Librarian Admin Tools")

# about
@app.route('/about')
def about():
    return render_template("about.html", title="Band Digitalization Team 2022", team=["ME2-2 Joe Tan", "ME1-2 Ng Wee Seng", "ME1-2 Vignesh", "ME1-2 Gerald Lim", "ME1-2 Kenneth Low"])

# upload csv form
@app.route('/uploadcsv')
def uploadCSV():
    return render_template("uploadcsv.html", title="Restore Database")

# form for Inserting new music
@app.route('/newmusic')
def newMusicForm():
    return render_template("insertmusic.html", title="Insert New Music Into Catalogue")

# form for deleting music
@app.route('/deletemusic')
def deleteMusicForm():
    return render_template("deletemusic.html", title="Condemn Sheet Music")

# form for editing music
@app.route('/editmusic')
def editMusicForm():
    return render_template("editmusic.html", title="Edit Catalogue")

#######################
# # ERRORS
@app.errorhandler(500)
def error500(e):
    print(e)
    return render_template("500.html"), 500

@app.errorhandler(404)
def error404(e):
    print(e)
    return render_template("404.html"), 404



##################################################
# CREATE
# INSERT new music
@app.route('/newmusic', methods=['POST'])
def insertMusic():
    try:
        jsonMusic = request.form
        rows = Music.insertMusic(jsonMusic)
        if rows > 0:
            flash("Music inserted successfully", "info")
        output = {"Music Inserted": rows}
        return jsonify(output), 201     # Successful creation
    except Exception as err:
        print(err)
        return {},500

##################################################
# READ
# GET all Music [keep for csv exporting for db backup]
@app.route('/music')
def getAllMusic():
    try:
        jsonMusic = Music.getAllMusic()
        output = {"Music": jsonMusic}
        return jsonify(output), 200     # OK
    except Exception as err:
        print(err)
        return {}, 500      # internal server error


# # GET music by category
@app.route('/category/<int:catID>')
def getMusicByCatID(catID):
    try:
        jsonMusic = Music.getMusicByCatID(catID)
        if len(jsonMusic)>0:
            output = {"Music": jsonMusic}
            return jsonify(output), 200     # OK
        else:
            output = {}
            return jsonify(output), 404     # Not found
    except Exception as err:
        print(err)
        return {}, 500      # internal server error


# # GET music by ensemble type
@app.route('/ensemble/<ensemble>')
def getMusicByEnsembleType(ensemble):
    try:
        jsonMusic = Music.getMusicByEnsembleType(ensemble)
        if len(jsonMusic)>0:
            output = {"Music": jsonMusic}
            return jsonify(output), 200     # OK
        else:
            output = {}
            return jsonify(output), 404     # Not found
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


# GET one music by catNo
@app.route('/music/catno/<catNo>')
def getMusicByCatNo(catNo):
    try:
        jsonMusic = Music.getMusicByCatNo(catNo)

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
@app.route('/search/title')
def searchMusicByTitle():
    try:
        query = request.args['q']           # use request.form for POST method
        music = Music.searchMusicByTitle(query)
        if len(music) > 0:
            output = {"Music": music}
            return jsonify(output), 200      # OK
        else:
            output = {}
            return jsonify(output), 404      # Not Found
    except Exception as err:
        print(err)
        return {}, 500       # Internal Server Error

# SEARCH music by composer/arranger
@app.route('/search/comparr')
def searchMusicByCompArr():
    try:
        query = request.args['q']           # use request.form for POST method
        music = Music.searchMusicByCompArr(query)
        if len(music) > 0:
            output = {"Music": music}
            return jsonify(output), 200      # OK
        else:
            output = {}
            return jsonify(output), 404      # Not Found
    except Exception as err:
        print(err)
        return {}, 500       # Internal Server Error

# SEARCH music by publisher
@app.route('/search/publisher')
def searchMusicByPublisher():
    try:
        query = request.args['q']           # use request.form for POST method
        music = Music.searchMusicByPublisher(query)
        if len(music) > 0:
            output = {"Music": music}
            return jsonify(output), 200      # OK
        else:
            output = {}
            return jsonify(output), 404      # Not Found
    except Exception as err:
        print(err)
        return {}, 500       # Internal Server Error

# SEARCH music by Featured Instrument
@app.route('/search/feat')
def searchMusicByFeatInstru():
    try:
        query = request.args['q']           # use request.form for POST method
        music = Music.searchMusicByFeatInstru(query)
        if len(music) > 0:
            output = {"Music": music}
            return jsonify(output), 200      # OK
        else:
            output = {}
            return jsonify(output), 404      # Not Found
    except Exception as err:
        print(err)
        return {}, 500       # Internal Server Error

# GET boxes in given category
@app.route('/boxes/<catNo>')
def getEmptyBoxes(catNo):
    try:
        boxList = Music.getBoxes(catNo)
        output = {"Boxes": boxList}
        return jsonify(output), 200     # OK
    except Exception as err:
        print(err)
        return {}, 500      # internal server error


##################################################
# UPDATE
# EDIT EXISTING MUSIC
@app.route('/music/<catNo>', methods=['PUT'])
def editMusicByCatNo(catNo):
    try:
        jsonMusic = request.form
        rows = Music.editMusicByCatNo(catNo, jsonMusic)
        if rows > 0:
            flash("Music edited successfully", "info")
        output = {"Music Edited": rows}
        return jsonify(output), 201     # Successful creation
    except Exception as err:
        print(err)
        return {},500


##################################################
#DELETE music by CatNo
@app.route('/music/<catNo>', methods=['DELETE'])
# @requireAdmin
def deleteMusicByCatNo(catNo):
    try:
        rows = Music.deleteMusicByCatNo(catNo)
        if rows > 0:
            flash("FlashMsg: Music deleted successfully", "success")
        output = {"Rows Affected": rows}
        return jsonify(output), 200
    except Exception as err:
        print(err)
        return {}, 500



##############################################################

# Restore database by inputting a csv file [not working]
# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/uploadcsv', methods=['POST'])
def restoreDB():
    try:
        # get the uploaded file
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
            # save the file
            return redirect(url_for('index'))

        rows = Music.DBReset(uploaded_file)
        output = {"Music Inserted": rows}
        return jsonify(output), 201     # Successful creation
    except Exception as err:
        print(err)
        return {},500





###########################################
# USERS

# Log in page
@app.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'GET':
        return render_template("login.html", title="Librarian Login")
    elif request.method == 'POST':
        try:
            jsonUser = request.form
            username = jsonUser['username']
            password = jsonUser['password']
            jwtToken = User.loginUser(username, password)
            output = {'JWT' : jwtToken}
            return jsonify(output), 200
        except Exception as err:
            print(err)
            return {}, 500

###########################################
