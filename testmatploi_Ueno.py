# -*- coding: UTF-8 -*-
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from piadatainsertNew import SalesforceAccessNew
from datetime import datetime, timedelta

class matploitTempTest:

    def showDetail(self,df1):

        for row11 in range(df1.shape[0]):
            print((df1.iloc[row11, 0],df1.iloc[row11, 1],df1.iloc[row11, 2],df1.iloc[row11, 3],df1.iloc[row11, 4]))
        print('-----------------------------')
    def countRenSub(self, indexTaiNo,adate):

        engine = create_engine('mysql+pymysql://root:541880qw@localhost/pia?charset=utf8')
        params = {'name': indexTaiNo,'adate':adate}
        # sql 命令
        sql_cmd = '''select 
            ROW_NUMBER() OVER(ORDER BY adate DESC, asort DESC) AS row_no,
            CONCAT(adate ,LPAD(asort,2,0)) as tindex,if(atype=1 OR atype=2 ,-1,kaiten) AS tkaiten,
            atype
            FROM pia.piadata__c 
            WHERE name = %(name)s 
            AND adate <= %(adate)s
            and kaiten >= 2
            AND atype IN (1,0) 
            ORDER BY adate DESC, asort DESC limit 400'''
        # データを読み込み
        df = pd.read_sql(sql=sql_cmd%params, con=engine)
        df['atypebk'] = df.shift(periods=-1)['atype']

        df.fillna(0, inplace = True)
        df = df.sort_values(by='tindex', ascending=True)
        # self.showDetail(df)
        df["tkaiten"] = df["tkaiten"].astype(int)
        df["atype"] = df["atype"].astype(int)
        df["atypebk"] = df["atypebk"].astype(int)
        # df = df.query('atype == 0')
        # print(df)
        # self.showDetail(df)
        return df
    
    def processData(self, indexTaiNo, cntbig, cntsmall,adate):

        df = self.countRenSub(indexTaiNo,adate)
        df = df.sort_values(by='tindex', ascending=False)
        rows = df.shape[0]
        danfaCnt = 0
        lineCnt = 0
        stLongCnt = 0
        quebianCnt = 0
        input_ALL97 = 0
        input_ALL = 0
        danfaCnt_A = 0
        input_ALL97_A = 0
        input_ALL_A = 0
        # print(indexTaiNo)
        # self.showDetail(df)
        for row1 in range(rows):
            # print(df.iloc[row1, 1])
            lineCnt += 1
            # 第一个确变的实际回转 0 确变 1 单发
            if df.iloc[row1, 3] == 0 and df.iloc[row1, 4] == 1:
                df.iloc[row1, 2] = df.iloc[row1, 2] + 157
            # 单发
            if df.iloc[row1, 3] == 1 and df.iloc[row1, 4] == 0:
                df.iloc[row1, 2] = 0
                # danfaCnt += 1
            # 单发    
            if df.iloc[row1, 3] == 1 and df.iloc[row1, 4] == 1:
                df.iloc[row1, 2] = 0
                danfaCnt += 1
            # 确变回转
            if df.iloc[row1, 2] > 0:
                # 确变回转和
                input_ALL += df.iloc[row1, 2]
                # 确变个数计数
                quebianCnt += 1 
            # 确变回转 大于80的统计    
            if df.iloc[row1, 2] > 70:
                # 确变个数计数
                stLongCnt += 1
                # 确变回转计数
                input_ALL97 += df.iloc[row1, 2]

            if quebianCnt == cntsmall:
                input_ALL97_A = input_ALL97
                input_ALL_A = input_ALL
                danfaCnt_A = danfaCnt
                # input_ALL97 = 0
                # input_ALL = 0
            if quebianCnt == cntbig:
                break
        # print((indexTaiNo,lineCnt - 20,quebianCnt,danfaCnt,input_ALL,input_ALL97))
        # print((indexTaiNo,
        #         lineCnt -20,
        #         input_ALL97_A,
        #         input_ALL97 - input_ALL97_A ,
        #         input_ALL - input_ALL_A,
        #         input_ALL))
        turulv = 0.5
        data97_A = (input_ALL97_A + danfaCnt_A * turulv * 157) 
        dat97 = (input_ALL97 + danfaCnt * turulv * 157) 

        data_A = (input_ALL_A + danfaCnt_A * turulv * 157) 
        data = (input_ALL_A + danfaCnt * turulv * 157) 

        results = (indexTaiNo,
                lineCnt - cntbig,
                data97_A,
                dat97,
                data_A,
                data
        )
        print(results)
        return results
        
    def getRen(self,cntbig,cntsmall,isToday,adate):
        listFor585 =[]
        for indexTaiNo4 in range(898,941):
            if indexTaiNo4 in range(912,927):
                continue
            listFor585.append(self.processData(indexTaiNo4,cntbig,cntsmall,adate))
        # salesforce连携
        sa2 = SalesforceAccessNew('EVA17')
        if isToday == 1:
            sa2.piadataupdatebk2(listFor585)
        # if isToday == 2:
        #     sa2.piadataupdatebk2(listFor585)
        
if __name__ == '__main__':

    piaDB = matploitTempTest()
    datetimetmp = datetime.now() - timedelta(days=1)
    adate = int(datetimetmp.strftime("%y%m%d"))
    piaDB.getRen(20,20,1,adate)
    # piaDB.processData(596,30,15,adate)
    # datetimetmp = datetime.now() - timedelta(days=2)
    # adate = int(datetimetmp.strftime("%y%m%d"))
    # piaDB.getRen(40,20,2,adate)
    # piaDB.getRen(30,15,2,adate)

    # piaDB.pltShow(592,350,adate)
    # piaDB.processData(607,150,20)