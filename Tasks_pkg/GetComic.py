import DMZJ_pkg
import asyncio
# 获取漫画
async def getComic_Take(DMZJ,startID=0,stopID=0):
    if (stopID-startID)<=0:
        return None
    tasks=[DMZJ.getComicInfo(ID) for ID in range(startID,stopID)]
    done,pending=await asyncio.wait(tasks)

    resultList=iter(list(done))
    mangars={}
    while True:
        try:
            node=next(resultList)
            mangar=node.result()
            if(isinstance(mangar, DMZJ_pkg.Comic)):
                mangars[mangar.getID()]=mangar
        except StopIteration as err:
            break
        except BaseException as err:
            print(err)
            raise err

    print("--ID",str(startID)+"-"+str(stopID-1),"获取完毕--")
    return mangars