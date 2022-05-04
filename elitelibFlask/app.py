from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import os
from os.path import join, dirname, realpath
from model.Music import Music
from model.User import User
# from Validation.Validator import *

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

# home page
@app.route('/')
@app.route("/index")
@app.route("/home")
def sanityCheck():
    return render_template("index.html", title="Band Library Catalogue")
    # return "Hello World"

# ADMIN Tools
@app.route('/admin')
# @validateJWTToken
# @requireAdmin
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

# delete music page
@app.route('/deletemusic')
def deleteSelectionPage():
    return render_template("deletemusic.html", title="Condemn Sheet Music")

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



######################################################

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
        print(catID)
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
@app.route('/search/title',methods=['GET'])
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
@app.route('/search/comparr',methods=['GET'])
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
@app.route('/search/publisher',methods=['GET'])
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
@app.route('/search/feat',methods=['GET'])
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



# INSERT new music [not tested]
@app.route('/newmusic', methods=['POST'])
def insertMusic():
    try:
        jsonMusic = request.json
        rows = Music.insertMusic(jsonMusic)
        if rows > 0:
            flash("Music inserted successfully", "info")
        output = {"Music Inserted": rows}
        return jsonify(output), 201     # Successful creation
    except Exception as err:
        print(err)
        return {},500


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


# available boxes in given category
@app.route('/emptyboxes/<catNo>')
def getEmptyBoxes(catNo):
    try:
        boxList = Music.getEmptyBoxes(catNo)
        output = {"Boxes": boxList}
        return jsonify(output), 200     # OK
    except Exception as err:
        print(err)
        return {}, 500      # internal server error


###########################################
# USERS

# Log in page
@app.route('/login')
def Login():
    return render_template("login.html", title="Librarian Login")

# # ISSUE JWTs / LOGIN
# @app.route('/users/login', methods=['POST']) # POST as token creation
# def loginUser():
#     try:
#         jsonUser = request.json
#         email = jsonUser['email']
#         password = jsonUser['password']
#         jwtToken = User.loginUser(email, password)
#         output = {"JWT": jwtToken}
#         return jsonify(output), 200     # Successful creation
#     except Exception as err:
#         print(err)
#         return {},500

