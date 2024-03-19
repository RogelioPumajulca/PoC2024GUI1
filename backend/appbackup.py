from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from module_1 import Module1
from module_2 import Module2
import queue
import time

app = Flask(__name__,
            static_folder='../frontend/static',
            template_folder='../frontend/templates')

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})

module1 = Module1()
module1.start()

module2 = Module2()
module2.start()







### WEBPAGE/MODULE ROUTES

@app.route('/module1', methods=['GET'])
def get_module1():
    return render_template('module1.html')

@app.route('/module2', methods=['GET'])
def get_module2():
    return render_template('module2.html')

@app.route('/detectionmodule', methods=['GET'])
def get_detectionmodule():
    return render_template('detectionmodule.html')

@app.route('/phoenix', methods=['GET'])
def get_detectionmodule():
    return render_template('phoenix.html')






### API/BACKEND ROUTES GO HERE

@app.route('/api/module1', methods=['GET'])
def get_module1_status():
    return {"counter": module1.get_stdout(), "alerts": module1.alerts}

@app.route('/api/module2', methods=['GET'])
def get_module2_status():
    return {"counter": module2.get_stdout(), "alerts": module2.alerts}


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



### MAIN ROUTE

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', flaskGreeting="Hello from Flask")


## Static file route, use to serve static JS, CSS, and HTML
@app.route('/<path:filename>', methods=['GET'])
def send_static(filename):
  return app.send_static_file(filename)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)