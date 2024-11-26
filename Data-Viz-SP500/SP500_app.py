import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import pdfplumber
import nltk
import re
from nltk.corpus import stopwords
from wordcloud import WordCloud
from collections import Counter


# Chargement des données
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data["Date"] = pd.to_datetime(data["Date"])
    data["Daily Change (%)"] = ((data["Close"] - data["Open"]) / data["Open"]) * 100
    data["Daily Range"] = data["High"] - data["Low"]
    return data

file_path = "FS_sp500_Value_cleaned.csv"
data = load_data(file_path)

# Récupérer les limites valides des dates
min_date = data["Date"].min()
max_date = data["Date"].max()

# Configuration de l'interface Streamlit
st.title("Analyse Financière des Actifs du S&P 500")

# Introduction
st.write("""
Cette étude analyse les actifs composant l'indice S&P 500, un des indices les plus suivis des marchés financiers. 
Le S&P 500 comprend les 500 plus grandes entreprises cotées aux États-Unis et reflète la performance générale du marché boursier américain.

L'objectif de cette étude est de décomposer la performance des actifs du S&P 500 à travers plusieurs indicateurs financiers clés, 
tels que l'évolution des prix de clôture, la volatilité des prix, les volumes échangés et la variation quotidienne des actifs. 
Nous allons explorer ces données et offrir une analyse visuelle des tendances du marché pour aider à mieux comprendre les comportements des actifs.

Ce travail a été réalisé par :
- **Salma Lahbati**
- **Cyrena Ramdani**
- **Yoav Cohen**
""")

# Description du jeu de données
st.header("Description du jeu de données")

st.write("""
Les données utilisées dans cette étude proviennent d'une base de données historique des actifs du S&P 500. 
Lien: https://www.kaggle.com/datasets/hanseopark/sp-500-stocks-value-with-financial-statement
Elles contiennent des informations financières quotidiennes pour chaque actif de l'indice. 
Le jeu de données comprend plusieurs variables financières et a été nettoyé pour supprimer les anomalies et les valeurs manquantes.
Nous avons sélectionné par défaut 10 actifs composants le S&P 500 mais un filtre situé en haut à gauche permet d'ajouter ou retirer des actifs afin de comparer leurs différentes caractéristiques. 

### Détails du jeu de données :
- **Nombre d'observations** : {} lignes
- **Nombre de variables** : {} colonnes
- **Types de variables** :
  - `Date` : Date (datetime64)
  - `Ticker` : Identifiant de l'actif (String)
  - `Open` : Prix d'ouverture (float)
  - `High` : Prix le plus élevé (float)
  - `Low` : Prix le plus bas (float)
  - `Close` : Prix de clôture (float)
  - `Volume` : Volume échangé (int)
  - `Daily Change (%)` : Variation quotidienne en pourcentage (float)
  - `Daily Range` : Amplitude journalière des prix (float)

### Statistiques descriptives :
""")

# Afficher les statistiques descriptives du jeu de données
st.write(data.describe())

# Nombre de valeurs manquantes par variable
missing_values = data.isnull().sum()
st.write("Nombre de valeurs manquantes par variable :")
st.write(missing_values)

# Filtrage initial
tickers = data["Ticker"].unique()[:10]  # Sélectionner uniquement 10 tickers par défaut

# Mise à jour des dates par défaut pour s'aligner sur les données
start_date = min_date
end_date = max_date

st.sidebar.header("Filtres")
selected_tickers = st.sidebar.multiselect("Sélectionnez les tickers", options=data["Ticker"].unique(), default=tickers)
start_date = st.sidebar.date_input("Date de début", value=start_date.date(), min_value=min_date.date(), max_value=max_date.date())
end_date = st.sidebar.date_input("Date de fin", value=end_date.date(), min_value=min_date.date(), max_value=max_date.date())

# Convertir les dates de l'utilisateur en datetime pour comparaison avec la colonne 'Date'
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filtrage des données
filtered_data = data[
    (data["Ticker"].isin(selected_tickers)) &
    (data["Date"] >= start_date) &
    (data["Date"] <= end_date)
]

# Section des graphiques
st.header("Visualisations des données financières")

