import urllib2
import json
import time
import pandas as pd
from pandas import DataFrame
import hashlib

public_key = "INSERT PUBLIC KEY HERE"
private_key = "INSERT PRIVATE KEY HERE"

limit = 100
offset = 0
iterations = 15 	# only <1500 characters
df = DataFrame()

for i in xrange(iterations):
	ts = str(int(time.time()))
	hash = hashlib.md5(ts + private_key + public_key).hexdigest()
	request_url = 'http://gateway.marvel.com/v1/public/characters?ts=%s&apikey=%s&hash=%s&limit=%s&offset=%s' % (ts, public_key, hash, limit, offset)
	req = urllib2.Request(request_url)
	response = urllib2.urlopen(req)
	data = json.loads(response.read())["data"]["results"]
	df = df.append(data,ignore_index=True)
	offset = offset + limit

for col in ["comics","events","series","stories"]:
	df[col] = df[col].map(lambda x: x["available"])
	
ordered_df = df[["name", "comics", "series", "stories", "events"]]
ordered_df = ordered_df.sort("comics", ascending=False)
ordered_df.to_csv("marvel_characters.csv",encoding='utf-8', index=False)