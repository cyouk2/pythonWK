# -*- coding: UTF-8 -*-
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from piadatainsertNew import SalesforceAccessNew
from datetime import datetime, timedelta

class matploitTempTest02:

    def showDetail(self,df1):
        df1 = df1.reset_index(drop=True)
        # print(f"row_no: {df1['kaiten'][3]}")
        # print(f"row_no: {df1.loc[3, 'kaiten']}")
        # print(f"row_no: {df1.iloc[3, 4]}")

        # for row in df1.itertuples():
        #     print(f"row_no: {row.row_no}, adate: {row.adate}, atype: {row.atype}")

        for row11 in range(df1.shape[0]):
            print((df1.loc[row11, 'adate'],
                   df1.loc[row11, 'Name'],
                   df1.loc[row11, 'atype'],
                   df1.loc[row11, 'kaiten'],
                   df1.loc[row11, 'asort']))

    def getFormatDate(self,dindex):
        
        datetimetmpEnd = datetime.now() - timedelta(days=dindex)
        adateEnd = int(datetimetmpEnd.strftime("%y%m%d"))
        return adateEnd

    def countRenSub(self, indexTaiNo):

        engine = create_engine('mysql+pymysql://root:541880qw@localhost/pia?charset=utf8')
        params = {'name': indexTaiNo}
        # sql 命令
        sql_cmd = '''SELECT adate,Name,atype,kaiten,aren,asort FROM pia.piadata__c 
            WHERE name = %(name)s 
            AND atype IN (1,2) 
            ORDER BY adate desc, asort desc limit 200 '''
        
        # データを読み込み
        df = pd.read_sql(sql=sql_cmd%params, con=engine)

        df.fillna(1, inplace = True)
        
        df = df.sort_index(ascending=False)

        return df
    
    def processData(self, indexTaiNo):

        df = self.countRenSub(indexTaiNo)

        dataType2 = 0
        rows = df.shape[0]
        df = df.reset_index(drop=True)
        # print(df)
        for row1 in range(rows):

            if df.loc[row1, 'atype'] == 2 and row1 !=(rows - 1) :
                dataType2 += df.loc[row1, 'kaiten']
                df.loc[row1, 'kaiten'] = 0
            if df.loc[row1, 'atype'] == 1:
                df.loc[row1, 'kaiten'] = df.loc[row1, 'kaiten'] + dataType2
                dataType2 = 0
        # print(df)
        df = df.query('kaiten != 0')
        df = df.sort_index(ascending=False)

        # print(df)
        # df['asortbk'] = df.shift(periods=1)['asort']
        df.fillna(0, inplace = True)
        # df = df[:cntbig]
        # df = df.sort_values(by='kaiten', ascending=False)
        # df = df[4:]
        df_reset = df.reset_index(drop=True)
        
        # # self.showDetail(df)
        # rows2 = df.shape[0]
        # print(rows2)
        return df_reset
        
    def getRen(self,startIndex,endIndex,flg):

        bean ={}
        bean['Name'] = []
        bean['mean'] = []
        bean['std'] = []
        bean['mean_std'] = []
        bean['max'] = []
        bean['count'] = []
        
        
        rang1 = range(585,613)
        if flg == 15:
            rang1 = range(697,725)

        for indexTaiNo4 in rang1:
            
            df = self.processData(indexTaiNo4)
            
            dfgroupbybk = df.copy().groupby('adate', as_index=False).agg('max')
          
            
            dfgroupbybkadatebk = dfgroupbybk[-1 * endIndex:]['adate']
            if startIndex != 0:
                dfgroupbybkadatebk = dfgroupbybk[-1 * endIndex : -1 * startIndex]['adate']
            # print(dfgroupbybkadatebk)

            adateEnd = dfgroupbybkadatebk.max()
            adateStart =  dfgroupbybkadatebk.min()

            print(f"{indexTaiNo4} :  {adateStart} ~ {adateEnd}")

            df = df.query(f'adate >= {adateStart} and adate <= {adateEnd}')

            df_kaiten = df['kaiten']
            mean = round(df_kaiten.mean(),0)
            std = round(df_kaiten.std(),0)

            bean['Name'].append(indexTaiNo4)
            bean['mean'].append(mean)
            bean['std'].append(std)
            bean['max'].append(df_kaiten.max())
            bean['count'].append(df_kaiten.count())
            bean['mean_std'].append(mean + std)
           
        dfbean = pd.DataFrame(bean)
        
        # dfbean = dfbean.copy().sort_values(by='mean_std', ascending=True)
        # print(dfbean)
        listFor585 =[]
        for row in dfbean.itertuples():
            bean ={}
            bean['Name'] = row.Name
            bean['data1'] = row.mean
            bean['data2'] = row.std
            bean['data3'] = row.mean_std
            bean['data4'] = row.max
            bean['data5'] = row.count
            listFor585.append(str(bean))
            # print(result)
            # listFor585.append(result)

        # SalesforceAccess
        
        if flg == 15:
            sa2 = SalesforceAccessNew(711)
            sa2.piadataupdatebk2(listFor585)
        else:
            sa2 = SalesforceAccessNew(585)
            sa2.piadataupdatebk2(listFor585)
        
if __name__ == '__main__':

    piaDB = matploitTempTest02()
    dateS = 0
    detaE = (dateS + 1) + 1
    piaDB.getRen(dateS,detaE,15)
    # piaDB.pltShow(592,350,adate)