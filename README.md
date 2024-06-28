# README

## Introduction

Ce projet vise à répondre aux besoins d'UgoFresh en automatisant l'extraction d'informations à partir de descriptions en langage naturel fournies par les fournisseurs. Le système implémente une API qui permet de traiter des phrases et de retourner les différentes entités nécessaires pour décrire les offres de fruits et légumes<sub>2</sub>.

## Structure du Projet

Le projet contient trois principaux fichiers Python :

- `main.py`
- `controller.py`
- `cresult.py`

## Fichiers et Fonctions

### main.py

`main.py` initialise l'application FastAPI et définit les routes pour l'API.

- `read_root()`: Route GET de base qui retourne un message de bienvenue.
- `order()`: Route POST qui traite une phrase et un seuil pour analyser les informations.
- `addInfo()`: Route POST qui permet d'ajouter des informations dans un fichier CSV.
- `correct()`: Route POST pour corriger les informations déjà présentes.

### CController.py

`controller.py` contient la classe `CController` qui gère le traitement des phrases en utilisant un objet `CResult`.

- `__init__(self)`: Initialise un objet `CResult`.
- `traitementIA(self, pPhrase, pSeuil, pBench)`: Traite une phrase, ajuste le seuil et retourne les résultats avec un benchmark de temps<sub>1</sub>.

### CResult.py

`cresult.py` contient la classe `CResult` qui est utilisée pour extraire et stocker les différentes entités de la phrase.

- `setSeuil(seuil)`: Définit le seuil.
- `parseEan(phrase)`, `parsePrix(phrase)`, `parseCalibre(phrase)`, `parseQuantite(phrase)`: Méthodes pour extraire différentes entités de la phrase.
- `toObject()`: Convertit les résultats en un objet dictionary.

## Installation

1. Clonez le repository:

    ```sh
    git clone https://github.com/Douraid-BEN-HASSEN/ugo-fresh.git
    cd ugo-fresh
    ```

2. Installez les dépendances:

    ```sh
    pip install fastapi uvicorn jarowinkler
    ```

3. Lancez l'application FastAPI:

    ```sh
    uvicorn main:app --reload
    ```

## Utilisation

### Endpoints

- `GET /`: Route de base, retourne `"Hello": "World"`
- `POST /order/`: Prend deux paramètres `phrase` et `seuil` pour effectuer le traitement IA.
    - Exemples de phrases supportées :
        - "J'ai 300kg d'aubergines type grafiti variété angela, en cagette qui viennent de France."<sub>1</sub>
        - "Ajoute une offre de 40 colis de 12 Batavia voltron d'Espagne calibre 300g à 7 euros 50"<sub>1</sub>.
- `POST /addInfo/`: Prend deux paramètres `file` et `info` pour ajouter des informations dans un fichier CSV.
- `POST /correct/`: Prend deux paramètres `file` et `info` pour corriger des informations déjà présentes.

## Exemples d'Utilisation

Pour utiliser l'API, vous pouvez envoyer des requêtes via `curl` ou tout autre outil de requête HTTP :

```sh
curl -X POST "http://127.0.0.1:8000/order/" -F "phrase=J'ai 300kg d'aubergines type grafiti variété angela, en cagette qui viennent de France." -F "
```
```sh
curl -X POST "http://127.0.0.1:8000/addInfo/" -F "file=data.csv" -F "info=nouveau fruit"
```
```sh
curl -X POST "http://127.0.0.1:8000/correct/" -F "file=data.csv" -F "info=correction"
```
