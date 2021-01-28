from bs4 import BeautifulSoup as bs
import requests
import re

"""get user input for search details"""


def getBasicRecipeInfo(url, recipe_quantity):
    # initialize while loop condition
    keep_going = True
    # initialize lists for links, titles, and images
    """grab recipe links and filter to requested amount""" 
    link_hrefs = []
    link_titles = []
    link_imgs = []
    link_descriptions = []
    # initialize page_num for url iteration
    page_num = 1

    """ while loop is used to get the user requested amount of recipes (recipeQuanity)
        The loop sends a new request to the url each iteration, and increases the page_num 
        in the url to fetch more links, as the website only loads a certain amount at a time.
        Then the for loops check to see if the desired amount of recipes have been gathered. 
        If so, the loops are exited and keep_going is set to False and the while loop is exited
    """
    while(keep_going):
        # convert page_num to string for url
        page_string = str(page_num)
        # send request to url
        res = requests.get(url + page_string)
        # make the soup
        soup = bs(res.text,"html.parser")
        # gather the recipe links, titles, and images for links
        links = soup.find_all("a", re.compile(r'.recipe.'))
        titles = soup.find_all("span", class_="fixed-recipe-card__title-link")
        imgs = soup.find_all("img", class_="fixed-recipe-card__img")
        descriptions = soup.find_all("div", class_="fixed-recipe-card__description")
        # append titles to link_titles
        for title in titles:
            if len(link_titles) >= recipe_quantity:
                keep_going = False
                break
            else:
                link_titles.append(title.string)
        # append links to link_hrefs
        for link in links:
            if len(link_hrefs) >= recipe_quantity:
                keep_going = False
                break
            else:
                link_hrefs.append(link.attrs['href'])
        # append image src links to link_imgs
        for img in imgs:
            link_imgs.append(img.attrs['data-original-src'])
        # append description snippet to 
        for description in descriptions:
            link_descriptions.append(description.text.strip())
        # increase page_num variable for url on next iteration
        page_num += 1

    # creat dictionary of with titles as keys and links as values
    recipe_links = {link_titles[i]: {
                                 'title': link_titles[i],
                                 'link':link_hrefs[i], 
                                 'image': link_imgs[i],
                                 'description':link_descriptions[i]
                                 }  for i in range(len(link_titles))}
    return recipe_links

def compileSearchUrl(keywords,sort_method):
    recipe_quantity = 100
    searchWords = keywords.split(" ")
    # set sortby to users choice of 1:Best Match,2:Newest or 3:Popular
    sorting_choices = {'1':'Best Match','2':'Newest','3':'Popular'}
    sortby = sorting_choices[sort_method]

    """compile url for scraper"""
    baseUrl = "https://www.allrecipes.com/search/results/?wt="
    # make string of user selected search terms
    url_search_terms = " ".join(searchWords)
    # user selected sort method for url
    url_sort_method = f'&sort={sortby}'
    # put full url together
    url = baseUrl + url_search_terms + url_sort_method + "&page="
    # call getBasicRecipeInfo to scrape recipe with given url info and return dictionary of links, images, titles
    links = getBasicRecipeInfo(url, recipe_quantity)
    return links

def getFullRecipes(recipe_links):
    """visit each link to scrape recipe data"""
    recipes = {}
    for title in recipe_links.keys():
        res = requests.get(recipe_links[title]['link'])
        soup = bs(res.text, 'html.parser')
        ingredients = soup.find_all('span', class_='ingredients-item-name')
        steps = soup.find_all('div', class_='paragraph')
        metaHeaders = soup.find_all('div', class_='recipe-meta-item-header')
        metaText = soup.find_all('div', class_='recipe-meta-item-body')
        nutrition = soup.find('div', class_="recipe-nutrition-section")

        recipes[title] = {}
        recipes[title]['ingredients'] = []
        recipes[title]['steps'] = []
        recipes[title]['meta'] = {}
        recipes[title]['nutrition'] = nutrition.contents[3].text.strip().split("\n")[0]

        for item in ingredients:
            recipes[title]['ingredients'].append(item.text.strip())
        
        for step in steps:
            recipes[title]['steps'].append(step.text.strip())

        recipes[title]['meta'] = {metaHeaders[i].text.strip().split(':')[0]: metaText[i].text.strip() for i in range(len(metaHeaders))}
    return recipes


# get ingredients list and store in array
# get recipe instructions
# get recipe image
# store recipe info into csv
if __name__ == "__main__":
    print("Main")

