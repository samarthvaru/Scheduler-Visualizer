from flask import Flask, render_template, request, jsonify
import queue
import threading
import time

app = Flask(__name__)

# Define the process class
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time

# Define scheduling algorithms
def round_robin(processes, quantum, result_queue, completion_event):
    time_elapsed = 0
    while processes:
        for process in list(processes):
            if process.arrival_time <= time_elapsed:
                run_time = min(quantum, process.burst_time)
                process.burst_time -= run_time
                result_queue.put(process.pid)
                print(f"Processing process {process.pid} for {run_time} units")
                time.sleep(0.5)  # Simulate processing time
                if process.burst_time <= 0:
                    processes.remove(process)
            time_elapsed += 1
    completion_event.set()  # Signal completion

def fifo(processes, result_queue, completion_event):
    for process in processes:
        print(f"Processing process {process.pid} for {process.burst_time} units")
        time.sleep(process.burst_time)  # Simulate processing time
        result_queue.put(process.pid)
    completion_event.set()  # Signal completion

def sjf(processes, result_queue, completion_event):
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    for process in processes:
        print(f"Processing process {process.pid} for {process.burst_time} units")
        time.sleep(process.burst_time)  # Simulate processing time
        result_queue.put(process.pid)
    completion_event.set()  # Signal completion

def uni_programming(processes, result_queue, completion_event):
    for process in processes:
        print(f"Processing process {process.pid} for {process.burst_time} units")
        time.sleep(process.burst_time)  # Simulate processing time
        result_queue.put(process.pid)
    completion_event.set()  # Signal completion

# Define route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Define route for scheduling endpoint
@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.json
    processes_data = data['processes']
    algorithm = data['algorithm']
    quantum = int(data.get('quantum', 1))  # For Round Robin only
    processes = [Process(int(p['pid']), int(p['arrival_time']), int(p['burst_time'])) for p in processes_data]

    result_queue = queue.Queue()
    completion_event = threading.Event()  # Event to signal completion

    if algorithm == 'round_robin':
        threading.Thread(target=round_robin, args=(processes, quantum, result_queue, completion_event)).start()
    elif algorithm == 'fifo':
        threading.Thread(target=fifo, args=(processes, result_queue, completion_event)).start()
    elif algorithm == 'sjf':
        threading.Thread(target=sjf, args=(processes, result_queue, completion_event)).start()
    elif algorithm == 'uni_programming':
        threading.Thread(target=uni_programming, args=(processes, result_queue, completion_event)).start()

    # Wait for completion before returning the result
    completion_event.wait()

    result = []
    while not result_queue.empty():
        result.append(result_queue.get())

    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)
