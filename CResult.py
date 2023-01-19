import re
from jarowinkler import jarowinkler_similarity

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
        self._prix = None # reset prix self._prix
        n = 0
        while True and n < 3:
            m = re.search('((\d+|\d+,\d+|\d+\.\d+|[0-9 ]+))(?:euro| euro|e| e|€| €)', pPhrase)
            if m:
                # ex xxx€
                try:
                    self._prix = {
                        "value": float(m.group(2).replace(',', '.')),
                        "confidence": 100
                    }
                    return True
                except ValueError:
                    print('a')
            
            # ex €xxx
            m = re.search('(?:€| €)(\d+(?:[.,\s]\d{3})*(?:[.,]\d+)?)', pPhrase)
            if m:
                print(m)
                try:
                    self._prix = {
                        "value": float(m.group(1).replace(',', '.')),
                        "confidence": 100
                    }
                    return True
                except ValueError:
                    print('b')

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

    # méthode qui trouve le calibre
    def parseCalibre(self, pPhrase) -> bool:
        '''
        # to lower
        # remplacer les accents (é -> e, à -> a)

        rechercher les unités :
        unité =
        - x unite
        - x unites
        - x element
        - x elements
        - douzaine
        - demi douzaine
        - x piece
        - x pieces
        - un demi
        - x demi
        - x fruit
        - x fruits
        - x pot
        - x pots
        - x botte
        - x bottes

        // check l'unité si mm ou cm
        millimiter =
        - x millimietre
        - x millimietres
        - x mm
        centimeter =
        - x centimetre
        - x centimetres
        - x cm
        // ensuite voir si inf ou sup
        inf_millimiter/inf_centimeter =
        - inferieur a x
        - inf a x
        sup_millimiter/sup_centimeter =
        - superieur a x
        - sup a x
        
        gram =
        - x gramme
        - x grammes
        - x grame
        - x grames
        - x g

        very_small =
        - xs
        - tres fin
        - trs fin
        - tres petit
        - trs petit
        small =
        - s
        - fin
        - petit
        medium =
        - m
        - moyen
        - moy
        - medium
        - med
        large =
        - l
        - grand
        - grands
        - large
        - lg
        very_large =
        - xl
        - tres grand
        - trs grand
        - tres grands
        - trs grands
        - tres large
        - trs large
        - tres larges
        - trs larges
        very_very_large =
        - xxl
        - tres tres grand
        - trs tres grand
        - tres trs grand
        - trs trs grand
        - tres tres grands
        - trs tres grands
        - tres trs grands
        - trs trs grands
        - tres tres large
        - trs tres large
        - tres trs large
        - trs trs large
        - tres tres larges
        - trs tres larges
        - tres trs larges
        - trs trs larges
        '''
        return False

    # méthode qui trouve la quantite
    def parseQuantite(self, pPhrase) -> bool:
        '''
        trouver le calibre en 1er
        '''
        return False

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
        return jarowinkler_similarity(a,b)