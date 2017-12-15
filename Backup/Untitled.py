
# coding: utf-8

# In[820]:

import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


# In[821]:

dirs = os.listdir('.') 

# This will print all the files and directories
for file in dirs:
    print file

# response = None
# while response not in dirs:
#     response = raw_input("Please enter filename: ")
df = pd.read_excel(response, sheetname=None)


# In[822]:

# Assigns rank based on ascending or descending scores
pt_order ={
    'Dendro': False,
    'Traverse': True,
    'Hard': False,
    'Double': True,
    'PSaw': True,
    'Choker': True,
    'Throw': False,
    'Single': True,
    'Caber': True,
    'Climb': False,
    'JackJill': True,
    'Speed': True,
    'Pulp': True,
    'OP': True}

# Assigns points to rankings
rankswap = {1:10, 2:7, 3:5, 4:3, 5:1}

# Assigns points based on whether 
gender_split = ['Dendro', 'Traverse', 'Cruise']

partner_split = ['Double', 'JackJill', 'Caber']

scores = pd.DataFrame()


# In[823]:

for key, value in df.iteritems() :
    
    if key in gender_split:
        temp = df[key].dropna(subset=['Contestant'])
        tempN = temp.sort('Score',ascending = pt_order[key]).reset_index(drop=True)
        # Assign rank to competitor names
        tempN['Rank'] = tempN.index + 1
        # Assign point values to rank
        tempN['Points'] = tempN.Rank.map(rankswap)
        tempN = tempN[tempN['Points'] >0]
        tempN['Event'] = key
        
        scores = tempN.append(scores)
        print key
    
    else:
        # Clean Input Data
        temp = df[key].dropna(subset=['Contestant'])
    
        # Sort based on correlated rank
        tempM = temp[temp['Gender']=='M'].sort('Score',ascending = pt_order[key]).reset_index(drop=True)
        # Assign rank to competitor names
        tempM['Rank'] = tempM.index + 1
        # Assign point values to rank
        tempM['Points'] = tempM.Rank.map(rankswap)
        tempM = tempM[tempM['Points'] >0]
        tempM['Event'] = key
        scores = tempM.append(scores)
        print key + '-M'
        
        # Sort based on correlated rank
        tempF = temp[temp['Gender']=='F'].sort('Score',ascending = pt_order[key]).reset_index(drop=True)
        # Assign rank to competitor names
        tempF['Rank'] = tempF.index + 1
        # Assign point values to rank
        tempF['Points'] = tempF.Rank.map(rankswap)
        tempF = tempF[tempF['Points'] >0]
        tempF['Event'] = key
        scores = tempF.append(scores)
        print key + '-F'


# In[806]:

scores['Contestant B'].append(scores['Contestant'])


# In[807]:

scores


# In[801]:

scores[scores['Rank']==1]
scores[scores['Rank']==2]
scores[scores['Rank']==3]


# In[695]:

list(scores)


# In[701]:

final = scores[['Contestant', 'School', 'Team' , 'Event', 'Gender', 'Points', 'Rank']]


# In[726]:

report = final.groupby(['Contestant', 'School', 'Team','Gender'],  as_index=False).sum().sort('Points', ascending = False)
# print "Bull" + report


# In[789]:

print 'first place'
print report[report['Gender'] == 'M'].reset_index(drop = True).loc[0]

print report[report['Gender'] == 'F'].reset_index(drop = True).loc[0]


# In[793]:

report = final.groupby(['School', 'Team'],  as_index=False).sum().sort('Points', ascending = False)
print report  


# In[819]:

names = pd.concat(df).dropna(subset=['Contestant'])[['Contestant', 'School', 'Team']]
names = names.reset_index(drop = True).drop_duplicates()


# In[ ]:



