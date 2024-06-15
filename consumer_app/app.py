import json
import threading
import time
from collections import defaultdict 
from flask import Flask, jsonify
import os
import select

FIFO = os.environ.get("IPC_PATH", "/tmp/ipc/event_stream.fifo")

if not os.path.exists(FIFO):
    os.mkfifo(FIFO)

class Stats:
    def __init__(self):
        self.event_count = defaultdict(int)
        self.word_count = defaultdict(int)
        self.lock = threading.Lock()

    def update_stats(self, event):
        with self.lock:
            self.event_count[event["event_type"]] += 1
            for word in event["data"].split():
                self.word_count[word] += 1

    def get_event_count(self):
        with self.lock:
            return dict(self.event_count)

    def get_word_count(self):
        with self.lock:
            return dict(self.word_count)

stats = Stats()

def event_consumer():
    with open(FIFO, 'r') as fifo:
        while True:
            line = fifo.readline()
            if line:
                try:
                    event = json.loads(line)
                    stats.update_stats(event)
                except json.JSONDecodeError:
                    continue

consumer_thread = threading.Thread(target=event_consumer)
consumer_thread.setDaemon(True)
consumer_thread.start()

# Flask app
app = Flask(__name__)

@app.route('/events/countByEventType', methods=['GET'])
def count_by_event_type():
    return jsonify(stats.get_event_count())

@app.route('/events/countWords', methods=['GET'])
def count_words():
    return jsonify(stats.get_word_count())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
