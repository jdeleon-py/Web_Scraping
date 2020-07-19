import csv
import time
from scraper import IMDB_Scraper

if __name__ == '__main__':
    
    # tuples of the director information (profile url, index of directed movies, file to be written out to)
    scorsese = ('https://www.imdb.com/name/nm0000217/', 1, 'scorsese_movies.csv')
    spielberg = ('https://www.imdb.com/name/nm0000229/', 2, 'spielberg_movies.csv')
    kubrick = ('https://www.imdb.com/name/nm0000040/', 0, 'kubrick_movies.csv')
    nolan = ('https://www.imdb.com/name/nm0634240/', 2, 'nolan_movies.csv')
    tarantino = ('https://www.imdb.com/name/nm0000233/', 3, 'tarantino_movies.csv')

    dir_arr = [scorsese, spielberg, kubrick, nolan, tarantino]
    
    for director in dir_arr:
        while True:
            try:        
                scraper = IMDB_Scraper(dir_url = director[0], dir_index = director[1])
                break

            except:
                print('Connection Error! Trying again...')
                time.sleep(30)
                continue

        movie_links = scraper.links # has all movie links
        time.sleep(30)

        with open('/Users/jamesdeleon/Documents/Programs/Python_Programs/Scraping/Web_Scraping/directors_project/data_files/' + director[2], 'w') as file:
            writer = csv.writer(file) # write csv file
            writer.writerow(['Index', 'Movie Title', 'Release Date', 'Runtime', 'Age Rating', 'Genre(s)', 'Review Rating'])

            for movie in range(0, len(movie_links)):
                while True:
                    try: 
                        scraper.request_movie(movie_links[movie]) # request movie from the link accordingly
                        break
                    
                    except:
                        print('Connection Error! trying again...')
                        time.sleep(30)
                        continue

                # grab all the info
                title = scraper.movie_title()
                release_date = scraper.release_date()
                runtime = scraper.runtime()
                age_rating = scraper.age_rating()
                genre = scraper.genre()
                score = scraper.score()

                # write all the info to the file
                writer.writerow([movie, title, release_date, runtime, age_rating, genre, score])
                print([movie, title, release_date, runtime, age_rating, genre, score])
                time.sleep(30)

        print('\n')
