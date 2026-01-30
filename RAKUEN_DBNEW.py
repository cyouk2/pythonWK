# -*- coding: UTF-8 -*-
import pymysql
import pandas as pd
from piadatainsertNew import SalesforceAccessNew
from sqlalchemy import create_engine

class RAKUENDBNew:
    
    def updateRenData(self,aren,kaiten,adate,Name,asort):
        # # 打开数据库连接
        db = pymysql.connect(host='localhost',user='root',password='541880qw',database='pia')
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # SQL
        sql02 = 'UPDATE piadata__c set aren = %s,kaiten= %s, isProcessed = 1 where adate= %s and Name= %s and asort= %s and isProcessed IS NULL ' 
        # save
        cursor.execute(sql02, (aren,kaiten,adate,Name,asort))
        db.commit()
        db.close()

    def countRenSub(self, indexTaiNo, adateTmp):
        engine = create_engine('mysql+pymysql://root:541880qw@localhost/pia?charset=utf8')
        params = {'name': indexTaiNo,'adate':adateTmp}
        # sql 命令
        sql_cmd = '''SELECT adate,Name,asort,orgkaiten,kaiten,atype,aren,isProcessed FROM pia.piadata__c 
            WHERE name = %(name)s 
            AND adate = %(adate)s
            AND atype IN (1,2) 
            ORDER BY adate, asort desc'''
        # データを読み込み
        df = pd.read_sql(sql=sql_cmd%params, con=engine)
        # print(sql_cmd%params)
        df['asortbk'] = df.shift(periods=1)['asort']
        df.fillna(0, inplace = True)
        rows = df.shape[0]

        for row in range(rows):
            # 最終スタートの場合
            if df.loc[row, 'atype'] == 2:
                df.loc[row, 'aren'] = 0
            else:
                df.loc[row, 'aren'] = df.loc[row, 'asortbk'] - df.loc[row, 'asort']

        for row in range(rows):
            # 最終スタートの場合
            if df.loc[row, 'atype'] == 2:
                df.loc[row, 'aren'] = 0
                if rows > 1:
                    if df.loc[row + 1, 'aren'] > 1:
                        df.loc[row, 'kaiten'] = df.loc[row, 'orgkaiten'] - 167
                    else:
                        df.loc[row, 'kaiten'] = df.loc[row, 'orgkaiten'] - 100
                else:
                    df.loc[row, 'kaiten'] = df.loc[row, 'orgkaiten']
            else:
                if row == rows - 1:
                    df.loc[row, 'kaiten'] = df.loc[row, 'orgkaiten']
                else:
                    if df.loc[row + 1, 'aren'] > 1:
                        df.loc[row, 'kaiten'] = df.loc[row, 'orgkaiten'] - 167
                    else:
                        df.loc[row, 'kaiten'] = df.loc[row, 'orgkaiten'] - 100
            self.updateRenData(df.loc[row, 'aren'],df.loc[row, 'kaiten'],adateTmp,indexTaiNo,df.loc[row, 'asort'])
        # print(df)
        print(df)
        return df

    def getRen(self, adateTmp, flg):
        if flg == 1:
            sa1 = SalesforceAccessNew('EVA15')
            for indexTaiNo1 in range(697,725):
                df1 = self.countRenSub(indexTaiNo1, adateTmp)
                # salesforce连携
                # sa1.main(df1)
        if flg == 2:
            sa2 = SalesforceAccessNew('EVA17')
            for indexTaiNo2 in range(585,613):
                # salesforce连携
                df2 = self.countRenSub(indexTaiNo2, adateTmp)
                # sa2.main(df2)

if __name__ == '__main__':  
    piaDB = RAKUENDBNew()
    piaDB.countRenSub(943, 260122)
    # piaDB.getRen(260111,2)