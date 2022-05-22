from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session, send_file
from flask_session import Session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import datetime
import csv
from model.Music import Music
from model.User import User

app = Flask(__name__)
app.config.from_pyfile('config/Settings.py')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)

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
def admin():
    return render_template("admin.html", title="Librarian Admin Tools")

# about
@app.route('/about')
def about():
    return render_template("about.html", title="Band Digitalization Team 2022", team=["ME2-2 Joe Tan", "ME1-2 Ng Wee Seng", "ME1-2 Vignesh", "ME1-2 Gerald Lim", "ME1-2 Kenneth Low"])

# print format
@app.route('/print')
def printFormat():
    return render_template("print.html", title="Print Search Results")

# database reset form
@app.route('/dbimport')
def importDatabaseForm():
    if not session.get('username'):
        return redirect('/login')
    return render_template("resetdb.html", title="Reset Database")

# bulk entry form
@app.route('/bulkentry')
def bulkEntryForm():
    if not session.get('username'):
        return redirect('/login')
    return render_template("bulkentry.html", title="Bulk Entry into Database")


# form for Inserting new music
@app.route('/newmusic')
def newMusicForm():
    if not session.get('username'):
        return redirect('/login')
    return render_template("insertmusic.html", title="Insert New Music Into Catalogue")

# form for deleting music
@app.route('/deletemusic')
def deleteMusicForm():
    if not session.get('username'):
        return redirect('/login')
    return render_template("deletemusic.html", title="Condemn Sheet Music")

# form for editing music
@app.route('/editmusic')
def editMusicForm():
    if not session.get('username'):
        return redirect('/login')
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
    if not session.get('username'):
        return redirect('/login')
    try:
        jsonMusic = request.form
        rows = Music.insertMusic(jsonMusic)
        if rows > 0:
            flash("Music inserted successfully", "success")
        output = {"Music Inserted": rows}
        return jsonify(output), 201     # Successful creation
    except Exception as err:
        print(err)
        return {},500

##################################################
# READ
# Print format of whole database
@app.route('/printdb')
def printAllMusic():
    try:
        jsonMusic = Music.getAllMusic()
        return render_template("printdb.html", data=jsonMusic, title="Print Catalogue")
    except Exception as err:
        print(err)
        return {}, 500                  # internal server error

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

# SEARCH music
@app.route('/search')
def searchMusic():
    try:
        searchType = request.args['type']
        query  = request.args['q']

        music = Music.searchMusic(searchType, query)

        if len(music) > 0:
            output = {"Music": music}
            return jsonify(output), 200      # OK
        else:
            output = {}
            return jsonify(output), 404      # Not Found
    except Exception as err:
        print(err)
        return {}, 500       # Internal Server Error



# Check for similar music from same composer
@app.route('/search/similar')
def similarMusic():
    try:
        composer = request.args['composer']
        title = request.args['title']
        music = Music.searchSimilarMusic(composer, title)
        if len(music) > 0:
            output = {"Music": music}
        else:
            output = {}
        return jsonify(output), 200      # OK
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
    if not session.get('username'):
        return redirect('/login')
    try:
        jsonMusic = request.form
        rows = Music.editMusicByCatNo(catNo, jsonMusic)
        if rows > 0:
            flash("Music edited successfully", "success")
        output = {"Music Edited": rows}
        return jsonify(output), 201     # Successful creation
    except Exception as err:
        print(err)
        return {},500


##################################################
#DELETE music by CatNo
@app.route('/music/<catNo>', methods=['DELETE'])
def deleteMusicByCatNo(catNo):
    if not session.get('username'):
        return redirect('/login')
    try:
        rows = Music.deleteMusicByCatNo(catNo)
        if rows > 0:
            flash("Music deleted successfully", "success")
        output = {"Rows Affected": rows}
        return jsonify(output), 200
    except Exception as err:
        print(err)
        return {}, 500



##############################################################

# Reset database by inputting a csv file
# Set upload folder
UPLOAD_FOLDER = '/home/elitelib22/mysite/importedfiles/'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

