#!/usr/bin/python3

import json, re, time, requests, logging, traceback, codecs

#config
pastebin = 'https://pastebin.com/raw/'
post_limit = '100'
urlposts = 'https://scrape.pastebin.com/api_scraping.php?limit='
wait = 60

#loading regex
with open('regex.json', 'r') as f:
    j = json.load(f)
j_reg = j['regex_pasta']

#log settings
logging.basicConfig(filename='pasta.log',level=logging.INFO,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S%p')


restart=True
def pasta():
        logging.info('Loop Started!')      
        p_posts = requests.get(f'{urlposts}{post_limit}')
        p_json = json.loads(p_posts.content)
        
        for x in j_reg:
                xnam = (x['name']) 
                xreg = (x['regex'])
                for k in p_json:
                        p_sc = (k['scrape_url'])
                        p_k = (k['key'])
                        p_get = requests.get(p_sc)
                        xcheck = re.match(f'{xreg}', p_get.text)
                        print(xcheck, xreg, p_k)                   
                        if  xcheck is not None :
                                logging.info(f'Regex Rule:{xnam} Matched! - {pastebin}{p_k}')
                                with open(f'{xnam}-{p_k}.txt', 'w') as pasta:
                                        p_out = pasta.write(f'{p_get.text}')
                        elif xcheck is None :
                                print(xnam, xreg, 'no match')
                                continue
             
                                         
        logging.info('Loop Completed!')
        time.sleep(wait)

while restart:
        try:
                pasta()
        except Exception as e:
                logging.error(traceback.format_exc())
                restart=True
