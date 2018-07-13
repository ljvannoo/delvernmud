#!/usr/bin/env python3

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['blackpy']
accounts = db['test_account']
result = accounts.find({})

print(result.count())
# for account in result:
#   print(account)