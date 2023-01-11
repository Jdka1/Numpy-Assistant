'''
Chatbot for a question answering system with numpy
'''


import requests
from bs4 import BeautifulSoup
import time
import random


class Scraper:
    def __init__(self):
        self.BASE_URL = 'https://numpy.org/doc/stable/reference/'
        pass
    
    def pause(self):
        time.sleep(random.uniform(1,2))
    
    def get_function_urls(self):
        response = requests.get(self.BASE_URL + 'routines.html')
        soup = BeautifulSoup(response.content, 'html.parser')
        
        numpy_routines_html = soup.find_all('li', {'class': 'toctree-l1 current active has-children'})[0]
        numpy_routines_html = numpy_routines_html.find_all('li')
        numpy_routine_urls = [self.BASE_URL + li.find('a')['href'] for li in numpy_routines_html]

        numpy_functions_urls = []
        for url in numpy_routine_urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            numpy_functions = soup.find_all('li', {'class': 'toctree-l2 current active has-children'})[0]
            numpy_functions = numpy_functions.find('ul')
            numpy_functions = numpy_functions.find_all('li')
            numpy_functions_urls += [self.BASE_URL + func.find('a')['href'] for func in numpy_functions]
            
            break
            self.pause()
            
        print(numpy_functions_urls)
        
        
        
        
        
print('\n' * 100)
s = Scraper()
print(s.get_routine_urls())
