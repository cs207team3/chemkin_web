from flask import Flask, flash, render_template, abort, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from flask_socketio import SocketIO, disconnect
import chem3
from chem3.chemkin import *
import os
from werkzeug.contrib.fixers import ProxyFix
 
access_counter = 0

def get_data(filename):
    system = ReactionSystem(filename=filename)

    data = {}
    data['equations'] = []
    data['species'] = system.order
    for reaction in system.reactions:
        data['equations'].append(reaction.equation)
    return data, system

def get_rates(system, T, concs):
    concs = concs.strip().split(',')
    concs = [float(c) for c in concs]
    return system.reaction_rate(concs, float(T))

app = Flask(__name__)
app.secret_key = "super secret key"
UPLOAD_FOLDER = '/uploaded_files/'
ALLOWED_EXTENSIONS = set(['xml'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app)
app.config["CACHE_TYPE"] = "null"

app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('test.html')

# @app.before_request
# def limit_acess():
#     global access_counter
#     if access_counter == 0:
#         print("Hi connect")
#         access_counter += 1
#     else:
#         abort(403)

# @socketio.on('connect')
# def connect_user():
#     global access_counter
#     if access_counter == 0:
#         print("Hi connect")
#         access_counter = 1
#     else:
#         # abort(403)
#         print("Can not go through")
#         render_template('403.html')

# @socketio.on('disconnect')
# def disconnect_user():
#     global access_counter
#     access_counter = 0
#     print('disconnected', access_counter)
#     disconnect()

#-------------------------------- Upload files -------------------------------------------#
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

reaction_data = None
system = None

@app.route('/', methods = ['GET', 'POST'])
def upload_data():
    # print(request.headers)
    print('This is ip:', request.headers.get('X-Forwarded-For', request.remote_addr), file=sys.stderr)
    if request.method == 'POST':
        # This is file upload
        if request.files:
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if allowed_file(file.filename):
                file.save(secure_filename(file.filename))
                flash(file.filename + ' uploaded Successfully!')

                global reaction_data, system
                reaction_data, system = get_data(file.filename)
                print(reaction_data)
                return render_template('test.html', data=reaction_data, scroll='hi')
            else:
                flash('Incorrect file format!')
                return redirect(request.url)

        # This is form upload of T and concs
        if request.form:
            T = request.form['temp']
            concs = request.form['concs']

            if len(T) == 0:
                return render_template('test.html', data=reaction_data, error='Temperature is required!', scroll='hi')
            if len(concs) == 0:
                return render_template('test.html', data=reaction_data, error='Concentration is required!', scroll='hi')
            if reaction_data == None:
                return render_template('test.html', data=reaction_data, error='No reaction system input yet!', scroll='hi')

            try:
                rates = get_rates(system, T, concs)
                species_dic = {}
                for i in range(len(rates)):
                    species_dic[reaction_data['species'][i]] = rates[i]
            except ValueError as e:
                print('Error occured:', e)
                return render_template('test.html', data=reaction_data, error=e.messsage, scroll='hi')

            return render_template('test.html', data=reaction_data, species_dic=species_dic, scroll='hi')
            # return redirect(request.url)
            # return render_template('base.html', t_concs = [T, concs])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    # socketio.run(app, host='0.0.0.0', port=5000, debug=True)