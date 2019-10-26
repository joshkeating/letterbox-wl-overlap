import math
from selenium import webdriver
from collections import defaultdict
from bs4 import BeautifulSoup as bs


def pull_url(url):

    STANDARD_PAGE_SIZE = 28

    browser = webdriver.Chrome()
    target_url = url
    browser.get(target_url)

    html = browser.execute_script("return document.body.innerHTML")
    page = bs(html, 'html.parser')

    num_films = page.find('h1', attrs={'class': 'section-heading'}).get_text()[-8:]
    total_count = int(num_films[0:2])

    page_count = math.ceil(total_count / STANDARD_PAGE_SIZE)

    movie_list = []

    for movie in page.find_all('span', attrs={'class': 'frame-title'}):
            movie_list.append(movie.get_text())

    if page_count > 1:

        for i in range(2, page_count+1):
            browser.get(url + '/page/' + str(i))
            html = browser.execute_script("return document.body.innerHTML")
            page = bs(html, 'html.parser')
            for movie in page.find_all('span', attrs={'class': 'frame-title'}):
                movie_list.append(movie.get_text())

        return movie_list
    else:
        return movie_list    


def process_friends(friend_list):

    movie_bag = []

    for name in friend_list:
        search_path = 'https://letterboxd.com/' + name + '/watchlist/'
        movie_bag.append(pull_url(search_path))    

    return movie_bag


def find_films_in_common(film_bag):

    film_dict = defaultdict(int)

    for wishlist in film_bag:
        for film in wishlist:
            film_dict[film] += 1

    desc_dict = sorted(film_dict.items() , key=lambda t : t[1] , reverse=True)
    
    output_file = open("movies-in-common.txt", "w")

    for k,v in desc_dict:
        output_file.write(k + ' ' + str(v) + '\n')

    output_file.close

    return


def main():

    FRIENDS = ['joshkeating', 'ekatnic', 'paquinn', 'cjp123']

    bag = process_friends(FRIENDS)
    find_films_in_common(bag)


if __name__ == "__main__":
    main()
