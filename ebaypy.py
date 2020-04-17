#Program by Hamza Benhammouda
#instagram for improvements: @hamza_benhammouda
#Run the script and enter the keyword when asked
#The ouput Excel file is geenrate in the same source code directory

#If you think this program helped you somehow
#You can donate --> https://www.paypal.me/HamzaBenhammouda
#Otherwise, feel free to enjoy. Good luck in your e-commerce carrer!

from time import sleep
import pandas as pd
import requests
from bs4 import BeautifulSoup







Titles=[]
Prices=[]
Shipping_costs=[] #
Countries=[]
Rates=[]
Sales_number=[]
Links=[]




def scrape(keyword,pagen):
    url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=dog&_sacat=0&LH_TitleDesc=0&_ipg=200&_pgn="+pagen
    page = requests.get(url)
    sleep(1)
    soup = BeautifulSoup(page.text, 'html.parser')
    products = soup.findAll("div", {"class": "s-item__wrapper clearfix"})
    
    if(len(products) == 0):
        return 0 

   
    
    for product in products:
        
        #Get product title
        title = product.find("h3")
        if(title != None):
             Titles.append(title.get_text())
        else:
              Titles.append("Unknown")
        
        #Get product price
        price = product.find("span", {"class": "s-item__price"})
        if(price != None):
            price = price.get_text()
            price = price.replace('$','')
            if(price == 'Tap item to see current priceSee price'):
                price = 'Not listed'
            Prices.append(price)
        else:
            Prices.append("Not listen")
        
        #Get seller's country
        country = country = product.find("span", {"class": "s-item__location s-item__itemLocation"})
        if(country != None):
             country = country.get_text().replace('From', '')
             Countries.append(country)
        else:
            
            Countries.append("Not listed")
       
        #Is the seller Top Rated ? YES or No
        rate=product.find("span", {"class": "s-item__etrs-text"})
        if(rate!=None):
            Rates.append("Yes")
        else:
            Rates.append("No")
            
        #The number of sales if listed
        sales=product.find("span", {"class": "BOLD NEGATIVE"})
        str = 'sold'
        if(sales!=None and (str in sales.get_text())):
            sales = sales.get_text().replace('sold', '')
            Sales_number.append(sales)
        else:
            Sales_number.append("Not listed")
            
        #Check shipping:
        shipping_cost = product.find("span", {"class": "s-item__shipping s-item__logisticsCost"})
        if(shipping_cost is None):
            if( product.find("span", {"class": "BOLD"}) != None):
                shipping_cost=product.find("span", {"class": "BOLD"}).get_text()
                Shipping_costs.append(shipping_cost)
                
                    
            else:
                Shipping_costs.append("Not listen")
                
        else:
            shipping_cost = shipping_cost.get_text().replace('shipping','')
            shipping_cost = shipping_cost.replace('$','')
            Shipping_costs.append(shipping_cost)
             
        
        
        #Get links:
        link = product.find("a", {"class": "s-item__link"}).get('href')
        Links.append(link)
    return 1
        
        
        
   


     
def Write():
    print("Writing to disk...")
    df = pd.DataFrame.from_dict({'Titles':Titles,'Prices':Prices,'Shipping costs':Shipping_costs,
                                 'Countries':Countries,'Top Rated':Rates,'Sales number':Sales_number,
                                 'Link':Links})
    df = df.reindex(columns=['Titles','Prices','Shipping costs','Countries','Top Rated','Sales number','Link'])
    df.to_excel(keyword+'.xlsx', header=True, index=False)
    
    


print("------------Ebay py---------------")
print("")

keyword = input('Input a keyword: ')
pagen=1  
                     
while(scrape(keyword,str(pagen))):
    print("Getting all products related to "+keyword+" from page "+str(pagen))
    pagen = pagen + 1
    
print("Found " + str(len(Titles)) + " products!")          
Write()
input("done, click Enter key to abort")


    
