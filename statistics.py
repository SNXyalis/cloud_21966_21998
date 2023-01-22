import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mongoengine as me
from models import Article, SDName
import datetime
import json
from collections import Counter

try:
    me.connect('fmk_assignment', host='localhost', port=27017)
except Exception as err:
    print(f'Error during connection to db {err}')
 
columns_data=[]
KEYWORDS_STR = [
    "Tesla", 
    "Microsoft", 
    "Apple",
    "Verizon",
    "Meta",
    "Coinbase",
    "Amazon",
    "Tencent"
]
today = datetime.datetime.today().strftime ('%d-%m-%Y') # format the date to ddmmyyyy

for i in range (5,0,-1):
    columns_data.append((datetime.datetime.today() - datetime.timedelta(days=i)).strftime ('%d-%m-%Y'))

tmp_ds =[] #a list with entris of format [keyword, date]

for entry in KEYWORDS_STR:#For every user keyword
        from mongoengine.queryset import QuerySet
        articles = Article.switch_collection(Article(), entry.capitalize())#Switch to the collection
        new_objects = QuerySet(Article,articles._get_collection())#Query all the document of the keyword
        d = {} #Documents in Python Object form
        for artcl in new_objects:
            d.update(json.loads(artcl.to_json()))#Format BSON to Python Object

        article_obj = d['articles'] #Array of articles
        for elem in article_obj: #For every document get source name and article
            dt = datetime.datetime.fromisoformat(elem['publishedAt'][:-1]).astimezone(datetime.timezone.utc).strftime ('%d-%m-%Y')
            tmp_ds.append([dt, entry])
            
tmp_keyw =[]
tmp_date = []
for elem in tmp_ds:
    tmp_date.append(elem[0])
    tmp_keyw.append(elem[1])
    #print(elem)
tmp_df = pd.DataFrame({'dt': tmp_date , 'keyw': tmp_keyw})
grouped_ds = tmp_df.groupby(['dt', 'keyw'])['dt'].count()

print(grouped_ds)
article_data_counts=[]
for i in columns_data:
    article_data_counts.append([0, 0, 0, 0, 0, 0, 0, 0])

for i, e in zip(grouped_ds.index, grouped_ds.values):
    for tdate in range(len(columns_data)):
        if columns_data[tdate]==i[0]:
            for kw in range(len(KEYWORDS_STR)):
                if KEYWORDS_STR[kw]==i[1]:
                    article_data_counts[tdate][kw]+=e

flag=0
for t in columns_data:
    article_data_counts[flag].insert(0, t)
    flag+=1
print(article_data_counts)




COLUMN_KEYWORDS = [
    "Dates",
    "Tesla", 
    "Microsoft", 
    "Apple",
    "Verizon",
    "Meta",
    "Coinbase",
    "Amazon",
    "Tencent"
]

df = pd.DataFrame(article_data_counts, columns=COLUMN_KEYWORDS)

df.plot(x='Dates', kind='bar', stacked=True, title='Articles per keyword during last 5 day')
plt.show()
