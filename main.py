from typing import Union
from fastapi import FastAPI, Form
import re

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/order/")
async def order(phrase: str = Form()):
    '''
    
    traitement IA
    
    '''
    
    result = {}

    # get EAN
    m = re.search('(\d){13}', phrase)
    if m:
        result["ean"] = {
            "value": m.group(0),
            "condifdence": 100
        }

    # get price
    n = 0
    while True and n < 3:
        m = re.search('((\d+|\d+,\d+|\d+\.\d+|[0-9 ]+))(?:euro| euro|e| e|€| €)', phrase)
        if m:
            # ex xxx€
            if m.group(2).isnumeric() == True:
                result["price"] = {
                    "value": float(m.group(2).replace(',', '.')),
                    "confidence": 100
                }
                break
            else:
                # ex €xxx
                m = re.search('(?:€| €)((\d+|\d+,\d+|\d+\.\d+|[0-9 ]+))', phrase)
                if m:
                    if m.group(2).isnumeric() == True:
                        result["price"] = {
                            "value": float(m.group(2).replace(',', '.')),
                            "confidence": 100
                        }
                        break
                else:
                    # faute d'orthographe
                    # trouver le mot "euro" mal écrit en faisant des similaritudes et le remplacer
                    for word in phrase.split(' '):
                        if similaritude("euro", word) >= (0.8-(n*0.1)) or similaritude("euro", word) >= (0.8-(n*0.1)):
                            phrase.replace(word, "euro")
                            break

            n += 1
            
    return result

def similaritude(a, b):
    return 0.0