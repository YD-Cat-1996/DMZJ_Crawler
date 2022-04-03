import asyncio
# 保存漫画
async def saveComic_Take(DMZJ,db,mangars):
    if mangars is None:
        return 0
    # 复制一份保存列表
    saveSuccess=mangars.copy()
    if (not mangars is None) and (len(mangars)>=1):
        tasks=[db.save(mangars[ID]) for ID in mangars]
        done,pending=await asyncio.wait(tasks)
        # 获取保存失败的漫画
        resultList=iter(list(done))
        saveFail=[]
        while True:
            try:
                node=next(resultList)
                saveFail.append(node.result())
            except StopIteration :
                break
        # 剔除保存失败的漫画
        for ID in saveFail:
            if not ID is None:
                saveSuccess.pop(ID)

    # 保存已获取到的最大ID
    maxID=0
    if (not saveSuccess is None) and (len(saveSuccess)>=1):
        maxID=max(saveSuccess)
        DMZJ.setMaxID(maxID)
    print("-------保存完毕-------")
    print("本次保存最大ID:",maxID)
    return len(saveSuccess)
