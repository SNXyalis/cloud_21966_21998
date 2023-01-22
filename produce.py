from time import sleep  
from json import dumps  
import kafka, requests, json
from requests.exceptions import HTTPError
import mongoengine as me
from models import SingleArticle
from datetime import datetime

try:
    me.connect('fmk_assignment', host='localhost', port=27017)
except Exception as err:
    print(f'Error during connection to db {err}')
 
k_producer = kafka.KafkaProducer(  
    bootstrap_servers = ['localhost:9092'],  
    value_serializer = lambda x:dumps(x).encode('utf-8')  
) 

DATE=datetime.today().strftime('%Y-%m-%d')

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

def get_newsapi_data():
    for key_ in KEYWORDS_STR:

        sources_list = set() #Strings of article sources / sources name
        try:

            #Get newsapi and filter the articles
            response = requests.get('https://newsapi.org/v2/everything?q='+key_+'&from='+DATE+'&sortBy=popularity&apiKey=dfa72c75b9ec4b3d8470b1786f586658')
            response.raise_for_status()
            data = json.loads(response.text)
            filtered_data = {
                'keyword': key_,
                'articles': data['articles']
            }

            #Filter the source names
            for entry in data['articles']:
                # Add article to mongodb
                singleArticle = SingleArticle(**entry)
                singleArticle.save()

                sources_list.add(entry['source']['name'])

            #Sends only the articles
            try:
                k_producer.send(topic=key_, value=filtered_data)
            except Exception as topic_err:
                print(f'Kafka-Producer topic error occured: {topic_err}')

            try:
                for entry in sources_list:
                    response = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&exlimit=1&titles='+entry+'&explaintext=1&format=json')
                    response.raise_for_status()
                    data = json.loads(response.text)

                    #Filter title and description
                    src_name, src_desc = None, None 

                    for value in data['query']['pages']:
                        src_name = data['query']['pages'][value]['title']
                        src_desc = data['query']['pages'][value]['extract']

                    #if there are values, send the msg
                    if src_name or src_desc:
                        filtered_data = {
                            'name': src_name,
                            'description': src_desc
                        }

                        try:
                            k_producer.send(topic='Sourcedomainname', value=filtered_data)
                        except Exception as sdn_err:
                            print(f'Kafka-Producer source domain name error occured: {sdn_err}')

            except HTTPError as http_sdn_err:
                print(f'HTTP error on sdn occurred: {http_sdn_err}')
            except KeyError:
                print(f'Description for {entry} not found')
            except Exception as other_sdn_err:
                print(f'Other error on sdn occurred: {other_sdn_err}')


        except HTTPError as http_err:
            print(f'HTTP error on topic occurred: {http_err}')
        except Exception as err:
            print(f'Other error on topic occurred: {err}')
    
def producer_run():#Call producer and queue data from APIs every 2 hours
    while True:
        DATE = datetime.today().strftime('%Y-%m-%d')
        get_newsapi_data()
        sleep(7200)


producer_run()
