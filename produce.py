from time import sleep  
from json import dumps  
import kafka, requests, json
from requests.exceptions import HTTPError
 
k_producer = kafka.KafkaProducer(  
    bootstrap_servers = ['localhost:9092'],  
    value_serializer = lambda x:dumps(x).encode('utf-8')  
) 

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
            response = requests.get('https://newsapi.org/v2/everything?q='+key_+'&from=2022-10-21&sortBy=popularity&apiKey=dfa72c75b9ec4b3d8470b1786f586658')
            response.raise_for_status()
            data = json.loads(response.text)
            filtered_data = {
                'keyword': key_,
                'articles': data['articles']
            }

            #Filter the source names
            for entry in data['articles']:
                sources_list.add(entry['source']['name'])

            #Sends only the articles
            k_producer.send(topic=key_, value=filtered_data)
    
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
                        k_producer.send(topic='Sourcedomainname', value=filtered_data)

            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                print(f'Other error occurred: {err}')


        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
    
get_newsapi_data()

def automate_api_call():
    while True:
        get_newsapi_data()
        sleep(7200)
