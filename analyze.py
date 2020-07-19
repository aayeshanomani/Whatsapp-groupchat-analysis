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

time = [msgs[i].split('-')[0].strip().split(',')[1].strip() for i in range(len(msgs)) if len(msgs[i].split('-')[0].strip().split(','))>1 and ':' in msgs[i].split('-')[0].strip().split(',')[1]]
time = [s for s in time if len(s) == 5]
print(time)
print("length of time is:")
print(len(time))
#print(time)

date = [msgs[i].split('-')[0].strip().split(',')[0] 
  for i in range(len(msgs)) 
  if '/' in msgs[i].split('-')[0].strip().split(',')[0] 
  and len(msgs[i].split('-')[0].strip().split(',')[0]) == 8]
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

df = df[df["Content"]!='Missing Text']
df.reset_index(inplace=True, drop=True)
print(len(df))
print(df[100:])

df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
print(df['DateTime'])

df['Weekday'] = df['DateTime'].apply(lambda x: x.day_name())

df['Letter_Count'] = df['Content'].apply(lambda s : len(s))
df['Word_Count'] = df['Content'].apply(lambda s : len(s.split(' ')))

df['Hour'] = df['Time'].apply(lambda x : x.split(':')[0])

print(df.head())

df.to_csv(file.split('.')[0]+".csv")