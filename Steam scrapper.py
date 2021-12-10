import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import re
tab_titles=[]
tab_prices=[]
tab_discounts=[]
tab_reviews=[]
tab_links=[]
tab_scores=[]
def scrap(page):


    #HTML
    for each in page:
        url = 'https://store.steampowered.com/search/?filter=weeklongdeals&page='+str(each+1)+'&category1=998'
        response = requests.get(url)
    
        #Parse

        soup = BeautifulSoup(response.text, 'html.parser')

        #Scrap
        
        games = soup.findAll('div', attrs={'class': 'col search_name ellipsis'})
        org_prices = soup.findAll('div', attrs= {'class': 'col search_price discounted responsive_secondrow'})
        discounts = soup.findAll('div', attrs={'class': 'col search_discount responsive_secondrow'})
        reviews = soup.findAll('div', attrs={'class': 'col search_reviewscore responsive_secondrow'})
        links = soup.findAll('a', attrs={'class': 'search_result_row ds_collapse_flag '})
        if len(links) == 0:
            links = soup.findAll('a', attrs={'class': 'search_result_row ds_collapse_flag  app_impression_tracked'})
        if len(links) == 0:
            links = soup.findAll('a', attrs={'class': 'search_result_row ds_collapse_flag'})
        if len(links) == 0:
            soup.findAll('a', attrs={'class': 'search_result_row ds_collapse_flag app_impression_tracked '})
        links_2 = []
        i = 0
        for each in games:
            #i = games.index(each)
            title = each.find('span', {'class': 'title'})
            price = org_prices[i].find('strike').text.replace('$','').replace('ARS ', '').replace(',','.')
            if price.count('.') > 1:
                price = float(price.replace('.','', 1))
            else:
                price = float(price)
            try:
                discount = float(discounts[i].find('span').text.replace('-','').replace('%', ''))/100
            except AttributeError:
                discount = 0
            review = reviews[i].find('span')['data-tooltip-html']
            score = re.search('\w+ \D*', review.replace('<br>',' '))
            positive_reviews = re.search('\d+', review)
            # pat = re.compile('\d*(,|\.)?\d*(,|\.)?\d+')
            # total_reviews = pat.search(review, 18)
            for x in links:
                links_2.append(links[links.index(x)].get('href'))
            tab_titles.append(title.text)
            tab_prices.append(round(price*(1-discount), 2))
            tab_discounts.append(discount)
            tab_scores.append(score.group())
            tab_reviews.append(positive_reviews.group()+'%')
            tab_links.append('=HYPERLINK("%s", "%s")'%(str(links_2[i]),str(links_2[i])) )
            i+=1
    tabbed_data = {
            'Títulos': tab_titles,
            'Precios':tab_prices,
            'Descuento':tab_discounts,
            'Puntaje':tab_scores ,
            'Reviews Positivas':tab_reviews ,
            'Link': tab_links }
    
    #Time and xls
    date = time.localtime()
    name = 'Steam discounts ' + str(date.tm_mday)+'-'+str(date.tm_mon)+' .xlsx'
    xls = pd.DataFrame(tabbed_data)
    xls.to_excel(name)
      

scrap(range(5))

