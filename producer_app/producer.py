import sys
import json
import time
import random

with open("./config.json", "r+") as fp:
  config = json.load(fp)


class Event(object):
  def __init__(self, ev_type, data):
    self.type = ev_type
    self.data = data
    self.ts = time.time()

  def __str__(self):
    if random.random() < 0.1:
      return f'{"".join([chr(random.randint(0,255)) for i in range(0, 10)])}'
    else:
      return f'{{ "event_type": "{self.type}", "data": "{self.data}", "timestamp": {int(self.ts)} }}'


while True:
  for i in range(random.randint(1,5)):
    print(Event(random.choice(config.get("event_types")),
                random.choice(config.get("data"))))
    time.sleep(random.random()*3)