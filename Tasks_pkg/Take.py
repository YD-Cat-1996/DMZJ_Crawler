from .GetComic import *
from .SaveComic import *
class Take:
    def __init__(self,DMZJ):
        self.__DMZJ=DMZJ
    def getComic(self,startID=0,stopID=0):
        return getComic_Take(self.__DMZJ,startID,stopID)
    def saveComic(self,db,comics):
        return saveComic_Take(self.__DMZJ,db,comics)