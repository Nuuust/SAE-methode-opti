import pandas as pd
from tqdm import tqdm

BOLD = '\033[1m' # ACTIONS
BLUE = '\033[94m' # ACTIONS
RESET = '\033[0m'
RED = '\033[91m' # ERRORS
GREEN = '\033[92m' # SUCCESS
YELLOW = '\033[93m' # INFORMATIONS


print(BOLD+BLUE+"\n\nChargement des données...\n\n*")
df = pd.concat([chunk for chunk in tqdm(pd.read_json('./data/Video_Games.json', lines=True, chunksize=1000), desc='Loading data')])
df = df.drop(['style', 'image'], axis=1)

print(BLUE+'*\n\n'+RESET+BOLD+"Dimensions du DataFrame => "+YELLOW+f"{df.shape}" + RESET)
print(BOLD+"\nColonnes => "+YELLOW+f"{df.columns.to_list()}"+RESET)
print(BOLD+"\nNombre de textes d'avis null => "+YELLOW+f"{df['reviewText'].isnull().sum()}"+RESET)
print(BOLD+"\nNombre de titres d'avis null => "+YELLOW+f"{df['summary'].isnull().sum()}"+RESET)
#print(BOLD+"\nNombre de notes null => "+YELLOW+f"{df['overall'].isnull().sum()}"+RESET)
print(BOLD+"\nNombre de votes null => "+YELLOW+f"{df['vote'].isnull().sum()}"+RESET)
print(df.head()['vote'])

# TRI PAR ANNÉES

dfs_by_year = {}

# Iterate through the rows of the original DataFrame
for index, row in df.iterrows():
    year = row['reviewTime'].split(" ")[2]
    
    # Check if a DataFrame for the year exists, create one if not
    if year not in dfs_by_year:
        print(f'Creating DataFrame for year {year}...')
        dfs_by_year[year] = pd.DataFrame(columns=df.columns)
        df_y=pd.DataFrame(row)
        pd.concat([df_y, dfs_by_year[year]], ignore_index=True)
    
    # Check if vote exists
    if pd.isnull(row["vote"]):
        df.iloc[index, df.columns.get_loc("vote")] = 0.0
    
    

    #dfs_by_year[year].append(row, ignore_index=True)
    #dfs_by_year[year].insert(len(dfs_by_year[year].columns), index, row) ------->  NOT WORKING ON LARGE DATAFRAME



pd.concat(dfs_by_year[year], ignore_index=True)
print(dfs_by_year)
    # print(dfs_by_year[year].head())    
    #dfs_by_year[year] = pd.concat([dfs_by_year[year], pd.DataFrame([row])], ignore_index=True)
    #dfs_by_year[year].loc[len(dfs_by_year[year])] = row
print(BOLD+"\nNombre de votes null => "+YELLOW+f"{df['vote'].isnull().sum()}"+RESET)

# for year, df_year in dfs_by_year.items():
#     print(f'DataFrame for year {year}:')
#     print(df_year)