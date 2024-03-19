import subprocess
import threading
import queue
import time

class Module2(threading.Thread):
    def __init__(self):
        self.stdout = queue.Queue()
        threading.Thread.__init__(self)
        self.alerts = []

    def start(self):
        print("Starting Module 2")
        print("It just counts from 5 to 10 and goes back to 5")

        program = '''sh modules/module2.sh'''
        cmd = f"{program}"

        p = subprocess.Popen(cmd.split(),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        
        t = threading.Thread(target=enqueue_stdout, args=(p.stdout, self.stdout), daemon=True)
        t.start()

    def get_stdout(self):
        try: line = self.stdout.get_nowait()
        except queue.Empty:
            print('No output')
        else:
            return line.decode('utf-8').strip()


    def treat_alert(self, alert):
        print(f"Module 2 treating alert: {alert}")
        self.alerts.append(alert)
    
def enqueue_stdout(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()