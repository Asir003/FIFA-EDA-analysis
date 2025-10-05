import pandas as pd
import matplotlib.pyplot as plt
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

df.to_csv(r'E:\Asir\Project2_FIFA-EDA-analysis\players_22.csv', index=False)
df1.to_csv(r'E:\Asir\Project2_FIFA-EDA-analysis\players_19.csv', index=False)

print(df1[['Name','Age','Nationality','Club','Position','Value','Wage', 'pace','shooting','passing','dribbling','defending','physic']].isnull().sum())
print(df[['Name','Age','Nationality','Club','Position','Value','Wage', 'pace','shooting','passing','dribbling','defending','physic']].isnull().sum())

#Check Missing Columns
#to_check=['Finishing','Age','Nationality','Club','Position','Value','Wage', 'pace','shooting','passing','dribbling','defending','physic']
#missing=[col for col in to_check if col not in df.columns]
#print(missing)

#print(df.info())
