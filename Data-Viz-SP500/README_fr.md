# Analyse Financière des Actifs du S&P 500

Ce projet analyse la performance des actifs composant l'indice S&P 500, un indicateur majeur du marché boursier américain. L'application utilise Streamlit pour fournir un tableau de bord interactif visualisant les principaux indicateurs financiers et permettant aux utilisateurs de filtrer les données par date et par actif. Un nuage de mots est également généré à partir d'un article académique connexe pour visualiser les termes clés.

## Présentation du Projet

L'objectif est de fournir une analyse complète des actifs du S&P 500, englobant l'exploration des données, la visualisation et l'exploration de texte. L'analyse se concentre sur les mouvements de prix quotidiens, le volume des transactions et la volatilité, et explore la relation entre ces indicateurs.

Le projet utilise des données provenant de Kaggle ([https://www.kaggle.com/datasets/hanseopark/sp-500-stocks-value-with-financial-statement](https://www.kaggle.com/datasets/hanseopark/sp-500-stocks-value-with-financial-statement)) et intègre un PDF pour l'analyse de texte utilisant des techniques de PNL (Traitement du Langage Naturel).

## Fonctionnalités

* **Exploration interactive des données :** Les utilisateurs peuvent sélectionner des actifs spécifiques et des plages de dates pour filtrer les données.
* **Visualisations :** L'application fournit plusieurs graphiques :
  * Graphiques linéaires montrant l'évolution des cours de clôture au fil du temps.
  * Graphiques à barres illustrant le volume des transactions quotidiennes.
  * Nuages de points représentant la relation entre les cours hauts et bas quotidiens.
  * Boîtes à moustaches comparant la performance quotidienne (variation en pourcentage) des actifs sélectionnés.
  * Graphiques linéaires illustrant l'amplitude des cours quotidiens.
* **Statistiques descriptives :** Fournit des statistiques sommaires (moyenne, écart type, etc.) de l'ensemble de données.
* **Nuage de mots :** Génère un nuage de mots à partir d'un document PDF fourni, mettant en évidence les termes clés liés au sujet.
* **Nettoyage et prétraitement des données :** Gère les valeurs manquantes et prétraite les données textuelles pour l'analyse.

## Données

Les données utilisées sont une version nettoyée de l'ensemble de données original trouvé sur Kaggle. Cela inclut la création de nouvelles variables. Le fichier CSV nettoyé est fourni dans le dossier `clean-data`. Les données originales (différents formats) se trouvent également dans le dossier `Data`.

## Installation

1. **Installer les dépendances :** Installez les bibliothèques Python nécessaires à l'aide de `pip install -r requirements.txt`.
2. **Exécuter l'application :** Exécutez le fichier `SP500_app.py` à l'aide de `streamlit run SP500_app.py`.

## Structure des Fichiers

```
├── Data/                 # Fichiers de données originaux (JSON, numbers, etc.)
│  ├── FS_sp500_Value.json
│  └── FS_sp500_Value.numbers
├── data_process.ipynb    # Notebook Jupyter pour l'exploration et le nettoyage initiaux des données
├── README.md             # Ce fichier en anglais
├── README_fr.md          # Ce fichier
├── SP500_app.py          # Script principal de l'application Streamlit
├── articles/             # Dossier contenant des articles sur ce sujet
│  └── S&P 500 volatility, volatility regimes, and ECONOMIC UNCERTAINTY.pdf
├── clean-data/           # Fichiers de données nettoyées
│  ├── FS_sp500_Value_cleaned.csv
│  └── FS_sp500_Value_cleaned.json
└── requirements.txt      # Liste des paquets Python requis
```

## Contributeurs

- Salma Lahbati
- Cyrena Ramdani
- Yoav Cohen


Ce projet est un projet étudiant répondant aux exigences d'un cours de Gestion des Données, Visualisation des Données et Exploration de Texte. Il vise à démontrer des compétences en manipulation de données, visualisation et traitement du langage naturel.