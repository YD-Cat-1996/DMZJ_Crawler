class Comic(object):
    def __init__(self):
        self.__cover=""
        self.__ID=0
        self.__title=""
        self.__authors=[]
        # 介绍
        self.__description=""
        self.__types=[]
        # 连载状态
        self.__status=False
        # 简拼
        self.__comic_py=""
        self.__last_updatetime=""
        # 是否被隐藏
        self.__hidden=False
        # 是否被买版权
        self.__is_lock=False
    def getCover(self):
        return self.__cover
    def getID(self):
        return self.__ID
    def getTitle(self):
        return self.__title
    def getAuthors(self):
        return self.__authors
    def getDescription(self):
        return self.__description
    def getTypes(self):
        return self.__types
    def getStatus(self):
        return self.__status
    def getComicPy(self):
        return self.__comic_py
    def getLastUpdateTime(self):
        return self.__last_updatetime
    def isHidden(self):
        return self.__hidden
    def isLock(self):
        return self.__is_lock

    # 设置属性
    def __setInfo(self,JSON):
        # ID
        if JSON["id"] is None or JSON["id"] <0:
            return False
        self.__ID=JSON["id"]
        # 封面
        self.__cover=JSON["cover"]
        # 漫画名
        if JSON["title"][0]=="+":
            self.__title=JSON["title"][1:]
        else:
            self.__title=JSON["title"]
        # 作者
        for author in JSON["authors"]:
            self.__authors.append(author["tag_name"])
        self.__description=JSON["description"]
        # 类型
        for type in JSON["types"]:
            self.__types.append(type["tag_name"])
        # 连载状态
        if JSON["status"][0]["tag_name"]=="连载中":
            self.__status=False
        else:
            self.__status=True
        # 简拼
        self.__comic_py=JSON["comic_py"]
        #  最后更新时间
        import time
        if(JSON["last_updatetime"]<0):
            JSON_Time=0
        else:
            JSON_Time=JSON["last_updatetime"]
        self.__last_updatetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(JSON_Time))
        # 是否被隐藏
        self.__hidden=bool(JSON["hidden"])
        # 是否被买版权
        self.__is_lock=bool(JSON["is_lock"])
    def setInfo(self,ID,text):
        from json import JSONDecodeError
        import json
        try:
            JSON=json.loads(text)
        except JSONDecodeError:
            # print("ID: "+str(ID)+",漫画获取失败")
            return False

        try:
            self.__setInfo(JSON)
            print("ID:",str(ID),"漫画获取成功")
            return True
        except KeyError:
            return False
        except BaseException as err:
            raise err
            return False