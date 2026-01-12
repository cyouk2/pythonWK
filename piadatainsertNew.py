# -*- coding: UTF-8 -*-
import ssl
import json
import requests
import configparser

class SalesforceAccessNew:
    def __init__(self, database):
        ssl._create_default_https_context = ssl._create_unverified_context
        HOST = 'login.salesforce.com'

        config = configparser.ConfigParser()
        config.read('config.ini',encoding='utf-8')
        print(database)
        params = {
            'grant_type': 'password',
            'client_id': config.get(database,'client_id'),
            'client_secret': config.get(database,'client_secret'),
            'username': config.get(database,'username'),
            'password': config.get(database,'password')
        }
        print(params['username'])   
        res_post = requests.post('https://{}/services/oauth2/token'.format(HOST), params=params)
        # print('https://{}/services/oauth2/token'.format(HOST))
        # print(res_post.json())
        access_token = res_post.json().get('access_token')
        # print(access_token)
        self.instance_url = res_post.json().get('instance_url')
        # print(instance_url)
        self.headers = {
            'Content-type': 'application/json',
            'Accept-Encoding': 'gzip',
            'Authorization': 'Bearer {}'.format(access_token)
        }

    def main(self,df):
        
        services_url = '/services/apexrest/piadata/'
        strUrl = self.instance_url + services_url
        # adate  Name  asort  kaiten  atype  aren  asortbk
        beans =[]
        for row in range(df.shape[0]):
            bean ={}
            bean['adate'] = int(df.iloc[row, 0])
            bean['Name'] = int(df.iloc[row, 1])
            bean['asort'] = int(df.iloc[row, 2])
            bean['kaiten'] = int(df.iloc[row, 3])
            bean['atype'] = int(df.iloc[row, 4])
            bean['aren'] = int(df.iloc[row, 5])
            beans.append(bean)
        obj = {
            'beans':beans
        }
        json_data = json.dumps(obj)
        res_get = requests.post(url=strUrl, headers=self.headers, data=json_data, timeout=10)
        print(res_get.json())

    def piadataupdatebk2(self,beans):
        
        services_url = '/services/apexrest/piadataupdatebk2/'
        strUrl = self.instance_url + services_url

        obj = {
            'beans':beans
        }
        # print(obj)
        json_data = json.dumps(obj)
        res_get = requests.post(url=strUrl, headers=self.headers, data=json_data, timeout=10)
        print(res_get.json())
