
import pandas as pd
from tqdm import tqdm
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import spacy

BOLD = '\033[1m' # ACTIONS
BLUE = '\033[94m' # ACTIONSv
RESET = '\033[0m'
RED = '\033[91m' # ERRORS
GREEN = '\033[92m' # SUCCESS
YELLOW = '\033[93m' # INFORMATIONS

# print(BOLD+BLUE+"\n\nChargement des données...\n\n*")
df = pd.concat([chunk for chunk in tqdm(pd.read_json('./data/Video_Games.json', lines=True, chunksize=1000), desc=BLUE+'Chargement des données')])
df = df.drop(['style', 'image'], axis=1)


df['vote'] = df['vote'].fillna(0.0)

df['reviewTime'] = pd.to_datetime(df['reviewTime'], format='%m %d, %Y')

df['year'] = df['reviewTime'].dt.year

os.makedirs('./split_data', exist_ok=True)

for year, group in df.groupby('year'):
    if not os.path.exists(f'./split_data/reviews_{year}.json'):
        group.to_json(f'./split_data/reviews_{year}.json', orient='records', lines=True)
        print(GREEN + f'Fichier JSON créé pour l\'année {year}' + RESET)
    else:
        print(GREEN + f'Fichier JSON pour l\'année {year} existe déjà !' + RESET)
    
    group=group.drop_duplicates(subset=["asin","reviewerID","vote"], keep='last', inplace=True)
    if group!=None:
        print(f"{RED}Problème de doublons sur : {group}")
    else:
        print(f"{YELLOW}PAS DE DOUBLONS")


print(BLUE+'*\n\n'+RESET+BOLD+"Dimensions du DataFrame => "+YELLOW+f"{df.shape}" + RESET)
print(BOLD+"\nColonnes => "+YELLOW+f"{df.columns.to_list()}"+RESET)
print(BOLD+"\nNombre de textes d'avis null => "+YELLOW+f"{df['reviewText'].isnull().sum()}"+RESET)
print(BOLD+"\nNombre de titres d'avis null => "+YELLOW+f"{df['summary'].isnull().sum()}"+RESET)
print(BOLD+"\nNombre de notes null => "+YELLOW+f"{df['overall'].isnull().sum()}"+RESET)
print(BOLD+"\nNombre de votes null => "+YELLOW+f"{df['vote'].isnull().sum()}"+RESET)


'''
df=pd.read_json('./split_data/reviews_2014.json', lines=True)

df['label'] = df['overall'].apply(lambda x: 1 if x > 3 else 0) 

# Prétraitement avec spaCy
nlp = spacy.load("en_core_web_sm")
def preprocess(text):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

df['processed_text'] = df['reviewText'].apply(preprocess)






# Vectorisation
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['processed_text'])
y = df['label']

# Division des données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# KNN
knn_model = KNeighborsClassifier()
knn_params = {'n_neighbors': [3, 5, 7, 9]}
knn_clf = GridSearchCV(knn_model, knn_params)
knn_clf.fit(X_train, y_train)

# Régression logistique
log_model = LogisticRegression()
log_params = {'C': [0.01, 0.1, 1, 10]}
log_clf = GridSearchCV(log_model, log_params)
log_clf.fit(X_train, y_train)

# Évaluation de KNN
y_pred_knn = knn_clf.predict(X_test)
print("KNN Classification Report")
print(classification_report(y_test, y_pred_knn))

# Évaluation de la Régression logistique
y_pred_log = log_clf.predict(X_test)
print("Logistic Regression Classification Report")
print(classification_report(y_test, y_pred_log))
'''