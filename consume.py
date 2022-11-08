from json import loads  
from kafka import KafkaConsumer  
#from pymongo import MongoClient  
from models import Article, SDName
from time import sleep
import mongoengine as me

try:
    me.connect('fmk_assignment', host='localhost', port=27017)
except Exception as err:
    print(f'Error during connection to db {err}')

topics = [
    "Tesla", 
    "Microsoft", 
    "Apple",
    "Verizon",
    "Meta",
    "Coinbase",
    "Amazon",
    "Tencent",
    "Sourcedomainname"
]


tesla_consumer = KafkaConsumer(    
    client_id='tesla-consumer',
    bootstrap_servers = ['localhost : 9092'],     
    auto_offset_reset='earliest',
    consumer_timeout_ms=1000,
    value_deserializer=lambda m:loads(m.decode('utf-8'))  
)  
tesla_consumer.subscribe(topics=topics[0])

microsoft_consumer = KafkaConsumer(    
    client_id='microsoft-consumer',
    bootstrap_servers = ['localhost : 9092'],     
    auto_offset_reset='earliest',
    consumer_timeout_ms=1000,
    value_deserializer=lambda m:loads(m.decode('utf-8'))  
)  
microsoft_consumer.subscribe(topics=topics[1])

apple_consumer = KafkaConsumer(    
    client_id='apple-consumer',
    bootstrap_servers = ['localhost : 9092'],     
    auto_offset_reset='earliest',
    consumer_timeout_ms=1000,
    value_deserializer=lambda m:loads(m.decode('utf-8'))   
)  
apple_consumer.subscribe(topics=topics[2])

verizon_consumer = KafkaConsumer(    
    client_id='verizon-consumer',
    bootstrap_servers = ['localhost : 9092'],     
    auto_offset_reset='earliest',
    consumer_timeout_ms=1000,
    value_deserializer=lambda m:loads(m.decode('utf-8'))   
)  
verizon_consumer.subscribe(topics=topics[3])

meta_consumer = KafkaConsumer(    
    client_id='meta-consumer',
    bootstrap_servers = ['localhost : 9092'],     
    auto_offset_reset='earliest',
    consumer_timeout_ms=1000,
    value_deserializer=lambda m:loads(m.decode('utf-8'))   
)  
meta_consumer.subscribe(topics=topics[4])

coinbase_consumer = KafkaConsumer(    
    client_id='coinbase-consumer',
    bootstrap_servers = ['localhost : 9092'],     
    auto_offset_reset='earliest',
    consumer_timeout_ms=1000,
    value_deserializer=lambda m:loads(m.decode('utf-8'))  
)  
coinbase_consumer.subscribe(topics=topics[5])

amazon_consumer = KafkaConsumer(    
    client_id='amazon-consumer',
    bootstrap_servers = ['localhost : 9092'],     
    auto_offset_reset='earliest',
    consumer_timeout_ms=1000,
    value_deserializer=lambda m:loads(m.decode('utf-8'))  
)  
amazon_consumer.subscribe(topics=topics[6])

tencent_consumer = KafkaConsumer(    
    client_id='tencent-consumer',
    bootstrap_servers = ['localhost : 9092'],     
    auto_offset_reset='earliest',
    consumer_timeout_ms=1000,
    value_deserializer=lambda m:loads(m.decode('utf-8'))   
)  
tencent_consumer.subscribe(topics=topics[7])

sdn_consumer = KafkaConsumer(    
    client_id='sdn-consumer',
    bootstrap_servers = ['localhost : 9092'],     
    auto_offset_reset='earliest',
    consumer_timeout_ms=1000,
    value_deserializer=lambda m:loads(m.decode('utf-8'))  
)  
sdn_consumer.subscribe(topics=topics[8])




def consumer_save(topic):
    print('polling...')
    records=None #Articles and SDN entries from consumer
    
    if topic.capitalize() in topics:
        if topic == topics[0]:
            records = tesla_consumer.poll(timeout_ms=1000)
        elif topic == topics[1]:
            records = microsoft_consumer.poll(timeout_ms=1000)
        elif topic == topics[2]:
            records = apple_consumer.poll(timeout_ms=1000)
        elif topic == topics[3]:
            records = verizon_consumer.poll(timeout_ms=1000)
        elif topic == topics[4]:
            records = meta_consumer.poll(timeout_ms=1000)
        elif topic == topics[5]:
            records = coinbase_consumer.poll(timeout_ms=1000)
        elif topic == topics[6]:
            records = amazon_consumer.poll(timeout_ms=1000)
        elif topic == topics[7]:
            records = tencent_consumer.poll(timeout_ms=1000)
        elif topic == topics[8]:
            records = sdn_consumer.poll(timeout_ms=1000)
            for key, value in records.items():#Special case for sdn
                for record in value:
                    data = record.value

                    sdn = SDName(name=data["name"], description=data['description'])
                    sdn.switch_collection(topic.capitalize())
                    sdn.save()
        
                    print(data["name"])
                    print(data["description"])
                    print()
                break
            return


        for key, value in records.items():#Save articles in corresponding collection
            for record in value:
                data = record.value

                articles = Article(keyword=data["keyword"], articles=data['articles'])

                if data["keyword"].capitalize() in topics:
                    articles.switch_collection(data["keyword"].capitalize())
                    articles.save()
        
                print(data["keyword"])
                print(data["articles"])
                print()
            break
    return


def producer_run(): #Call consumers and save data to MongoDB every 2 hours
    while True:
        for entry in topics:
            consumer_save(entry)
        sleep(7200)


producer_run()
