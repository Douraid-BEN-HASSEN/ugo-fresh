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

    _bestConfidenceVal = 0.0

    # constructor
    def __init__(self, pSeuil = 0.8) -> None:
        self._seuil = float(pSeuil)

    def setSeuil(self, pSeuil) -> None:
        self._seuil = float(pSeuil)

    # méthode qui trouve le prix dans une phrase [OK]
    def parsePrix(self, pPhrase) -> bool:
        self._prix = {} # reset prix self._prix
        ''' séparer les mots de nombres '''
        wordTmp = re.split('(\d+(?:[.,\s]\d{3})*(?:[.,]\d+)?)', pPhrase)
        pPhrase = ""
        for w in wordTmp:
            pPhrase = pPhrase + " " + w
        pPhrase = pPhrase.replace("  ", " ")

        n = 0
        while n < 3:
            m = re.search('(\d+(?:[.,\s]\d{3})*(?:[.,]\d+)?)(?:euro| euro|e| e|€| €)', pPhrase)
            if m:
                # ex xxx€
                try:
                    self._prix["value"] = float(m.group(1).replace(',', '.'))

                    if "confidence" not in self._prix:
                        self._prix["confidence"] = 99.9
                    return True
                except ValueError:
                    pass
            
            # ex €xxx
            m = re.search('(?:€|€ )(\d+(?:[.,\s]\d{3})*(?:[.,]\d+)?)', pPhrase)
            if m:
                try:
                    self._prix["value"] = float(m.group(1).replace(',', '.'))
                    
                    if "confidence" not in self._prix:
                        self._prix["confidence"] = 99.9
                    return True
                except ValueError:
                    pass

            # faute d'orthographe
            # trouver le mot "euro" mal écrit en faisant des similaritudes et le remplacer
            self._bestConfidenceVal = 0.0 # reset self._bestConfidenceVal

            for word in pPhrase.split(' '):
                if self.similaritude("euro", word) >= (self._seuil-(n*0.1)) or self.similaritude("euros", word) >= (self._seuil-(n*0.1)) or self.similaritude("eur", word) >= (self._seuil-(n*0.1)):
                    self._prix["confidence"] = self._bestConfidenceVal
                    pPhrase = pPhrase.replace(word, "euro")
                    #return True
            n += 1
        
        self._prix = None
        return False
    
    # méthode qui trouve le numero EAN dans une phrase [OK]
    def parseEan(self, pPhrase) -> bool:
        self._ean = None # reset self._ean
        # get EAN
        m = re.search('(\d){13}', pPhrase)
        if m:
            self._ean = {
                "value": m.group(0),
                "confidence": 99.9
            }
            return True

    # méthode qui trouve le calibre
    def parseCalibre(self, pPhrase) -> bool:
        self._caliber = {} # reset self._caliber
        '''
        to lower
        remplacer les accents (é -> e, à -> a)
        '''
        pPhrase = pPhrase.lower().replace("é", "e").replace("è", "e").replace("à", "a")
       
        ''' séparer les mots de nombres '''
        wordTmp = re.split('(\d+(?:[.,\s]\d{3})*(?:[.,]\d+)?)', pPhrase)
        pPhrase = ""
        for w in wordTmp:
            pPhrase = pPhrase + " " + w
        pPhrase = pPhrase.replace("  ", " ")

        n = 0
        while n < 3:
            # partie 1 full regex
            '''
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
            '''
            m = re.search('(\d+(?:[.,\s]\d{3})*(?:[.,]\d+)?|un|une)(?: |)(?:unite|element|douzaine|demi douzaine|piece|demi|fruit)(?:s|)', pPhrase)
            if m:
                self._caliber["value"] = "unité"
                if "confidence"not in self._caliber:
                        self._caliber["confidence"] = 99.9
                return True

            '''
            // check l'unité si mm ou cm
            millimiter =
            - x millimietre
            - x millimietres
            - x mm
            centimeter =
            - x centimetre
            - x centimetres
            - x cm
            '''
            m = re.search('(inferieur a|inf a|superieur a|sup a|millimietre| mm|centimetre|cm)(?:|s)', pPhrase)
            if m:
                if "inf" not in m.group(1) and "sup" not in m.group(1):
                    if str(m.group(1)) == "millimietre" or str(m.group(1)) == "mm":
                        if self._caliber is not None:
                            if "value" in self._caliber:
                                self._caliber["value"] = self._caliber["value"] + "millimiter"
                            else:
                                self._caliber["value"] = "millimiter"
                        else:
                            self._caliber["value"] = "millimiter"
                    else:
                        if self._caliber is not None:
                            if "value" in self._caliber:
                                self._caliber["value"] = self._caliber["value"] + "centimeter"
                            else:
                                self._caliber["value"] = "centimeter"
                        else:
                            self._caliber["value"] = "centimeter"
                    if "confidence" not in self._caliber:
                        self._caliber["confidence"] = 99.9

                    return True

            m = re.search('(inferieur a|inf a|superieur a|sup a)', pPhrase)
            if m:
                '''
                // ensuite voir si inf ou sup
                inf_millimiter/inf_centimeter =
                - inferieur a x
                - inf a x
                sup_millimiter/sup_centimeter =
                - superieur a x
                - sup a x
                '''
                if "inf" in str(m.group(1)):
                    if self._caliber is not None:
                        if "millimiter" in self._caliber:
                            self._caliber["value"] = "inf_millimiter"
                        else:
                            self._caliber["value"] = "inf_centimeter"
                    else:
                        self._caliber["value"] = "inf_"
                    if "confidence" not in self._caliber:
                        self._caliber["confidence"] = 99.9
                else:
                    if self._caliber is not None:
                        if "millimiter" in self._caliber:
                            self._caliber["value"] = "sup_millimiter"
                        else:
                            self._caliber["value"] = "sup_centimeter"
                    else:
                        self._caliber["value"] = "sup_"
                    if "confidence" not in self._caliber:
                        self._caliber["confidence"] = 99.9

                if self._caliber["value"] == "sup_" or self._caliber["value"] == "inf_":
                    self._caliber["value"] = "inf_millimiter"
                    if "confidence" not in self._caliber:
                        self._caliber["confidence"] = 99.9
                return True

            m = re.search('(\d+(?:[.,\s]\d{3})*(?:[.,]\d+)?|un)(?: |)(gram|gramme|grame|g)(?:s|)', pPhrase)
            if m:
                '''
                gram =
                - x gramme
                - x grammes
                - x grame
                - x grames
                - x g
                '''
                self._caliber["value"] = "gram"
                if "confidence" not in self._caliber:
                    self._caliber["confidence"] = 99.9
                return True

            m = re.search('(xs|tres fin|trs fin|tres petit|trs petit)', pPhrase)
            if m:
                '''
                very_small =
                - xs
                - tres fin
                - trs fin
                - tres petit
                - trs petit
                '''
                self._caliber["value"] = "very_small"
                if "confidence" not in self._caliber:
                    self._caliber["confidence"] = 99.9
                return True
                
            m = re.search('( s,| s\.|fin|petit)', pPhrase)
            if m:
                '''
                small =
                - s
                - fin
                - petit
                '''
                self._caliber["value"] = "small"
                if "confidence" not in self._caliber:
                    self._caliber["confidence"] = 99.9
                return True

            m = re.search('( m,| m\.|moyen|moy|medium|med)', pPhrase)
            if m:
                '''
                medium =
                - m
                - moyen
                - moy
                - medium
                - med
                '''
                self._caliber["value"] = "medium"
                if "confidence" not in self._caliber:
                    self._caliber["confidence"] = 99.9
                return True
            
            m = re.search('(xxl|tres tres grand|trs tres grand|trs trs grand|tres tres large|trs tres large|tres trs large|trs trs large)', pPhrase)
            if m:
                '''
                very_very_large =
                - xxl
                - tres tres grand
                - trs tres grand
                - tres trs grand
                - trs trs grand
                - tres tres large
                - trs tres large
                - tres trs large
                - trs trs large
                '''
                self._caliber["value"] = "very_very_large"
                if "confidence" not in self._caliber:
                    self._caliber["confidence"] = 99.9
                return True

            m = re.search('( xl,| xl\.|tres grand|trs grand|tres large|trs large)', pPhrase)
            if m:
                '''
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
                '''
                self._caliber["value"] = "very_large"
                if "confidence" not in self._caliber:
                    self._caliber["confidence"] = 99.9
                return True

            m = re.search('( l,| l\.|grand|large|lg)', pPhrase)
            if m:
                '''
                large =
                - l
                - grand
                - grands
                - large
                - lg
                '''
                self._caliber["value"] = "large"
                if "confidence" not in self._caliber:
                    self._caliber["confidence"] = 99.9
                return True

            # partie 2 : combinaison regex + similiratude
            
            print(pPhrase)
            # construction liste monogram & bigram & trigram
            monogram = pPhrase.split(' ')
            bigram = []
            trigram = []

            index = 0
            words = pPhrase.split(' ')
            for word in words:
                if index+1 < len(words):
                    bigram.append(word + " " + words[index+1])
                    index = index + 1
                else:
                    bigram.append(word)
            
            index = 0
            words = pPhrase.split(' ')
            for word in words:
                if index+2 < len(words):
                    trigram.append(word + " " + words[index+1] + " " + words[index+2])
                    index = index + 1
                else:
                    trigram.append(word + " " + words[index+1])

            # check monogram
            monogramFound = False
            self._bestConfidenceVal = 0.0
            for word in monogram:
                if self.similaritude("unite", word) >= (self._seuil-(n*0.1)) or self.similaritude("unit", word) >= (self._seuil-(n*0.1)) or self.similaritude("uni", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "unite")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("element", word) >= (self._seuil-(n*0.1)) or self.similaritude("elemen", word) >= (self._seuil-(n*0.1)) or self.similaritude("elem", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "element")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("douzaine", word) >= (self._seuil-(n*0.1)) or self.similaritude("douzai", word) >= (self._seuil-(n*0.1)) or self.similaritude("dousain", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "douzaine")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("demi", word) >= (self._seuil-(n*0.1)) or self.similaritude("dem", word) >= (self._seuil-(n*0.1)) or self.similaritude("dmi", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "demi")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("fruit", word) >= (self._seuil-(n*0.1)) or self.similaritude("frui", word) >= (self._seuil-(n*0.1)) or self.similaritude("frit", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "fruit")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("pot", word) >= (self._seuil-(n*0.1)) or self.similaritude("pt", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "pot")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("botte", word) >= (self._seuil-(n*0.1)) or self.similaritude("bote", word) >= (self._seuil-(n*0.1)) or self.similaritude("btte", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "botte")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("millimietre", word) >= (self._seuil-(n*0.1)) or self.similaritude("milimietre", word) >= (self._seuil-(n*0.1)) or self.similaritude("milimietr", word) >= (self._seuil-(n*0.1)) or self.similaritude("mm", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "millimietre")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("centimetre", word) >= (self._seuil-(n*0.1)) or self.similaritude("centmtre", word) >= (self._seuil-(n*0.1)) or self.similaritude("cent", word) >= (self._seuil-(n*0.1)) or self.similaritude("cm", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "centimetre")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("inferieura", word) >= (self._seuil-(n*0.1)) or self.similaritude("inf", word) >= (self._seuil-(n*0.1)) or self.similaritude("<", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "inferieur a")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("superieura", word) >= (self._seuil-(n*0.1)) or self.similaritude("sup", word) >= (self._seuil-(n*0.1)) or self.similaritude(">", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "superieur a")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("gramme", word) >= (self._seuil-(n*0.1)) or self.similaritude("grame", word) >= (self._seuil-(n*0.1)) or self.similaritude("grme", word) >= (self._seuil-(n*0.1)) or self.similaritude("gr", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "gramme")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("xs", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "xs")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("fin", word) >= (self._seuil-(n*0.1)) or self.similaritude("fn", word) >= (self._seuil-(n*0.1)) or self.similaritude("petit", word) >= (self._seuil-(n*0.1)) or self.similaritude("ptit", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "fin")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("moyen", word) >= (self._seuil-(n*0.1)) or self.similaritude("moy", word) >= (self._seuil-(n*0.1)) or self.similaritude("medium", word) >= (self._seuil-(n*0.1)) or self.similaritude("med", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "moyen")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("grand", word) >= (self._seuil-(n*0.1)) or self.similaritude("gand", word) >= (self._seuil-(n*0.1)) or self.similaritude("large", word) >= (self._seuil-(n*0.1)) or self.similaritude("lrg", word) >= (self._seuil-(n*0.1)) or self.similaritude("larg", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "grand")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("xl", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "tres grand")
                    self._caliber["confidence"] = self._bestConfidenceVal
                    monogramFound = True
                elif self.similaritude("xxl", word) >= (self._seuil-(n*0.1)) or self.similaritude("unite", word) >= (self._seuil-(n*0.1)) or self.similaritude("unite", word) >= (self._seuil-(n*0.1)):
                    pPhrase = pPhrase.replace(word, "tres tres grand")
                    self._caliber["confidence"] = self._bestConfidenceVal
                if monogramFound == True:
                    break
                
            # check bigram
            bigramFound = False
            if monogramFound == False:
                self._bestConfidenceVal = 0.0
                for word in bigram:
                    if self.similaritude("demi douzaine", word) >= (self._seuil-(n*0.1)) or self.similaritude("dmi douzaine", word) >= (self._seuil-(n*0.1)) or self.similaritude("dmi douzai", word) >= (self._seuil-(n*0.1)):
                        pPhrase = pPhrase.replace(word, "unite")
                        self._caliber["confidence"] = self._bestConfidenceVal
                        bigramFound = True
                    elif self.similaritude("un demi", word) >= (self._seuil-(n*0.1)) or self.similaritude("u dmi", word) >= (self._seuil-(n*0.1)) or self.similaritude("un dmi", word) >= (self._seuil-(n*0.1)):
                        pPhrase = pPhrase.replace(word, "unite")
                        self._caliber["confidence"] = self._bestConfidenceVal
                        bigramFound = True
                    elif self.similaritude("inferieur a", word) >= (self._seuil-(n*0.1)) or self.similaritude("inf a", word) >= (self._seuil-(n*0.1)):
                        pPhrase = pPhrase.replace(word, "inferieur a")
                        self._caliber["confidence"] = self._bestConfidenceVal
                        monogramFound = True
                    elif self.similaritude("superieur a", word) >= (self._seuil-(n*0.1)) or self.similaritude("sup a", word) >= (self._seuil-(n*0.1)):
                        pPhrase = pPhrase.replace(word, "superieur a")
                        self._caliber["confidence"] = self._bestConfidenceVal
                        monogramFound = True
                    elif self.similaritude("tres fin", word) >= (self._seuil-(n*0.1)) or self.similaritude("trs fin", word) >= (self._seuil-(n*0.1)) or self.similaritude("tres petit", word) >= (self._seuil-(n*0.1)) or self.similaritude("trs petit", word) >= (self._seuil-(n*0.1)):
                        pPhrase = pPhrase.replace(word, "tres fin")
                        self._caliber["confidence"] = self._bestConfidenceVal
                        monogramFound = True
                    elif self.similaritude("superieur a", word) >= (self._seuil-(n*0.1)) or self.similaritude("sup a", word) >= (self._seuil-(n*0.1)):
                        pPhrase = pPhrase.replace(word, "superieur a")
                        self._caliber["confidence"] = self._bestConfidenceVal
                        monogramFound = True
                    elif self.similaritude("tres grand", word) >= (self._seuil-(n*0.1)) or self.similaritude("trs grand", word) >= (self._seuil-(n*0.1)) or self.similaritude("tres large", word) >= (self._seuil-(n*0.1)) or self.similaritude("trs large", word) >= (self._seuil-(n*0.1)):
                        pPhrase = pPhrase.replace(word, "tres grand")
                        self._caliber["confidence"] = self._bestConfidenceVal
                        monogramFound = True
                    elif self.similaritude("superieur a", word) >= (self._seuil-(n*0.1)) or self.similaritude("", word) >= (self._seuil-(n*0.1)):
                        pPhrase = pPhrase.replace(word, "superieur a")
                        self._caliber["confidence"] = self._bestConfidenceVal
                        monogramFound = True
                    elif self.similaritude("superieur a", word) >= (self._seuil-(n*0.1)) or self.similaritude("sup a", word) >= (self._seuil-(n*0.1)):
                        pPhrase = pPhrase.replace(word, "superieur a")
                        self._caliber["confidence"] = self._bestConfidenceVal
                        monogramFound = True
                    elif self.similaritude("superieur a", word) >= (self._seuil-(n*0.1)) or self.similaritude("sup a", word) >= (self._seuil-(n*0.1)):
                        pPhrase = pPhrase.replace(word, "superieur a")
                        self._caliber["confidence"] = self._bestConfidenceVal
                        monogramFound = True
                    elif self.similaritude("superieur a", word) >= (self._seuil-(n*0.1)) or self.similaritude("sup a", word) >= (self._seuil-(n*0.1)):
                        pPhrase = pPhrase.replace(word, "superieur a")
                        self._caliber["confidence"] = self._bestConfidenceVal
                        monogramFound = True
                    elif self.similaritude("superieur a", word) >= (self._seuil-(n*0.1)) or self.similaritude("sup a", word) >= (self._seuil-(n*0.1)):
                        pPhrase = pPhrase.replace(word, "superieur a")
                        self._caliber["confidence"] = self._bestConfidenceVal
                        monogramFound = True

                    if bigramFound == True:
                        break

            # check trigram
            if bigramFound == False:
                trigramFound = False
                self._bestConfidenceVal = 0.0
                for word in trigram:
                    if self.similaritude("tres tres grand", word) >= (self._seuil-(n*0.1)) or self.similaritude("trs tres grand", word) >= (self._seuil-(n*0.1)) or self.similaritude("trs trs grand", word) >= (self._seuil-(n*0.1)) or self.similaritude("trs tres large", word) >= (self._seuil-(n*0.1)) or self.similaritude("tres trs large", word) >= (self._seuil-(n*0.1)) or self.similaritude("trs trs large", word) >= (self._seuil-(n*0.1)):
                        pPhrase = pPhrase.replace(word, "tres tres grand")
                        self._caliber["confidence"] = self._bestConfidenceVal
                        trigramFound = True

                    if trigramFound == True:
                        break

            n = n + 1
        
        self._caliber = None
        return False

    # méthode qui trouve la quantite
    def parseQuantite(self, pPhrase) -> bool:
        self._quantite = {}

        ''' séparer les mots de nombres '''
        wordTmp = re.split('(\d+(?:[.,\s]\d{3})*(?:[.,]\d+)?)', pPhrase)
        pPhrase = ""
        for w in wordTmp:
            pPhrase = pPhrase + " " + w
        pPhrase = pPhrase.replace("  ", " ")

        n = 0
        while n < 3:
            # regex
            m = re.search('(\d+(?:[.,\s]\d{3})*(?:[.,]\d+)?)(?:| )(colis|kilo|kilogramme|kg)', pPhrase)

            if m:
                try:
                    self._quantite["value"] = float(m.group(1).replace(',', '.'))
                    self._quantite["type"] = "box" if (m.group(2) == "colis") else "kg"

                    if "confidence" not in self._quantite:
                        self._quantite["confidence"] = 99.9

                    return True
                except ValueError:
                    pass

            # regex + similitude
            self._bestConfidenceVal = 0.0 # reset self._bestConfidenceVal
            for word in pPhrase.split(' '):
                if self.similaritude("colis", word) >= (self._seuil-(n*0.1)):
                    self._quantite = {
                        "type": "box",
                        "confidence": self._bestConfidenceVal
                    }
                    self._bestConfidenceVal = 0.0
                    pPhrase = pPhrase.replace(word, "colis")
                elif self.similaritude("col", word) >= (self._seuil-(n*0.1)):
                    self._quantite = {
                        "type": "box",
                        "confidence": self._bestConfidenceVal
                    }
                    self._bestConfidenceVal = 0.0
                    pPhrase = pPhrase.replace(word, "colis")
                elif self.similaritude("kilo", word) >= (self._seuil-(n*0.1)):
                    self._quantite = {
                        "type": "kg",
                        "confidence": self._bestConfidenceVal
                    }
                    self._bestConfidenceVal = 0.0
                    pPhrase = pPhrase.replace(word, "kg")
                elif self.similaritude("kilogramme", word) >= (self._seuil-(n*0.1)):
                    self._quantite = {
                        "type": "kg",
                        "confidence": self._bestConfidenceVal
                    }
                    self._bestConfidenceVal = 0.0
                    pPhrase = pPhrase.replace(word, "kg")
                elif self.similaritude("kg", word) >= (self._seuil-(n*0.1)):
                    self._quantite = {
                        "type": "kg",
                        "confidence": self._bestConfidenceVal
                    }
                    self._bestConfidenceVal = 0.0
                    pPhrase = pPhrase.replace(word, "kg")

            n += 1

        self._quantite = None
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
        val = jarowinkler_similarity(a,b)
        if val > self._bestConfidenceVal:
            self._bestConfidenceVal = val
        return val