# 1. Évolution des prix de clôture dans le temps
st.subheader("Évolution des prix de clôture dans le temps")
st.write("""
Ce graphique montre la variation des prix de clôture sur la période choisie. Il est important de suivre l'évolution des prix de clôture pour identifier les tendances à long terme 
et évaluer la performance des actifs sélectionnés. 
""")

fig, ax = plt.subplots(figsize=(10, 5))
for ticker in selected_tickers:
    subset = filtered_data[filtered_data["Ticker"] == ticker]
    ax.plot(subset["Date"], subset["Close"], label=ticker)
ax.set_title("Évolution des prix de clôture")
ax.set_xlabel("Date")
ax.set_ylabel("Prix de clôture")
ax.legend(loc="best")
st.pyplot(fig)

# explication sous le graphique des prix de clôture
st.write(f"Sur la période choisie, on observe une tendance à la hausse pour certains actifs, notamment ceux qui sont liés à des secteurs comme la technologie. "
         f"Les prix de clôture montrent des fluctuations significatives autour de 2020, probablement en raison de l'impact du COVID-19 sur les marchés financiers.")

# 2. Graphique des volumes échangés
st.subheader("Volume échangé au fil du temps")
st.write("""
Le volume d'échange est une mesure clé de l'intérêt du marché pour un actif. Ce graphique montre l'évolution du volume échangé pour les actifs sélectionnés.
""")

fig, ax = plt.subplots(figsize=(10, 5))
for ticker in selected_tickers:
    subset = filtered_data[filtered_data["Ticker"] == ticker]
    ax.bar(subset["Date"], subset["Volume"], label=ticker, alpha=0.6)
ax.set_title("Volume échangé au fil du temps")
ax.set_xlabel("Date")
ax.set_ylabel("Volume")
ax.legend(loc="best")
st.pyplot(fig)

# Explication sous le graphique des volumes échangés
st.write(f"On observe une augmentation du volume d'échange pendant certaines périodes, en particulier pendant les périodes de forte volatilité, "
         f"comme lors des baisses importantes de 2020 liées à la pandémie de COVID-19.")

# 3. Relation entre les prix élevés et les prix bas
st.subheader("Corrélation entre les prix hauts et bas")
st.write("""
Analyser la relation entre les prix les plus hauts et les plus bas peut fournir une idée de la volatilité journalière des actifs. 
Une forte corrélation indique des fluctuations limitées, tandis qu'une corrélation plus faible peut signaler une volatilité accrue.
""")

fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=filtered_data, x="High", y="Low", hue="Ticker", ax=ax)
ax.set_title("Corrélation entre les prix hauts et bas")
ax.set_xlabel("Prix élevé")
ax.set_ylabel("Prix bas")
st.pyplot(fig)

# Explication sous le graphique de la corrélation entre prix haut et bas
st.write(f"Les actifs présentant une large différence entre les prix hauts et bas (plus de 10%) sont souvent plus volatils. "
         f"Ces variations sont typiques lors de périodes d'incertitude économique, comme celles observées durant les chocs économiques mondiaux.")

# 4. Performance quotidienne (Daily Change %)
st.subheader("Performance quotidienne des actifs")
st.write("""
La performance quotidienne est un indicateur de la rentabilité des actifs sur une base journalière. 
Ce graphique permet d'identifier les actifs les plus volatils et les plus stables en fonction de leurs variations quotidiennes.
Nous observons ici que l'actif ABMD est plus volatil que l'actif A. En effet, ses variations quotidiennes vont de -20 à 20% tandis que ca va seulement de -10 à 10% pour l'actif A. 
""")

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=filtered_data, x="Ticker", y="Daily Change (%)", ax=ax)
ax.set_title("Performance quotidienne (en %)")
ax.set_xlabel("Ticker")
ax.set_ylabel("Variation quotidienne (%)")
st.pyplot(fig)

# Explication sous le graphique de la performance quotidienne
st.write(f"En analysant la performance quotidienne, on peut voir que certains actifs, comme ABMD, montrent une plus grande volatilité "
         f"en raison de leur forte exposition aux facteurs de marché externes. Les actions moins volatiles peuvent refléter des secteurs plus stables.")

