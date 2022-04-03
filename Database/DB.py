import mysql.connector
class DB():
    def __init__(self):
        self.__dbConn=None

    # 初始化数据库
    def init(self,autoConnect=False):
        # 连接数据库
        self.__connect(autoConnect)
        # 创建表
        if not self.__dbConn is None:
            dbCursor=self.__dbConn.cursor()
            # 表创建语句
            sqls={
                # 漫画信息表
                "Comic_Info" : """CREATE TABLE `Comic_Info`  (
                `Comic_ID` int(10) UNSIGNED NOT NULL,
                `Title` varchar(100) NOT NULL,
                `Is_Status` bit(1) NOT NULL DEFAULT b'0',
                `Comic_py` varchar(100) NOT NULL,
                `Is_Hidden` bit(1) NOT NULL DEFAULT b'0' COMMENT '隐藏',
                `Is_Lock` bit(1) NOT NULL DEFAULT b'0' COMMENT '被买版权',
                `LastUpdateTime` datetime(0) NULL DEFAULT NULL,
                PRIMARY KEY (`Comic_ID`) USING BTREE,
                UNIQUE INDEX `Comic_Info_ID`(`Comic_ID`) USING BTREE,
                INDEX `Comic_Info_Title`(`Title`) USING BTREE
                )""",
                # 作者信息表
                "Author_Info":"""CREATE TABLE `Author_Info`  (
                `Author` varchar(50) NOT NULL,
                `Comic_ID` int(10) UNSIGNED NOT NULL,
                INDEX `Author`(`Author`) USING BTREE,
                INDEX `Author_Comic_ID`(`Comic_ID`) USING BTREE,
                CONSTRAINT `Author_Comic_ID` FOREIGN KEY (`Comic_ID`) REFERENCES `Comic_Info` (`Comic_ID`) ON DELETE CASCADE ON UPDATE CASCADE
                )""",
                # 漫画封面表
                "Comic_Cover":"""CREATE TABLE `Comic_Cover`  (
                `Comic_ID` int(10) UNSIGNED NOT NULL,
                `Cover` varchar(255) NULL DEFAULT NULL,
                PRIMARY KEY (`Comic_ID`) USING BTREE,
                INDEX `Cover_Comic_ID`(`Comic_ID`) USING BTREE,
                CONSTRAINT `Cover_Comic_ID` FOREIGN KEY (`Comic_ID`) REFERENCES `Comic_Info` (`Comic_ID`) ON DELETE CASCADE ON UPDATE CASCADE
                )""",
                # 漫画类型表
                "Comic_Type":"""CREATE TABLE `Comic_Type`  (
                `Type` varchar(10) NOT NULL,
                `Comic_ID` int(10) UNSIGNED NOT NULL,
                INDEX `Type`(`Type`) USING BTREE,
                INDEX `Type_Comic_ID`(`Comic_ID`) USING BTREE,
                CONSTRAINT `Type_Comic_ID` FOREIGN KEY (`Comic_ID`) REFERENCES `Comic_Info` (`Comic_ID`) ON DELETE CASCADE ON UPDATE CASCADE
                )""",
                # 漫画简介表
                "Comic_Description":"""CREATE TABLE `Comic_Description`  (
                `Comic_ID` int(10) UNSIGNED NOT NULL,
                `Description` text NULL,
                PRIMARY KEY (`Comic_ID`) USING BTREE,
                UNIQUE INDEX `Description_Comic_ID`(`Comic_ID`) USING BTREE,
                CONSTRAINT `Description_Comic_ID` FOREIGN KEY (`Comic_ID`) REFERENCES `Comic_Info` (`Comic_ID`) ON DELETE CASCADE ON UPDATE CASCADE
                )"""
            }
            for sql in sqls:
                try:
                    dbCursor.execute(sqls[sql])
                    print("表 '"+sql+"' 创建完成")
                except mysql.connector.errors.ProgrammingError as err:
                    if err.errno==1050:
                        msg=err.msg.replace("Table", "表")
                        msg=msg.replace("already exists","已存在")
                        print(msg)
                    else:
                        raise err
                except BaseException as err:
                    raise err
                    import sys
                    sys.exit()

    # 连接数据库
    def __connect(self,autoConnect=False):
        # 获取配置文件路径
        import os
        configPath=os.path.dirname(__file__)
        configPath=configPath[:configPath.rindex("Database")]+"config.ini"
        # 获取数据库的配置
        import configparser
        config=configparser.ConfigParser()
        config.read(configPath)
        try:
            __dbConfig={
                "user":config.get("db","user"),
                "password":config.get("db","password"),
                "host":config.get("db","host"),
                "port":config.get("db","port"),
                "connection_timeout":10
            }
            # 选择数据库
            dbName=config.get("db","database")
        except configparser.NoOptionError as err:
            print("\n配置文件里 ["+err.section+"] 下不存在",err.option,"配置项\n请检查配置文件")
            import sys
            sys.exit()

        # 连接数据库
        def __dbConnect():
            try:
                return mysql.connector.connect(**__dbConfig)
            except mysql.connector.Error as err:
                if err.errno==1049:
                    print("数据库连接失败，数据库",__dbConfig["database"],"尚未创建，请勿使用自动连接\n请使用DB().init(False)")
                elif err.errno==1045:
                    print("数据库登录失败, 请检查数据库帐号密码","\n错误代码:",err.errno,)
                elif err.errno==2003:
                    print("--数据库登录超时","\n错误代码::",err.errno)
                else:
                    print("数据库登录失败","\n错误内容:",err.msg,"错误代码:",err.errno)
                import sys
                sys.exit()
            except BaseException as err:
                raise err
                import sys
                sys.exit()

        # 是否自动连接数据库
        if autoConnect:
            __dbConfig["database"]=dbName
            self.__dbConn=__dbConnect()
            print("数据库",dbName,"已创建")
            return
        else:
            self.__dbConn=__dbConnect()
            dbCursor=self.__dbConn.cursor()
            try:
                dbCursor.execute("use "+dbName+";")
                print("数据库",dbName,"已创建")
                return
            except mysql.connector.Error as err:
                if err.errno==1049:
                    print("数据库连接失败，数据库",dbName,"尚未创建")
                    create=input("是否创建数据库(Y/N)：")
                    if create.upper() == "Y":
                        try:
                            dbCursor.execute("create database "+dbName+";")
                            dbCursor.execute("use "+dbName+";")
                            print("数据库",dbName,"创建完成")
                            return
                        except mysql.connector.errors.DatabaseError as err:
                            if err.errno==1007:
                                print("数据库",dbName,"无法创建，请检查数据库是否已存在")
                                import sys
                                sys.exit()
                    else:
                        print("程序退出")
                        import sys
                        sys.exit()
            except BaseException as err:
                raise err
                import sys
                sys.exit()


    '''
    保存漫画
    @:return 返回保存失败漫画
    '''
    async def save(self,comic):
        if not self.__dbConn is None:
            self.comic=comic
        self.__dbCursor=self.__dbConn.cursor()
        try:
            # 保存漫画信息
            await self.saveInfo()
            # 保存简介
            await self.saveDescription()
            # 保存封面
            await self.saveCover()
            # 保存作者信息
            await self.saveAuthors()
            # 保存类型信息
            await self.saveTypes()
        except BaseException as err:
            if err.errno==1062:
                import re
                r=re.search("\d+",err.msg)
                print("ID:", r.group(),"漫画已存在")
            return comic.getID()

        self.__dbConn.commit()
        self.__dbCursor.close()

    # 保存漫画信息
    async def saveInfo(self):
        # 保存漫画信息
        sql=("""
            INSERT INTO Comic_Info 
            (Comic_ID, Title, Is_Status, Comic_py, Is_Hidden, Is_Lock, LastUpdateTime) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""")
        val=(self.comic.getID(), self.comic.getTitle(), self.comic.getStatus(), self.comic.getComicPy(),
             self.comic.isHidden(), self.comic.isLock(), self.comic.getLastUpdateTime())
        try:
            self.__dbCursor.execute(sql, val)
        except mysql.connector.Error as err:
            if err.errno==1054:
                print("保存漫画信息失败")
                print("表 'Comic_Info' 不符合要求，请检查表的结构")
                import sys
                sys.exit()
            else:
                raise err

    # 保存作者信息
    async def saveAuthors(self):
        sql=("""INSERT INTO Author_Info 
             (Author, Comic_ID) 
             VALUES (%s, %s)""")
        val=[]
        for i in range(len(self.comic.getAuthors())):
            val.append((self.comic.getAuthors()[i],self.comic.getID()))

        try:
            self.__dbCursor.executemany(sql, val)
        except mysql.connector.Error as err:
            if err.errno==1054:
                print("保存作者信息失败")
                print("表 'Author_Info' 不符合要求，请检查表的结构")
                import sys
                sys.exit()
            else:
                raise err

    # 保存类型信息
    async def saveTypes(self):
        sql=("""INSERT INTO Comic_Type 
             (Type,Comic_ID) 
             VALUES (%s, %s)""")
        val=[]
        for i in range(len(self.comic.getTypes())):
            val.append((self.comic.getTypes()[i], self.comic.getID()))

        try:
            self.__dbCursor.executemany(sql, val)
        except mysql.connector.Error as err:
            if err.errno==1054:
                print("保存类型信息失败")
                print("表 'Comic_Type' 不符合要求，请检查表的结构")
                import sys
                sys.exit()

    # 保存封面
    async def saveCover(self):
        sql=("""INSERT INTO Comic_Cover 
             (Comic_ID, Cover) 
             VALUES (%s, %s)""")
        val=(self.comic.getID(), self.comic.getCover())

        try:
            self.__dbCursor.execute(sql, val)
        except mysql.connector.Error as err:
            if err.errno==1054:
                print("保存封面失败")
                print("表 'Comic_Cover' 不符合要求，请检查表的结构")
                import sys
                sys.exit()

    # 保存简介
    async def saveDescription(self):
        sql=("""INSERT INTO Comic_Description
             (Comic_ID, Description) 
             VALUES (%s, %s)""")
        val=(self.comic.getID(), self.comic.getDescription())

        try:
            self.__dbCursor.execute(sql, val)
        except mysql.connector.Error as err:
            if err.errno==1054:
                print("保存简介失败")
                print("表 'Comic_Description' 不符合要求，请检查表的结构")
                import sys
                sys.exit()
            else:
                raise err
