import requests 
from bs4 import BeautifulSoup 
    
def getdata(url): 
    r = requests.get(url) 
    return r.text

def get_food_image(food_name):
    htmldata = getdata("https://www.google.com/search?q=" + food_name + "&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj_--HXnKr7AhVUFFkFHTDfAI8Q_AUoAnoECAIQBA&biw=891&bih=922&dpr=1.1") 
    soup = BeautifulSoup(htmldata, 'html.parser') 
    item = soup.find_all('img')[1:2]
    return item[0]['src']

