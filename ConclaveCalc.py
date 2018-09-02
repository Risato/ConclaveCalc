
# coding: utf-8

# # Required Scripts

# In[1]:

import os
import pandas as pd
import numpy as np

from pandas import ExcelWriter
from pandas import ExcelFile


# In[2]:

# Add Switch for team or semiprofessional event
teamswitch = None
while teamswitch not in ['yes', 'no']:
    teamswitch = raw_input("Do you need to separate competitors by team? ").lower()


# In[3]:

dirs = os.listdir('.') 

# This will print all the files and directories
for file in dirs:
    print file

response = None
while response not in dirs:
    response = raw_input("Please enter filename: ")

# response = 'Bearclave.xlsx'
rawinput = pd.read_excel(response, sheetname=None)


# # Calculate Results

# In[4]:

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


# In[5]:

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


# In[6]:

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

# In[20]:

# Print Top 3 in each event
print scores[scores['Rank']<=3].sort_values(['Event', 'Gender', 'Rank'])


# In[21]:

# Print "Bull" and "Bell" of the woods
report = scores.groupby(['Contestant', 'School', 'Team','Gender'],  as_index=False).sum().sort_values('Points', ascending = False)

print 'Bull'
print report[report['Gender'] == 'M'].reset_index(drop = True).loc[0]
print '\n'
print 'Bell'
print report[report['Gender'] == 'F'].reset_index(drop = True).loc[0]


# In[23]:

# Print Team Rankings
report = scores.groupby(['School', 'Team'],  as_index=False).sum().sort_values('Points', ascending = False)
print report  


# In[ ]:



