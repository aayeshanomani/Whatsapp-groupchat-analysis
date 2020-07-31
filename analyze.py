import pandas as pd
import numpy as np
import re
import dateparser
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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

#print(df['Content'])
plt.figure(1)
wordfreq = dict()

for con in df['Content']:
  #print(con)
  
  con = con.split()
  for i in con:
    wordfreq[i] = wordfreq.get(i,0) + 1

k = Counter(wordfreq)
high = k.most_common(10)
D = dict()
for i,j in high:
  D[i] = j
plt.bar(range(len(D)), list(D.values()), align='center',color='xkcd:lime')
plt.xticks(range(len(D)), list(D.keys()))
ax = plt.gca()
ax.set_facecolor('xkcd:black')
title = 'Most Common Words in '+file.split('.')[0]
plt.title(title)
plt.xlabel('Words')
plt.ylabel('Frequency')

# # for python 2.x:
# plt.bar(range(len(D)), D.values(), align='center')  # python 2.x
# plt.xticks(range(len(D)), D.keys())  # in python 2.x
fig1 = plt.gcf()
#plt.show()
fig1.savefig(title+'.png')
#plt.clf()

plt.figure(2)
wordfreq = dict()
for con in df['Name']:
  #print(con)
  wordfreq[con] = wordfreq.get(con,0) + 1

k = Counter(wordfreq)
high = k.most_common(10)
#print(high)
D = dict()
for i,j in high:
  D[i] = j
plt.barh(range(len(D)), list(D.values()), align='center',color='xkcd:orange')
plt.yticks(range(len(D)), list(D.keys()))
ax = plt.gca()
ax.set_facecolor('xkcd:dark green')
for tick in ax.yaxis.get_major_ticks():
  tick.label.set_fontsize(10) 
#plt.xticks(rotation=90)
for label in ax.get_xaxis().get_ticklabels()[::2]:
    label.set_visible(True)
title = 'Most Talkative People in '+file.split('.')[0]
plt.title(title)
plt.xlabel('Messages')
plt.ylabel('People')

# # for python 2.x:
# plt.bar(range(len(D)), D.values(), align='center')  # python 2.x
# plt.xticks(range(len(D)), D.keys())  # in python 2.x
fig2 = plt.gcf()
#plt.show()
fig2.savefig(title+'.png',bbox_inches='tight')
#plt.clf()

day = {
  'Sunday': 0,
  'Monday': 0,
  'Tuesday': 0,
  'Wednesday': 0,
  'Thursday': 0,
  'Friday': 0,
  'Saturday': 0,
}

plt.figure(3)


for con in df['Weekday']:
  #print(con)
  day[con] = day.get(con,0) + 1


plt.bar(range(len(day)), list(day.values()), align='center',color='xkcd:dark red')
plt.xticks(range(len(day)), list(day.keys()))
ax = plt.gca()
ax.set_facecolor('xkcd:gold')
title = 'Active Weekdays in '+file.split('.')[0]
plt.title(title)
plt.xlabel('Weekdays')
plt.ylabel('Messages')
fig3 = plt.gcf()
#plt.show()
fig3.savefig(title+'.png',bbox_inches='tight')

hours = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']

#print(hours)
hdct = {}
for h in hours:
  hdct[h] = 0

plt.figure(4)

for con in df['Hour']:
  #print(con)
  hdct[con] = hdct.get(con,0) + 1


plt.bar(range(len(hdct)), list(hdct.values()), align='center',color='xkcd:brick red')
plt.xticks(range(len(hdct)), list(hdct.keys()))
ax = plt.gca()
ax.set_facecolor('xkcd:blue green')
title = 'Active Hours in '+file.split('.')[0]
plt.title(title)
plt.xlabel('Hours')
plt.ylabel('Messages')
fig3 = plt.gcf()
plt.show()
fig3.savefig(title+'.png',bbox_inches='tight')