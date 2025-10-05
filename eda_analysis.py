import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator
import re

pd.set_option('display.max_info_columns', 200)  


df = pd.read_csv(r'E:\Asir\Project2_FIFA-EDA-analysis\players_22.csv', encoding='latin1', low_memory=False)
df1=pd.read_csv(r'E:\Asir\Project2_FIFA-EDA-analysis\players_19.csv', encoding='latin1')

df1['pace']=df1[['Acceleration', 'SprintSpeed']].mean(axis=1)
df1['shooting']=df1[['Finishing', 'ShotPower', 'LongShots', 'Volleys', 'Penalties']].mean(axis=1)
df1['passing']=df1[['ShortPassing', 'LongPassing', 'Vision', 'Curve', 'FKAccuracy']].mean(axis=1)
df1['dribbling']=df1[['Dribbling', 'BallControl', 'Agility']].mean(axis=1)
df1['defending']=df1[['Marking', 'StandingTackle', 'SlidingTackle', 'Interceptions']].mean(axis=1)
df1['physic']=df1[['Strength', 'Stamina', 'Jumping', 'Balance', 'Aggression']].mean(axis=1)

df['Age']=df['age']
df['Name']=df['short_name']
df['Nationality']=df['nationality_name']
df['Club']=df['club_name']
df['Position']=df['player_positions']
df['Value']=df['value_eur']
df['Wage']=df['wage_eur']
df['Overall']=df['overall']

def convert_value(val):
    if isinstance(val, str):
        val = val.strip()
        match = re.search(r'([\d\.]+)([MK]?)', val)
        if match:
            number = float(match.group(1))
            suffix = match.group(2)
            if suffix == 'M':
                return int(number * 1_000_000)
            elif suffix == 'K':
                return int(number * 1_000)
            else:
                return int(number)
    return val

df['Value'] = df['Value'].apply(convert_value)
df1['Value'] = df1['Value'].apply(convert_value)

print(df1['Value'].head())


#Drop the Missing Values of Name
df.dropna(subset='Name',inplace=True)
df1.dropna(subset='Name',inplace=True)
#Fill the Missing Values of Age with Mean Age
df['Age'].fillna(df['Age'].mean(), inplace=True)
df1['Age'].fillna(df['Age'].mean(), inplace=True)
#Fill the Missing Values of Club with 'Free Agent'
df['Club'] = df['Club'].fillna('Free Agent')
df1['Club'] = df1['Club'].fillna('Free Agent')
#Drop the Missing Values of Position
df.dropna(subset=['Position'],inplace=True)
df1.dropna(subset=['Position'],inplace=True)
#Drop the Missing Values of Value and Wage with Median
for col in['Value','Wage']:
    df.dropna(subset=[col],inplace=True)
    df1.dropna(subset=[col],inplace=True)
#Fill the Missing Values of pace,shooting,passing,dribbling,defending
for col in ['pace','shooting','passing','dribbling','defending','physic']:
    df[col].fillna(df[col].median(), inplace=True)
    df1[col].fillna(df1[col].median(), inplace=True)
#Drop the Missing Values of Overall
df.dropna(subset='Overall',inplace=True)
df1.dropna(subset='Overall',inplace=True)


fig, ax = plt.subplots(2, 2, figsize=(14, 8))
# Age Distribution Comparison
bins = np.linspace(df['Age'].min(), df['Age'].max(),10)  
ax[0,0].hist(df['Age'], bins=bins, color='blue', alpha=0.5, edgecolor='black', label='FIFA 2022')
ax[0,0].hist(df1['Age'], bins=bins, color='red', alpha=0.5, edgecolor='black', label='FIFA 2019')
ax[0,0].set_title("Age Distribution of Players (2022 vs 2019)")
ax[0,0].set_xlabel("Player Age")
ax[0,0].set_ylabel("Number of Players")
ax[0,0].legend()
ax[0,0].set_xticks(bins.round(1))
#Nationality Distribution Comparison and which nationality not played in which year in top 10
player_per_nationality_22=(df.groupby(['Nationality']).size()).sort_values(ascending=False).head(10)
player_per_nationality_19=(df1.groupby(['Nationality']).size()).sort_values(ascending=False).head(10)
all_nationalities = player_per_nationality_22.index.union(player_per_nationality_19.index)
player_per_nationality_22 = player_per_nationality_22.reindex(all_nationalities, fill_value=0)
player_per_nationality_19 = player_per_nationality_19.reindex(all_nationalities, fill_value=0)
x = np.arange(len(all_nationalities)) 
width = 0.35 
ax[0,1].bar(x - width/2, player_per_nationality_22.values, width, color='orange', alpha=0.7, label='FIFA 2022')
ax[0,1].bar(x + width/2, player_per_nationality_19.values, width, color='blue', alpha=0.4, label='FIFA 2019')
ax[0,1].xaxis.set_major_locator(FixedLocator(x))
ax[0,1].set_xticklabels(all_nationalities, rotation=45, ha='right')
ax[0,1].set_title("Nationality Distribution of Players (2022 vs 2019)")
ax[0,1].set_xlabel("Nationality")
ax[0,1].set_ylabel("Number of Players")
ax[0,1].legend()
#Overall Rating vs Market Value Comparison
ax[1,0].scatter(df['Overall'], df['Value'], color='green', alpha=0.5,marker='^',s=5, label='FIFA 2022')
ax[1,0].scatter(df1['Overall'], df1['Value'], color='purple', alpha=0.5,marker='o',s=5, label='FIFA 2019')
ax[1,0].set_title("Overall Rating vs Market Value (2022 vs 2019)")
ax[1,0].set_xlabel("Overall Rating")
ax[1,0].set_ylabel("Market Value (EUR)")
ax[1,0].legend()

# Data for box plot
data_to_plot = [df['Overall'], df1['Overall']]  # comparing Overall ratings
labels = ['FIFA 2020', 'FIFA 2023']

# Create box plot in subplot ax[1,1]
ax[1,1].boxplot(data_to_plot, labels=labels, patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='red'),
                whiskerprops=dict(color='blue'),
                capprops=dict(color='blue'))

# Set title and labels
ax[1,1].set_title("Comparison of Overall Ratings (2020 vs 2023)")
ax[1,1].set_ylabel("Overall Rating")


plt.tight_layout()
plt.show()



#df.to_csv(r'E:\Asir\Project2_FIFA-EDA-analysis\players_22.csv', index=False)
#df1.to_csv(r'E:\Asir\Project2_FIFA-EDA-analysis\players_19.csv', index=False)

#print(df1[['Name','Age','Nationality','Club','Position','Value','Wage', 'pace','shooting','passing','dribbling','defending','physic','Overall']].isnull().sum())
#print(df[['Name','Age','Nationality','Club','Position','Value','Wage', 'pace','shooting','passing','dribbling','defending','physic','Overall']].isnull().sum())

#Check Missing Columns
#to_check=['Finishing','Age','Nationality','Club','Position','Value','Wage', 'pace','shooting','passing','dribbling','defending','physic']
#missing=[col for col in to_check if col not in df.columns]
#print(missing)

#print(df.info())
