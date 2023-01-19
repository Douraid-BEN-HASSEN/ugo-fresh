from CResult import CResult

class CController:
    _result = None

    def __init__(self) -> None:
        self._result = CResult()

    def traitementIA(self, pPhrase, pSeuil) -> object:
        try:
            float(str(pSeuil))
        except ValueError:
            pSeuil = 0.8
        
        self._result.setSeuil(pSeuil)

        # get ean
        self._result.parseEan(pPhrase)

        # get prix
        self._result.parsePrix(pPhrase)

        # TODO: get autre info
        
        return self._result.toObject()