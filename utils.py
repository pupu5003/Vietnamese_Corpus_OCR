from html import unescape
from bs4 import BeautifulSoup
from zenrows import ZenRowsClient
from curl_cffi import curl
import time

import os

def fetchDocument(url, documentName):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }

    header_list = [f'{key}: {value}'.encode('utf-8') for key, value in headers.items()]
    
    status_code = 403
    
    while (status_code != 200):

        responseBody = []
        handle = curl.Curl()

        def writeCallback(data):
            responseBody.append(data)
            return len(data)

        try:
            handle.setopt(curl.CurlOpt.URL, url)

            handle.setopt(curl.CurlOpt.HTTPHEADER, header_list)

            handle.setopt(curl.CurlOpt.WRITEFUNCTION, writeCallback)

            handle.perform()

            status_code = handle.getinfo(curl.CurlInfo.RESPONSE_CODE)
            
            if status_code == 200:
                document = b''.join(responseBody).decode('utf-8')
                document = unescape(document)
                with open(f'{documentName}.html', 'w', encoding='utf-8') as file: 
                    file.write(document)
                return document
                
            else:
                print(f"Failed to fetch the document. Status code: {status_code}")
                if (status_code == 302): time.sleep(60)
                

        finally:
            handle.close()
            

        