# check uploaded file for allowed ext
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/dbimport', methods=['POST'])
def dbimport():
    # redirect if not logged in
    if not session.get('username'):
        return redirect('/login')

    try:
        # GET FILE
        uploadedFile = request.files['file']
        secureFilename = secure_filename(uploadedFile.filename)
        if uploadedFile.filename != '' and allowed_file(uploadedFile.filename):
            # set the file path
            global filepath
            filepath = UPLOAD_FOLDER + secureFilename
            # SAVE FILE
            uploadedFile.save(filepath)
            print("File Uploaded - " + secureFilename)
            flash('File Uploaded. Reading...', 'success')
        else:
            flash('Filename Error.', 'error')
            return render_template('admin.html')
    except Exception as err:
        print(err)
        flash(err, 'error')
        return render_template('admin.html')

    # OPEN CSV FILE
    try:
        file = open(filepath, 'r')
        data = file.readlines()
        linecount = len(data)-1 # minus header
        flash(str(linecount)+' Entries Received.', 'info')
        # Rebuild DB with new data
        rows = Music.resetDB(data)
        flash('Database Rebuilt. '+str(rows)+' Entries Inserted.', 'success')
        return render_template('index.html'), 201
    except Exception as err:
        print(err)
        flash(err, 'error')
        return render_template('admin.html')
    finally:
        file.close()            # IMPT




# EXPORT CSV FILE
@app.route('/dbexport')
def dbexport():
    # redirect if not logged in
    if not session.get('username'):
        return redirect('/login')
    # set filename
    todayDate = datetime.datetime.now()
    todayDate = todayDate.strftime("%d%m%y")
    filename = "LibCatalog" + todayDate + ".csv"
    filepath = "/home/elitelib22/mysite/forexport/"+filename
    headers = ['Catalogue No','Title','Composer','Arranger','Publisher','Featured Instrument','Ensemble Type','Parts','Remarks']
    try:
        data = Music.getAllMusic()

        # make data into csv file
        f = open(filepath, 'w')
        # make csv writer
        writer = csv.writer(f)
        # input header & data
        writer.writerow(headers)
        writer.writerows(data)
        # IMPT
        f.close()
        return send_file(filepath, mimetype='document',attachment_filename=filename, as_attachment=True)

    except Exception as err:
        print(err)
        return {},500




# Bulk Entry by CSV File
# Set upload folder
UPLOAD_FOLDER = '/home/elitelib22/mysite/importedfiles/'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

@app.route('/bulkentry', methods=['POST'])
def bulkEntry():
    # redirect if not logged in
    if not session.get('username'):
        return redirect('/login')

    try:
        # GET FILE
        uploadedFile = request.files['file']
        secureFilename = secure_filename(uploadedFile.filename)
        if uploadedFile.filename != '' and allowed_file(uploadedFile.filename):
            # set the file path
            global filepath
            filepath = UPLOAD_FOLDER + secureFilename
            # SAVE FILE
            uploadedFile.save(filepath)
            print("File Uploaded - " + secureFilename)
            flash('File Uploaded. Reading...', 'success')
        else:
            flash('Filename Error.', 'error')
            return render_template('admin.html')
    except Exception as err:
        print(err)
        flash(err, 'error')
        return render_template('admin.html')

    # OPEN CSV FILE
    try:
        file = open(filepath, 'r')
        data = file.readlines()
        linecount = len(data)-1 # minus header
        flash(str(linecount)+' Entries Received.', 'info')
        # Rebuild DB with new data
        rows = Music.bulkEntry(data)
        flash(str(rows)+' Entries Inserted.', 'success')
        return render_template('index.html'), 201
    except Exception as err:
        print(err)
        flash(err, 'error')
        return render_template('admin.html')
    finally:
        file.close()            # IMPT



###########################################
# USERS

# LOG IN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", title="Librarian Login")
    elif request.method == 'POST':
        userJson = request.form
        username = userJson['username']
        password = userJson['password']
        try:
            auth = User.loginUser(username, password)
            if auth:
                session['username'] = username
                flash('Welcome back, Supreme Leader.', 'success')
                return redirect('/admin')
        except Exception as err:
            print(err)
            return {}, 500

# LOG OUT
@app.route('/logout')
def logout():
    session['username'] = None
    return redirect('/')

###########################################
