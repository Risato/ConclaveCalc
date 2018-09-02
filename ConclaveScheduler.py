
# coding: utf-8

# # Required Scripts

# In[ ]:

import os
import pandas as pd
import numpy as np

from pandas import ExcelWriter
from pandas import ExcelFile


# In[ ]:

dirs = os.listdir('.') 

# This will print all the files and directories
for file in dirs:
    print file

registration = None
while registration not in dirs:
    registration = raw_input("Please enter Registration File: ")

reginput = pd.read_excel(registration, sheetname='Registration')


# In[3]:

# Check to see if partners are listed in competitor list
reginput = reginput.dropna(subset=['Competitor'])

#Scan for Errors
names = reginput['Competitor']

#if error, return error margins for judge to fix
errorname = 0
for individuals in reginput['Double'].dropna():
    if individuals not in names.tolist():
        print 'Double Buck partner error: ' + individuals
        errorname = errorname + 1
        
for individuals in reginput['Pulp'].dropna():
    if individuals not in names.tolist():
        print 'Pulp Toss partner error: ' + individuals
        errorname = errorname + 1
        
for individuals in reginput['JackJill'].dropna():
    if individuals not in names.tolist():
        print 'Jack and Jill partner error: ' + individuals
        errorname = errorname + 1
    
if errorname > 0:
    print 'You have ' + str(errorname) + ' issues to resolve'
#     exit()


# # Generate Schedule

# In[4]:

teamswitch = None
options = ['COLLEGIATE', 'PROFESSIONAL']
while teamswitch not in options:
    teamswitch = raw_input("Is this for a COLLEGIATE or PROFESSIONAL competition? Enter answer in all caps. ")


# In[5]:


event_Hard = reginput[reginput['Hard'].notnull()]

event_Speed = reginput[reginput['Speed'].notnull()]

event_VHard = reginput[reginput['V Hard'].notnull()]

event_VSpeed = reginput[reginput['V Speed'].notnull()]

event_Single = reginput[reginput['Single'].notnull()]

event_OP = reginput[reginput['OP'].notnull()]

event_Psaw = reginput[reginput['Psaw'].notnull()]

event_Pulp = reginput[reginput['Pulp'].notnull()]

event_Double = reginput[reginput['Double'].notnull()]

event_JackJill = reginput[reginput['JackJill'].notnull()]

event_Climb = reginput[reginput['Climb'].notnull()]

event_Choker = reginput[reginput['Choker'].notnull()]

event_SpeedAxe = reginput[reginput['SpeedAxe'].notnull()]

event_Axe = reginput[reginput['Axe'].notnull()][['School', 'Team', 'Competitor', 'Gender']]
event_Axe['Throw 1'], event_Axe['Throw 2'], event_Axe['Throw 3'], event_Axe['Score'] = [np.nan, np.nan, np.nan, sum]

event_Caber = reginput[reginput['Caber'].notnull()]

event_Dendro = reginput[reginput['Dendro'].notnull()]

event_Traverse = reginput[reginput['Traverse'].notnull()]


# In[6]:

event_Axe


# In[7]:

list(reginput)


# In[8]:

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

# Assigns points based on whether events are run separately for men and women
gender_split = ['Dendro', 'Traverse', 'Cruise']

# Assigns whether or not events have a partner
partner_split = ['Double', 'JackJill', 'Caber']


# In[9]:

scores = pd.DataFrame()

for key, value in df.iteritems() :
    
    if key in gender_split:
        temp = rawinput[key].dropna(subset=['Contestant'])
        tempN = temp.sort_values('Score',ascending = pt_order[key]).reset_index(drop=True)
        # Assign rank to competitor names
        tempN['Rank'] = tempN.index + 1
        # Assign point values to rank
        tempN['Points'] = tempN.Rank.map(rankswap)
        tempN = tempN[tempN['Points'] >0]
        tempN['Event'] = key
        scores = tempN.append(scores)
#         print key
    
    else:
        # Clean Input Data
        temp = rawinput[key].dropna(subset=['Contestant'])
    
        # Sort based on correlated rank
        tempM = temp[temp['Gender']=='M'].sort_values('Score',ascending = pt_order[key]).reset_index(drop=True)
        # Assign rank to competitor names
        tempM['Rank'] = tempM.index + 1
        # Assign point values to rank
        tempM['Points'] = tempM.Rank.map(rankswap)
        tempM = tempM[tempM['Points'] >0]
        tempM['Event'] = key
        scores = tempM.append(scores)
#         print key + '-M'
        
        # Sort based on correlated rank
        tempF = temp[temp['Gender']=='F'].sort_values('Score',ascending = pt_order[key]).reset_index(drop=True)
        # Assign rank to competitor names
        tempF['Rank'] = tempF.index + 1
        # Assign point values to rank
        tempF['Points'] = tempF.Rank.map(rankswap)
        tempF = tempF[tempF['Points'] >0]
        tempF['Event'] = key
        scores = tempF.append(scores)
#         print key + '-F'


# In[ ]:

# Clean output
# Weigh scores in partner events
scores['multiplier'] = np.where(scores['Contestant B'].notnull(), 0.5, 1)
scores['Points'] = scores['multiplier']*scores['Points']
scores = scores[['Contestant', 'Gender', 'Contestant B', 'Gender B', 'Event', 'Team', 'School', 'Points', 'Rank']]

# isolate partners
partners = scores[scores['Contestant B'].notnull()]
partners.drop(['Contestant', 'Gender'], axis=1, inplace=True)
partners.rename(columns={'Contestant B': 'Contestant', 'Gender B': 'Gender'}, inplace=True)

# Clean remaining results from contestants
contestants = scores
contestants.drop(['Contestant B', 'Gender B'], axis=1, inplace=True)

# Recombine competitors and partners into final scoresheet
scores = contestants.append(partners)


# # Print Results

# In[ ]:

# Print Top 3 in each event
print scores[scores['Rank']<=3].sort_values(['Event', 'Gender', 'Rank'])


# In[ ]:

# Print "Bull" and "Bell" of the woods
report = scores.groupby(['Contestant', 'School', 'Team','Gender'],  as_index=False).sum().sort_values('Points', ascending = False)

print 'Bull'
print report[report['Gender'] == 'M'].reset_index(drop = True).loc[0]
print '\n'
print 'Bell'
print report[report['Gender'] == 'F'].reset_index(drop = True).loc[0]


# In[ ]:

# Print Team Rankings
report = scores.groupby(['School', 'Team'],  as_index=False).sum().sort_values('Points', ascending = False)
print report  


# In[ ]:



