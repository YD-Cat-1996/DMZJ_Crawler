import DMZJ_pkg
import asyncio
import time


if __name__=="__main__":
    while True:
        start_time=time.time()
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
        print("——————初始化DMZJ——————")
        # 初始化DMZJ类
        DMZJ=DMZJ_pkg.DMZJ()
        DMZJ.init()
        # DMZJ.maxID=660
        print("DMZJ返回最大ID:",DMZJ.maxID)
        # 计算分页次数
        startID=DMZJ.gotID+1
        shengyuNum=DMZJ.maxID-DMZJ.gotID
        page=shengyuNum/DMZJ.split
        print("——————初始化数据库——————")
        # 初始化数据库
        import Database
        db=Database.DB()
        db.init(False)

        count=0 # 统计保存数量
        import Tasks_pkg
        take=Tasks_pkg.Take(DMZJ)
        # 执行任务
        print("——————初始化完成——————")
        try:
            for i in range(1,int(page)+2):
                print("\n———————开始获取———————")
                if i<int(page)+1:
                    stopID=int(DMZJ.gotID)+(i*DMZJ.split)+1
                    print("startID:",startID,"stopID:",stopID-1)

                else:
                    stopID=DMZJ.maxID+1
                    print("startID:",startID,"stopID:",DMZJ.maxID)

                loop=asyncio.get_event_loop()
                # 执行获取任务
                comics=loop.run_until_complete(take.getComic(startID,stopID))
                # 执行保存任务
                print("———————正在保存———————")
                done=loop.run_until_complete(take.saveComic(db,comics))
                if done is None:done=0
                print("本次保存数量：",done)
                startID=stopID

                count+=done

                print("------第",i,"轮结束------")
                # 本轮结束后休息
                time.sleep(1)
        except KeyboardInterrupt as err:
            print("\n程序主动退出")
            import sys
            sys.exit()
        except BaseException as err:
            raise err
        print("-------全部结束-------")
        print("\n总保存数量:",count)
        print("耗时:",str(time.time()-start_time)+"s")
        print("—————————————————————\n")
        time.sleep(1*60*60*2)
