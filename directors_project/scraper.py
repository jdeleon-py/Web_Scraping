# scraper
from bs4 import BeautifulSoup
import requests

class IMDB_Scraper:
    '''
    This class scrapes IMDB movies directed by a list of directors.
    The script is passed a director profile url, then grabs links to all the movies they directed.
    The links are iteratively requested and scraped, with the director profile as a via.

    For each movie, the title, release_date, runtime, age_rating, genre(s), and review_rating is 
    put into a list and written out to a csv file
    '''
    def __init__(self, dir_url, dir_index):
        '''
        The director profile url is requested from the internet as text.
        The web-scraping library BeautifulSoup then parses the requested text as the full HTML script.

        IMDB has different indices for the 'Director' category, where 'Producer' and 'Actor' are sometimes mentioned,
        thus each index specifically for the director category is manually input into the system.

        Some movies are in production, so the array of movie links from the director's profile
        are filtered out to where only movies made on or before 2019 are processed.
        All other instances of inconsistent data are filtered out in the try/except block.
        '''
        self.source = requests.get(dir_url).text
        self.soup = BeautifulSoup(self.source, 'lxml')
        
        self.links = []
        
        dir_works = [category for category in self.soup.find_all('div', class_ = 'filmo-category-section')][dir_index]
        dir_works_arr = [works for works in dir_works.find_all('div')]
        
        for element in dir_works_arr:
            try:
                date = element.find('span', class_ = 'year_column').text
                date = date.split('\xa0')[1].split('\n')[0].split('/')[0].split('-')[0]

                if not date: pass
                elif int(date) <= 2019: self.links.append('https://imdb.com' + element.find('a', href = True)['href'])
                else: pass

            except AttributeError: print(' --- Inconsistent data or movie not found here. Skipping... ---')
                
    
    def request_movie(self, movie_url):
        '''
        The source url is the director profile, thus it is placed in the __init__() function
        For each movie link the source processing produces, it is requested and scraped here.
        The source and soup attributes are updated accordingly

        The div tag with title_wrapper class has most of the data needed for this project.
        '''
        self.source = requests.get(movie_url).text
        self.soup = BeautifulSoup(self.source, 'lxml')
        self.info = self.soup.find('div', class_ = 'title_wrapper')
        
    
    def movie_title(self):
        '''
        The heading tag has the title with some extra text,
        so the tag is filtered so only the title as a string is output.
        If the info is missing, which is unlikely, 'N/A' will be output instead.
        '''
        try: return self.info.find('h1').text.split('\xa0')[0]
        except: return 'N/A'
    
    
    def release_date(self):
        '''
        The release date is processed here...
        If the info is missing, 'N/A' will be output instead.
        '''
        try: return self.info.find('div', class_ = 'subtext').text.strip().split('\n')[-1]
        except: return 'N/A'
    
    
    def runtime(self):
        '''
        The runtime is processed here...
        If the info is missing, 'N/A' will be output instead.
        '''
        try: return self.info.find('time').text.strip()
        except: return 'N/A'
        
   
    def age_rating(self):
        '''
        The age rating is processed here...
        The runtime may be processed as the age_rating, which is incorrect as is filtered out.
        If the info is missing, or the runtime is output as the age_rating,
        'N/A' will be output instead.
        '''
        try:
            age_rating = self.info.find('div', class_ = 'subtext').text.strip().split('\n')[0] 
            return 'N/A' if (age_rating == self.runtime()) else age_rating
        
        except: return 'N/A'
    
    
    def genre(self):
        '''
        The genre is processed here...
        If the info is missing, 'N/A' will be output instead.
        '''
        try: return [self.info.find('div', class_ = 'subtext').text.strip().split('|')[2]]
        except: return 'N/A'
    
    
    def score(self):
        '''
        The review rating is processed here...
        If the info is missing, 'N/A' will be output instead.
        '''
        try: return self.soup.find('div', class_ = 'ratingValue').text.strip()
        except: return 'N/A'
