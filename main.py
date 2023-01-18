from typing import Union
from fastapi import FastAPI, Form
from CController import CController

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/order/")
async def order(phrase: str = Form(), seuil: str = Form()):
    '''
    traitement IA
    '''
    result = CController(seuil)

    return result.traitementIA(phrase)

def addInfo():
    '''
    Ajout d'info dans les csv, par ex un nouveau fruit etc...
    '''
    return 0.0