# 5. Variation des prix dans une journée (Daily Range)
st.subheader("Amplitudes journalières des prix")
st.write("""
L'amplitude journalière des prix (Daily Range) mesure la différence entre les prix hauts et bas d'une journée. 
Un large éventail peut indiquer une forte volatilité, utile pour déterminer les opportunités de trading à court terme.
""")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_data, x="Date", y="Daily Range", hue="Ticker", ax=ax)
ax.set_title("Amplitude journalière des prix")
ax.set_xlabel("Date")
ax.set_ylabel("Amplitude journalière")
st.pyplot(fig)

# Explication sous le graphique des amplitudes journalières
st.write(f"Les amplitudes journalières ont augmenté depuis 2020, particulièrement après le début de la pandémie de COVID-19, signalant une volatilité accrue. "
         f"Ces variations peuvent être interprétées comme des opportunités pour les traders à court terme, mais aussi comme des signaux de risque pour les investisseurs à long terme.")


# Télécharger les stopwords de NLTK
nltk.download('stopwords')
nltk.download('punkt')

# Liste des mots à exclure, en plus de ceux dans NLTK stopwords
extra_stopwords = {'of', 'and', 'the', 'a', 'to', 'in', 'for', 'on', 'with', 'as', 'at', 'by', 'an', 'is', 'that', 'are', 'epu'}

# Fonction pour extraire le texte du PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Fonction de prétraitement du texte
def preprocess_text(text):
    text = text.lower()  # Convertir en minuscules
    text = re.sub(r'[^a-z\s]', '', text)  # Supprimer les caractères non alphabétiques
    stop_words = set(stopwords.words('french'))  # Liste des mots fréquents
    stop_words.update(extra_stopwords)  # Ajouter les mots supplémentaires à exclure
    words = text.split()
    words = [word for word in words if word not in stop_words]  # Supprimer les stopwords
    return ' '.join(words), words

# Fonction pour générer un WordCloud
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

# Interface Streamlit
st.title("Générer un WordCloud à partir d'un PDF")

st.write("""
### Résumé de l'article
Cet article explore la relation entre la volatilité dépendante des régimes dans le S&P 500 et plusieurs indicateurs clés : l'incertitude économique, l'écart de sentiment entre les marchés haussiers et baissiers du S&P 500 (bb_sp), ainsi que l'indice VIX, mesurant la volatilité implicite. 
L'étude, menée sur la période 2000-2018, s'appuie sur des méthodologies avancées telles que GARCH-MIDAS, les chaînes de Markov à commutation de régimes et les régressions quantiles. 
Les résultats montrent que la manière dont la volatilité réalisée interagit avec ces indicateurs dépend fortement du régime de volatilité (élevée ou faible) et de la sensibilité des investisseurs face aux incertitudes économiques. 
Une conclusion notable est que ces indicateurs, bien qu'intéressants pour comprendre le marché, ont une utilité limitée dans la prévision de la volatilité, particulièrement dans les régimes de haute volatilité.
""")

# Demander à l'utilisateur de télécharger un fichier PDF
uploaded_file = st.file_uploader("Choisissez un fichier PDF", type="pdf")

if uploaded_file is not None:
    # Extraire le texte du PDF
    text = extract_text_from_pdf(uploaded_file)

    # Si du texte a été extrait
    if text:
        st.write("Le texte a été extrait avec succès. Prétraitement en cours...")
        
        # Prétraiter le texte et obtenir les mots pour la fréquence
        processed_text, words = preprocess_text(text)
        
        if words:
            # Générer le WordCloud
            wordcloud = generate_wordcloud(processed_text)
            
            # Afficher le WordCloud
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot(plt)  # Utilisation de Streamlit pour afficher la figure

            # Analyser les mots les plus fréquents
            word_counts = Counter(words)  # Utilisation de Counter pour compter la fréquence des mots
            most_common_words = word_counts.most_common(1)

            # Afficher les 3 mots les plus fréquents
            st.write("### Le mot le plus fréquent :")
            for i, (word, count) in enumerate(most_common_words):
                st.write(f"{i+1}. **{word}** : apparaissant {count} fois")

            # Fournir une explication des mots clés
            st.write("""
            Ce mot est pertinent car ils reflètent le thème principal de l'article. 
           En effet, le mot volatilité est bien représenté, surtout durant la periode 2018-2020, soit pendant le covid. 
            """)
        else:
            st.error("Aucun mot pertinent n'a été trouvé après le prétraitement du texte.")
    else:
        st.error("Aucun texte n'a pu être extrait du PDF.")