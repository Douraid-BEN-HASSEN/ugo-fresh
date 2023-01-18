from CResult import CResult

class CController:
    _result = None

    def __init__(self) -> None:
        self._result = CResult()

    def traitementIA(self, pPhrase, pSeuil) -> object:
        if not str(pSeuil).isnumeric():
            pSeuil = 0.8
        
        self._result.setSeuil(pSeuil)
        
        # get ean
        self._result.parseEan(pPhrase)

        # get prix
        self._result.parsePrix(pPhrase)

        return self._result.toObject()