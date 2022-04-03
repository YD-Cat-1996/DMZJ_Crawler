import DMZJ_pkg.Comic
# headers信息
headers={
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-encoding":"gzip, deflate",
    'Accept-Language':'zh-CN,zh;q=0.9',
    "Cache-Control":"max-age=0",
    "User-Agent":"Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36",
    "referer":"https://manhua.dmzj.com/"
}

# 获取漫画信息
class DMZJ():
    # 初始化
    def init(self):
        # 最大ID和最大页数的请求
        import json
        import requests
        import configparser

        # 获取配置文件路径
        import os
        self.__configPath=os.path.dirname(__file__)
        self.__configPath=self.__configPath[:self.__configPath.rindex("DMZJ_pkg")]+"config.ini"
        self.__config=configparser.ConfigParser()
        isRead=self.__config.read(self.__configPath)
        # 检测配置文件是否存在
        if len(isRead)<=0:
            print("\n配置文件不存在，请在run.py文件目录下创建config.ini")
            import sys
            sys.exit()

        def __request(page=1):
            url="http://sacg.dmzj.com/mh/index.php?c=category&m=doSearch&callback=search.renderResult&p="+str(page)
            r=requests.get(url)
            text=r.text
            text = text.replace("search.renderResult(", "")
            text = text.replace(");", "")
            return json.loads(text)

        #获取总页数
        JSON=__request()
        self.maxPage=JSON["page_count"]
        #获取最大ID
        JSON=__request(self.maxPage)
        self.maxID=int(JSON["result"][len(JSON["result"])-1]["id"])

        try:
            # 获取已爬取到的ID
            self.gotID=int(self.__config.get("mangar","got_id"))
            self.isSplit= self.__config.get("config","is_split").lower() == "true"
            if self.isSplit:
                print("启用分页模式")
                self.split=int(self.__config.get("config","split"))
            else:
                print("不启用分页模式")
                self.split=self.maxID
        except configparser.NoOptionError as err:
            print("\n配置文件里 ["+err.section+"] 下不存在",err.option,"配置项\n请检查配置文件")
            import sys
            sys.exit()

    # 保存已爬取到的最大ID
    def setMaxID(self,ID=1):
        self.__config.set("mangar","got_id",str(ID))
        self.__config.write(open(self.__configPath,"w"))

    # 获取漫画信息
    async def __getInfo(self,ID):

        url="http://v3api.dmzj.com/comic/comic_"+str(ID)+".json?version=2.7.019"
        while True:
            print("ID:",ID,"获取中")
            try:
                import aiohttp
                import asyncio
                async with aiohttp.ClientSession() as session:
                    # 老版本aiohttp没有verify参数，如果报错卸载重装最新版本
                    async with session.get(url, headers=headers, timeout=15) as r:
                        # text()函数相当于requests中的r.text，r.read()相当于requests中的r.content
                        reponse = await r.text()
                        return reponse
            except asyncio.TimeoutError as err:
                print("ID:",ID,"超时,正在重新获取")
                await asyncio.sleep(1)
                continue
            except BaseException as err:
                print(err)
                import time
                time.sleep(1)
                continue

    async def getComicInfo(self, ID=1):
        comic=DMZJ_pkg.Comic()
        infoText=await self.__getInfo(ID)
        isGet=comic.setInfo(ID, infoText)
        if isGet:
            return comic
        else:
            return None
