from lxml import html
import csv, os, json
import requests
from exceptions import ValueError
from time import sleep


def flush(data):
    f = open('bigbasket_result.json', 'w')
    json.dump(data, f, indent=4)
    return "json prepared---bigbasket_result.json"


def bigbasketreader(url):
    try:
        page = requests.get(url)

        doc = html.fromstring(page.content)
        totalrice_items = "//div[@class='uiv2-shopping-list-wrapper']/descendant::h2[@class='tabsEx']//text()"
        totalrice_items = doc.xpath(totalrice_items)[1]
        delivery_time = "//div[@class='uiv2-shopping-list-wrapper']/descendant::div[@id='products-container']/descendant::div[@class='uiv2-shopping-lis-sku-cards']//label[@class='delivery-slot-label ']//text()"
        product_price = "//div[@class='uiv2-shopping-list-wrapper']/descendant::div[@id='products-container']/descendant::div[@class='uiv2-shopping-lis-sku-cards']//div[@class='uiv2-rate-count-avial']//input[@type='hidden']/@value"
        product_name_pouchs = "//div[@class='uiv2-shopping-list-wrapper']/descendant::div[@id='products-container']/descendant::div[@class='uiv2-shopping-lis-sku-cards']//div[@class='uiv2-list-box-img-block']//a/@title"
        discount = "//div[@class='uiv2-shopping-list-wrapper']/descendant::div[@id='products-container']/descendant::div[@class='uiv2-shopping-lis-sku-cards']//li//div[@class='uiv2-combo-block']//span[2]//text()"
        brand_product= "//div[@class='uiv2-shopping-list-wrapper']/descendant::div[@id='products-container']/descendant::div[@class='uiv2-shopping-lis-sku-cards']//div[@class='uiv2-list-box-img-title']//span[2]//a[1]//text()"
        delivery_time = doc.xpath(delivery_time)
        product_price = doc.xpath(product_price)
        product_name_pouchs = doc.xpath(product_name_pouchs)
        brand_product = doc.xpath(brand_product)
        discount = doc.xpath(discount)

        for idx, i in enumerate(delivery_time):
            delivery_time[idx] = i.strip()

        dimension=[]
        for i in product_name_pouchs:
            dimension.append(" ".join(i.split(' ')[-3:]))

        brand = brand_product[0::2]
        product = brand_product[1::2]

        for idx,item in enumerate(product):
            product[idx]=item.strip()

        brands_list = []
        for i in range(len(zip(brand, zip(brand, product, dimension, delivery_time, product_price)))):
            brands_list.append(zip(brand, zip(brand, product, dimension, delivery_time, product_price))[i][0])

        master = {}
        for i in set(brands_list):
            master.update({i: []})

        for brand_details in zip(brand, zip(brand,product, dimension, delivery_time, product_price)):
            master[brand_details[0]].append(brand_details[1])

        for i in set(brands_list):
            if (len(master[i]) > 0):
                temp = []
                for details in master[i]:
                    temp.append({"title": details[0],"product_name": details[1], "size": details[2], "delivery": details[3], "price": details[4]})
                master[i] = []
                master[i]= temp

        return master,totalrice_items

    except Exception as e:
        print"exception"




def fetch():
    print"***********start**************"
    result = {}

    coimbatore = "https://www.bigbasket.com/skip_explore/?c=12&l=0&s=0&n=/ps/?q=rice"
    chennai = "https://www.bigbasket.com/skip_explore/?c=6&l=0&s=0&n=/ps/?q=rice"

    com_dict,totalrice_items = bigbasketreader(coimbatore)
    result.update({"coimbatore":com_dict,"total_rice_products_coimbatore":totalrice_items})
    sleep(5)
    com_dict, totalrice_items = bigbasketreader(chennai)
    result.update({"chennai": com_dict, "total_rice_products_chennai": totalrice_items})
    sleep(5)
    print"end  ",flush(result)


if __name__ == "__main__":
    fetch()
    #fetch_delivery()
