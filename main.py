
import pandas as pd
from tqdm import tqdm
import os

BOLD = '\033[1m' # ACTIONS
BLUE = '\033[94m' # ACTIONS
RESET = '\033[0m'
RED = '\033[91m' # ERRORS
GREEN = '\033[92m' # SUCCESS
YELLOW = '\033[93m' # INFORMATIONS

# print(BOLD+BLUE+"\n\nChargement des données...\n\n*")
df = pd.concat([chunk for chunk in tqdm(pd.read_json('./data/Video_Games.json', lines=True, chunksize=1000), desc=BLUE+'Chargement des données')])
df = df.drop(['style', 'image'], axis=1)


df['vote'] = df['vote'].fillna(0.0)

# Adapting to 'reviewTime' column with the format 'mm d, yyyy'
df['reviewTime'] = pd.to_datetime(df['reviewTime'], format='%m %d, %Y')

# Extract year from 'reviewTime'
df['year'] = df['reviewTime'].dt.year

# Creating a directory to store the split DataFrames
os.makedirs('./split_data', exist_ok=True)

# Splitting the DataFrame by year and saving each as a separate file
for year, group in df.groupby('year'):
    if not os.path.exists(f'./split_data/reviews_{year}.json'):
        group.to_json(f'./split_data/reviews_{year}.json', orient='records', lines=True)
        print(GREEN + f'Fichier JSON créé pour l\'année {year}' + RESET)
    else:
        print(GREEN + f'Fichier JSON pour l\'année {year} existe déjà !' + RESET)
    
    group=group.drop_duplicates(subset=["asin","reviewerID","vote"], keep='last', inplace=True)
    if group!=None:
        print(group)
print("PAS DE DOUBLONS")




###############################################################################
###############################################################################
######################### A   O P T I M I S E R ###############################
###############################################################################
###############################################################################


# for reviewerID, group in df.groupby('asin'):
#     group=group.drop_duplicates(subset=["asin","reviewerID","vote"], keep='last', inplace=True)
#     if group!=None:
#         print(group)
# print("PAS DE DOUBLONS")
        # if group.duplicated(subset=["asin","reviewerID","vote"], keep='last').any():
        #     print(RED + f'Problème de doublons pour l\'ID {reviewerID}' + RESET)
    # for bool in group.duplicated(subset=["asin"], keep='last').any():
    #     if bool:
    #         group.drop_duplicates(subset=["asin","reviewerID","vote"], keep='last', inplace=True)


print(BLUE+'*\n\n'+RESET+BOLD+"Dimensions du DataFrame => "+YELLOW+f"{df.shape}" + RESET)
print(BOLD+"\nColonnes => "+YELLOW+f"{df.columns.to_list()}"+RESET)
print(BOLD+"\nNombre de textes d'avis null => "+YELLOW+f"{df['reviewText'].isnull().sum()}"+RESET)
print(BOLD+"\nNombre de titres d'avis null => "+YELLOW+f"{df['summary'].isnull().sum()}"+RESET)
print(BOLD+"\nNombre de notes null => "+YELLOW+f"{df['overall'].isnull().sum()}"+RESET)
print(BOLD+"\nNombre de votes null => "+YELLOW+f"{df['vote'].isnull().sum()}"+RESET)