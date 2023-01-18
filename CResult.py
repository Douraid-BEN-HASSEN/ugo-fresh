import re

class CResult:
    _seuil = None
    _caliber = None
    _conditionnement = None
    _famille = None
    _labels = None
    _pays = None
    _quantite = None
    _sous_variete = None
    _variete = None
    _prix = None
    _ean = None

    # constructor
    def __init__(self, pSeuil = 0.8) -> None:
        self._seuil = pSeuil

    def setSeuil(self, pSeuil) -> None:
        self._seuil = pSeuil
        
    # méthode qui trouve le prix dans une phrase
    def parsePrix(self, pPhrase) -> bool:
        n = 0
        while True and n < 3:
            m = re.search('((\d+|\d+,\d+|\d+\.\d+|[0-9 ]+))(?:euro| euro|e| e|€| €)', pPhrase)
            if m:
                # ex xxx€
                if m.group(2).isnumeric() == True:
                    self._prix = {
                        "value": float(m.group(2).replace(',', '.')),
                        "confidence": 100
                    }
                    return True
                else:
                    # ex €xxx
                    m = re.search('(?:€| €)((\d+|\d+,\d+|\d+\.\d+|[0-9 ]+))', pPhrase)
                    if m:
                        if m.group(2).isnumeric() == True:
                            self._prix = {
                                "value": float(m.group(2).replace(',', '.')),
                                "confidence": 100
                            }
                            return True
                    else:
                        # faute d'orthographe
                        # trouver le mot "euro" mal écrit en faisant des similaritudes et le remplacer
                        for word in pPhrase.split(' '):
                            if self.similaritude("euro", word) >= (self._seuil-(n*0.1)) or self.similaritude("euro", word) >= (self._seuil-(n*0.1)):
                                pPhrase.replace(word, "euro")
                                return True
                n += 1
        
        return False
    
    # méthode qui trouve le numero EAN dans une phrase
    def parseEan(self, pPhrase) -> bool:
        # get EAN
        m = re.search('(\d){13}', pPhrase)
        if m:
            self._ean = {
                "value": m.group(0),
                "condifdence": 100
            }
            return True

    # méthode qui retourne les données sous forme d'un objet
    def toObject(self) -> object:
        result = {}
        if self._caliber is not None:
            result["caliber"] = self._caliber

        if self._conditionnement is not None:
            result["conditionnement"] = self._conditionnement
        
        if self._famille is not None:
            result["famille"] = self._famille
        
        if self._labels is not None:
            result["labels"] = self._labels
        
        if self._pays is not None:
            result["pays"] = self._pays
        
        if self._quantite is not None:
            result["quantite"] = self._quantite
        
        if self._sous_variete is not None:
            result["sous_variete"] = self._sous_variete
        
        if self._variete is not None:
            result["variete"] = self._variete
        
        if self._prix is not None:
            result["prix"] = self._prix        
        
        if self._ean is not None:
            result["ean"] = self._ean

        return result

    #TODO: méthode à faire
    # méthode qui retourne la similaritude entre 2 mot
    def similaritude(self, a, b) -> float:
        return 0.0