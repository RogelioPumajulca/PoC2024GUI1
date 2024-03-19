from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from module_1 import Module1
from module_2 import Module2
import queue
import time


# for detection midule
import os
from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename
from datetime import datetime


#for Phoenix 
from phoenix import Phoenix
from sqlalchemy import text


#for RCA


app = Flask(__name__,
            static_folder='../frontend/static',
            template_folder='../frontend/templates')

app.config.from_object(__name__)


CORS(app, resources={r"/*":{'origins':"*"}})

module1 = Module1()
module1.start()

module2 = Module2()
module2.start()

##set up connection to the db using SQLALCHEMY 
app.config.update(
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:password@localhost/POC2024',
    #SQLALCHEMY_DATABASE_URI='mysql://root:password@localhost/POC2024',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db = SQLAlchemy(app)

class PhoenixEditTabletest(db.Model):

    __tablename__ = 'PhoenixEditTabletest' 
    id = db.Column(db.Integer, primary_key=True)
    syscall = db.Column(db.String(255))


def get_syscalls():
    # Query the first three system calls from the database
    syscalls = PhoenixEditTabletest.query.with_entities(PhoenixEditTabletest.syscall).filter(PhoenixEditTabletest.id.in_([1, 2, 3])).all()
    
    # Extract the syscalls from the query result
    syscalls = [syscall[0] for syscall in syscalls]

    return syscalls



### WEBPAGE/MODULE ROUTES

@app.route('/module1', methods=['GET'])
def get_module1():
    return render_template('module1.html')

@app.route('/module2', methods=['GET'])
def get_module2():
    return render_template('module2.html')

@app.route('/detectionmodule', methods=['GET'])
def get_detectionmodule():
    display_text=""
    return render_template('detectionmodule.html', text_box=display_text)

@app.route('/phoenix', methods=['GET'])
def get_phoenixmodule():
    return render_template('phoenix.html')

@app.route('/sareh1', methods=['GET'])
def get_sareh_poi():
    return render_template('sareh1.html')




### API/BACKEND ROUTES GO HERE

@app.route('/api/module1', methods=['GET'])
def get_module1_status():
    return {"counter": module1.get_stdout(), "alerts": module1.alerts}

@app.route('/api/module2', methods=['GET'])
def get_module2_status():
    return {"counter": module2.get_stdout(), "alerts": module2.alerts}



@app.route('/api/phoenix',methods=['GET'])
def send_syscalls():
    syscalls = get_syscalls()
    #return render_template('phoenix.html', syscalls=syscalls)
    print(syscalls)
    return jsonify({'syscalls': syscalls})



### Table form route
@app.route('/api/alerts', methods=['POST'])
def process_alert_table():
    data = request.json
    result = []
    for alert in data['selectedAlerts']:
        if alert['severity'] == 'High':
            result.append(module1.treat_alert(alert))
        elif alert['severity'] == 'Medium':
            result.append(module2.treat_alert(alert))
    return "Alerts processed", 200






### DATABASE ROUTES GO HERE 

#phoenix function to place data in db when the save button is pressed
@app.route('/api/save_data', methods=['POST'])
def save_data():
    data = request.get_json()
    print('Received data:', data)
    
    try:
        syscall = data['syscall']
        action = data['action']
        uploaddate = data['date']

        print(syscall)
        print(action)
        print(uploaddate)


        # Using parameterized query to safely insert data into the database
        with db.engine.connect() as connection:
            query = text("INSERT INTO POC2024.PhoenixEditTabletest (syscall, action, uploaddate) VALUES (:syscall, :action, :uploaddate)")
            connection.execute(query, {"syscall": syscall, "action": action, "uploaddate": uploaddate})
            connection.commit()
               
            
        
        return jsonify({"message": "Data saved successfully"})
    except KeyError as e:
        return jsonify({"error": f"Missing key in JSON data: {e}"})
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})










##upload josn file 
class SystemCall(db.Model):
    __tablename__ = 'PhoenixJsonFile' 
    id = db.Column(db.Integer, primary_key=True)
    syscall = db.Column(db.String(255))
    action = db.Column(db.String(255))
    process = db.Column(db.String(255))
    args = db.Column(db.JSON)
    filename = db.Column(db.String(255))  # Add filename attribute


@app.route('/api/upload_data', methods=['POST'])
def upload_data():
    data = request.json
    #filename = request.headers.get('Content-Disposition').split('filename=')[1]  # Get the filename from request headers
    try:


        filename = request.headers.get('Content-Disposition')
        if filename:
            filename = filename.split('filename=')[1].strip()  # Get the filename from request headers
        else:
            filename = 'unknown_filename'  # Provide a default filename if Content-Disposition header is not present

        
        syscall = data['syscall']
        action = data['action']
        process = data['process']
        args = data['args']
        
        # Create a new SystemCall object and add it to the database
        new_syscall = SystemCall(syscall=syscall, action=action, process=process, args=args, filename=filename)
        db.session.add(new_syscall)
        db.session.commit()
        
        return jsonify({"message": "Data uploaded successfully"})
    except KeyError as e:
        return jsonify({"error": f"Missing key in JSON data: {e}"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})   














# for detection module uploading csv
app.config['UPLOAD_EXTENSIONS'] = ['.csv']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/detectionmodule', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    new_filename = f'{filename.split(".")[0]}_{str(datetime.now())}.csv'
    display_text = str(filename) + " uploaded"
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], new_filename))
    return render_template('detectionmodule.html', text_box = display_text)
    # return redirect(url_for('get_detectionmodule'))


@app.route('/detectionmodule', methods=['GET'])
def apply():
    display_text = "Detection Metrics"
    return render_template('detectionmodule.html', text_box = display_text)




### MAIN ROUTE

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', flaskGreeting="Hello from Flask")


## Static file route, use to serve static JS, CSS, and HTML
@app.route('/<path:filename>', methods=['GET', 'POST'])
def send_static(filename):
  return app.send_static_file(filename)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)