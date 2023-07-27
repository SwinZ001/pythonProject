import json

import MySQLdb
import redis


def process_item():
    rediscli = redis.Redis(host="127.0.0.1",port=6379,db=0)

    mysqlcli = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="123456",db="test")
    while True:

        source,data = rediscli.blpop("amazon:items")
        item = json.loads(data)
        print(item)


        cursor = mysqlcli.cursor()

        cursor.execute('insert into amazon_data (commodity_link,commodity_name,commodity_price) value (%s,%s,%s)',(item['commodity_link'],item['commodity_name'],item['commodity_price']))
        mysqlcli.commit()




if __name__ == '__main__':
    process_item()
