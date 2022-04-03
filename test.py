# 测试
import json
import requests
import time

if __name__=="__main__":
    while True:
        ID=50818
        url="http://v3api.dmzj.com/comic/comic_"+str(ID)+".json?version=2.7.019"
        r=requests.get(url)
        try:

            t=time.localtime()
            if r.json()["id"]==ID:
                print(str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday),
                      str(t.tm_hour)+":"+str(t.tm_min)+":"+str(t.tm_sec),
                      "ID:",ID,"获取成功")
        except json.decoder.JSONDecodeError as err:
            print(str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday),
                  str(t.tm_hour)+":"+str(t.tm_min)+":"+str(t.tm_sec),
                  "ID:",ID,"获取失败")
        time.sleep(1*60*60)