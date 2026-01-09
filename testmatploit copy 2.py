# -*- coding: UTF-8 -*-
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from piadatainsertNew import SalesforceAccessNew
from datetime import datetime, timedelta

class matploitTempTest02:

    def showDetail(self,df1):

        for row11 in range(df1.shape[0]):
            print((df1.iloc[row11, 0],df1.iloc[row11, 1],df1.iloc[row11, 2],df1.iloc[row11, 3],df1.iloc[row11, 4],df1.iloc[row11, 5],df1.iloc[row11, 6]))
        print('-----------------------------')
    def countRenSub(self, indexTaiNo,adate):

        engine = create_engine('mysql+pymysql://root:541880qw@localhost/pia?charset=utf8')
        params = {'name': indexTaiNo,'adate':adate}
        # sql 命令
        sql_cmd = '''SELECT dt.* FROM (SELECT ROW_NUMBER() OVER(ORDER BY adate desc, asort desc) as row_no,adate,Name,atype,kaiten,aren,asort FROM pia.piadata__c 
            WHERE name = %(name)s 
            AND atype IN (1,2) 
            ORDER BY adate desc, asort desc limit 20 ) dt order by row_no desc'''
        
        # データを読み込み
        df = pd.read_sql(sql=sql_cmd%params, con=engine)

        df.fillna(1, inplace = True)
        # self.showDetail(df)
        print(df)
        return df
    
    def processData(self, indexTaiNo, cntbig,adate):

        df = self.countRenSub(indexTaiNo,adate)
        dataType2 = 0
        rows = df.shape[0]

        for row1 in range(rows):
            # print(df.iloc[row1, 0])
            if df.iloc[row1, 3] == 2 and row1 !=(rows - 1) :
                dataType2 += df.iloc[row1, 4]
                df.iloc[row1, 4] = 0
            if df.iloc[row1, 3] == 1:
                df.iloc[row1, 4] = df.iloc[row1, 4] + dataType2
                dataType2 = 0
        df = df.query('kaiten != 0')
        df = df.sort_values(by='row_no', ascending=True)
        df['asortbk'] = df.shift(periods=1)['asort']
        df.fillna(0, inplace = True)
        # df = df[:cntbig]
        print(df)
        # self.showDetail(df)
        # df = df.sort_values(by='kaiten', ascending=False)
        # # self.showDetail(df)
        # df = df[4:]
        # # self.showDetail(df)
        # rows2 = df.shape[0]
        # print(rows2)
        return df
        
    def getRen(self,cntbig,adate):

        listFor585 =[]
        for indexTaiNo4 in range(585,586):
            # if indexTaiNo4 in [585,594]:
            #     continue
            # listFor585.append(self.processData(indexTaiNo4,cntbig,adate))
        # listFor585.append(self.processData(585,cntbig,adate))
            print('-----------------------------------')
            df = self.processData(indexTaiNo4,cntbig,adate)
            for rows21 in range(cntbig):
                result = (df.iloc[rows21, 1],df.iloc[rows21, 2],df.iloc[rows21, 6],df.iloc[rows21, 4],df.iloc[rows21, 3],df.iloc[rows21, 5])
                print(result)
                listFor585.append(result)
        
        
        # listFor585.append(self.processData(585,cntbig,adate))
        # salesforce连携
        # sa2 = SalesforceAccessNew(1062)
        # if isToday == 1:
        # sa2.main(listFor585)
        # if isToday == 2:
        #     sa2.piadataupdatebk2(listFor585)
        
if __name__ == '__main__':

    piaDB = matploitTempTest02()
    datetimetmp = datetime.now() - timedelta(days=1)
    adate = int(datetimetmp.strftime("%y%m%d"))
    piaDB.getRen(10,adate)
    # piaDB.countRenSub(585,250925)
    # piaDB.processData(596,30,15,adate)
    # datetimetmp = datetime.now() - timedelta(days=2)
    # adate = int(datetimetmp.strftime("%y%m%d"))
    # piaDB.getRen(40,20,2,adate)
    # piaDB.getRen(30,15,2,adate)

    # piaDB.pltShow(592,350,adate)
    # piaDB.processData(607,150,20)