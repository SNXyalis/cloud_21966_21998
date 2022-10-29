from json import loads  
from kafka import KafkaConsumer  
from pymongo import MongoClient  


my_consumer = KafkaConsumer(  
    'testnum',  
     bootstrap_servers = ['localhost : 9092'],  
     auto_offset_reset = 'earliest',  
     enable_auto_commit = True,  
     group_id = 'my-group',  
     value_deserializer = lambda x : loads(x.decode('utf-8'))  
     )  

my_client = MongoClient('localhost : 27017')  
my_collection = my_client.testnum.testnum  


for message in my_consumer:  
    message = message.value  
    my_collection.insert_one(message)  
    print(message + " added to " + my_collection)  