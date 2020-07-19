import pandas as pd
import numpy as np
import re
import dateparser
from collections import Counter
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def read_file(file):
    x = open(file, 'r', encoding = 'utf-8')
    y = x.read()
    context = y.splitlines()
    return context

file = input('Enter chat file: ')
chat = read_file(file)
print(len(chat))

join = [line for line in chat if  "joined using this" in line]
print(join)

chat = [line.strip() for line in chat]
print("length of chat is:")
print(len(chat))

clean_chat = [line for line in chat if not "joined using this" in line]

clean_chat = [line for line in clean_chat if len(line) > 1]
print("length of clean_chat is:")
print(len(clean_chat)) 

left = [line for line in clean_chat if line.endswith("left")]
print(left)

clean_chat = [line for line in clean_chat if not line.endswith("left")]
print(len(clean_chat))

msgs = []
pos = 0

for line in clean_chat:
  if re.findall("\A\d+[/]", line):
    msgs.append(line)
    pos += 1
  else:
    take = msgs[pos-1] + ". " + line
    msgs.append(take)
    msgs.pop(pos-1)
print(len(msgs)) 

print(msgs[0:10])

time = [msgs[i].split(',')[1].split('-')[0] for i in range(len(msgs)) if len(msgs[i].split(','))>1]
time = [s.strip(' ') for s in time] # Remove spacing
print("length of time is:")
print(len(time))
#print(time)

date = [msgs[i].split(',')[0] for i in range(len(msgs))]
print(len(date))

name = [msgs[i].split('-')[1].split(':')[0] for i in range(len(msgs))]
len(name)

content = []
for i in range(len(msgs)):
  try:
    content.append(msgs[i].split(':')[2])
  except IndexError:
    content.append('Missing Text')
print(len(content))

df = pd.DataFrame(list(zip(date, time, name, content)), columns = ['Date', 'Time', 'Name', 'Content'])
print(df.head())