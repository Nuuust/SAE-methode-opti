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

print(BLUE+'*\n\n'+RESET+BOLD+"Dimensions du DataFrame => "+YELLOW+f"{df.shape}" + RESET)
print(BOLD+"\nNombre de textes d'avis null => "+YELLOW+f"{df['reviewText'].isnull().sum()}"+RESET)