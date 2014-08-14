#!/usr/bin/env python
# -*- coding:utf-8 -*-
# -*- author:liuguanyu -*-
# python抓取笑话类的工厂


from thirdpart import hao360fetcher , qiubaifetcher , mahuafetcher


class Fetcher :
    def fetch(self , user_id):
        if user_id == "1":
            f = hao360fetcher.Hao360Fetcher()         
        elif user_id == "2":
            f = qiubaifetcher.QiubaiFetcher()     
        elif user_id == "3":
            f = mahuafetcher.MahuaFetcher()    
        else :
            return []
       
        
        res = [] 
        rets = []
    
        while f.is_need_next() :
            con = f.get()
            res.extend(f.parse(con)) 
    
        for item in res :
            item["user_id"] = user_id
            rets.append(item)

        return rets    

def main():    
    pass   

if __name__ == "__main__":
    main()