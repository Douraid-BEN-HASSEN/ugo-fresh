from CResult import CResult

class CController:
    _result = None

    def __init__(self, pSeuil = 0.8) -> None:
        if not str(pSeuil).isnumeric():
            pSeuil = 0.8

        self._result = CResult(pSeuil)

    def traitementIA(self, phrase) -> object:
        # get ean
        self._result.parseEan(phrase)

        # get prix
        self._result.parsePrix(phrase)

        return self._result.toObject()