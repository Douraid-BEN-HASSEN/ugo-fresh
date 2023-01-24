from typing import Union
from fastapi import FastAPI, Form
from CController import CController

app = FastAPI()
controller = CController()

import time

phrases = [
    "J'ai 300kg d'aubergines type grafiti variété angela, en cagette qui viennent de France.",
    "J'ai 300kilg d'aubergines type grafiti variété angela, en cagette qui viennent de France. à €80",
    "J'ai 300kg d'aubergines type grafiti variété angela, en cagette qui viennent de France. de taille sup à 50mm",
    "Ajoute une offre de 40 colis de 12 Batavia voltron d'Espagne calibre 300g à 7 euros 50",
    "Ajoute une offre de 40 colis de 12 Batavia voltron d'Espagne calibre 300g à 7 euros 50",
    "Des abricots rouge du roussillon AOC bio en cagette de 20kg, j'en ai 50, je les vends à 60euros",
    "Je cherche 300 kilos de tomate française coeur de boeuf d'un gros calibre",
    "Je vends 540 petits ananas victoria de la réunion, à 80 euros le carton de 20 ananas"
]

for p in phrases:
    print(controller.traitementIA(p, 0.8, time.time())["benchmark"])


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/order/")
async def order(phrase: str = Form(), seuil: str = Form()):
    '''
    traitement IA
    '''
    return controller.traitementIA(phrase, seuil, time.time())

@app.post("/addInfo/")
async def addInfo(file: str = Form(), info: str = Form()):
    '''
    Ajout d'info dans les csv, par ex un nouveau fruit etc...
    '''
    return { "response": "OK" }

@app.post("/correct/")
async def addInfo(file: str = Form(), info: str = Form()):
    '''
    Fonction de correction
    '''
    return { "response": "OK" }
