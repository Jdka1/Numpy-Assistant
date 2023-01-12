'''
Chatbot for a question answering system with numpy
'''


import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd


class Scraper:
    def __init__(self):
        self.BASE_URL = 'https://numpy.org/doc/stable/reference/'
        pass
    
    def pause(self):
        time.sleep(random.uniform(1,4))
    
    def get_function_urls(self):
        response = requests.get(self.BASE_URL + 'routines.html')
        soup = BeautifulSoup(response.content, 'html.parser')
        
        numpy_routines_html = soup.find_all('li', {'class': 'toctree-l1 current active has-children'})[0]
        numpy_routines_html = numpy_routines_html.find_all('li')
        numpy_routine_urls = [self.BASE_URL + li.find('a')['href'] for li in numpy_routines_html]

        numpy_functions_urls = []
        for url_index, url in enumerate(numpy_routine_urls):
            print(f'Gathering {url}')
            
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            try:
                numpy_functions = soup.find_all('li', {'class': 'toctree-l2 current active has-children'})[0]
            except IndexError:
                numpy_functions_urls += [url]
            else:
                numpy_functions = numpy_functions.find('ul')
                numpy_functions = numpy_functions.find_all('li')
                numpy_functions_urls += [self.BASE_URL + func.find('a')['href'] for func in numpy_functions]

            print(f'Completed {url_index + 1} / {len(numpy_routine_urls)}\n')
            self.pause()
            
        with open('numpy_functions_urls.txt', 'w') as f:
            f.write(''.join([elem + '\n' for elem in numpy_functions_urls]))

    def get_text_and_labels(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data = {
            'label': [soup.find('h1').text[:-1]],
            'text': [soup.find('dl').find('p').text],
            'example': [soup.find('pre')]
        }

        return data

        
        
        
        

        
print('\n' * 100)
s = Scraper()

with open('numpy_functions_urls.txt', 'r') as f:
    urls = f.read().splitlines()
    
data = pd.DataFrame(columns=['label', 'text', 'example'])

for i, url in enumerate(urls):
    try:
        text_and_labels = s.get_text_and_labels(url)
    except:
        continue
    else:
        text_and_labels_df = pd.DataFrame.from_dict(text_and_labels, orient='columns')
        data = pd.concat([data, text_and_labels_df])

        print(f'Completed {i + 1} / {len(urls)}')

        if i % 10 == 0:
            data.to_csv('data.csv', index=False)

            t = time.localtime()
            print(f'Wrote to file at {time.strftime("%H:%M:%S", t)}')

    s.pause()

