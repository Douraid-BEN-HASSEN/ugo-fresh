from typing import Union
from fastapi import FastAPI, Form
from CController import CController

app = FastAPI()
controller = CController()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/order/")
async def order(phrase: str = Form(), seuil: str = Form()):
    '''
    traitement IA
    '''
    return controller.traitementIA(phrase, seuil)

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
