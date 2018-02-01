from lxml import html
import csv, os, json
import requests
from time import sleep


def flush(data,str_title):
    f = open(str_title+'_shopclues_result.json', 'w')
    json.dump(data, f, indent=4)
    return "json prepared---"+str_title+"_shopclues_result.json"

def shopcluesreader(url):
    try:
        page = requests.get(url)
        doc = html.fromstring(page.content)
        present_price = "//div[@class='column col3']/descendant::span[@class='p_price']//text()"
        old_prices = "//div[@class='column col3']/descendant::span[@class='old_prices']//text()"
        emi_details = "//div[@class='column col3']/descendant::div[@class='sh_content']/descendant::div[@class='emi']/descendant::span[2]//text()"
        title = "//div[@class='column col3']//descendant::h3//text()"
        discount = "//div[@class='column col3']/descendant::div[@class='ori_price']/descendant::span//text()"
        url = "//div[@class='column col3']//a[2]/@href"
        thumbnail = "//div[@class='column col3']/descendant::div[@class='img_section']//img/@src"

        product_title = doc.xpath(title)
        present_price = doc.xpath(present_price)
        emi_details = doc.xpath(emi_details)
        discount = doc.xpath(discount)
        url = doc.xpath(url)
        thumbnail = doc.xpath(thumbnail)

        # ----clean discount-----
        for i, m in enumerate(discount):
            if "off" in m.lower():
                discount[i - 1] = discount[i - 1] + ":" + discount.pop(i)

        product_details = zip(discount, emi_details, present_price, url, thumbnail)
        json_data = dict(zip(product_title, product_details))

        for i in json_data:
            temp = {}
            try:
                price = json_data[i][2]
                url = json_data[i][3]
                thumbnail = json_data[i][4]
                emi = json_data[i][1]
                discount = json_data[i][0].split(":")[1]
                temp.update({"price": price, "url": url, "thumbnail": thumbnail, "emi": emi, "discount": discount})
                json_data[i] = temp
            except Exception:
                price = json_data[i][2]
                url = json_data[i][3]
                thumbnail = json_data[i][4]
                emi = json_data[i][1]
                discount = "No discount"
                temp.update({"price": price, "url": url, "thumbnail": thumbnail, "emi": emi, "discount": discount})
                json_data[i] = temp

        print"\nextracted data-1", json_data
        return json_data
    except Exception as e:
        print"exception"


def shopclues_product_delivery(url, pincode):
    try:

        page = requests.get(url)
        doc = html.fromstring(page.content)

        p_id = doc.xpath("//span[@class='pID']//text()")
        p_id = p_id[0].split(":")[1].strip()

        description = doc.xpath("//div[@class='shd_box']/descendant::div[@class='des_info']/descendant::li//text()")
        description = " ".join(str(x) for x in description)
        product_name = doc.xpath("//div[@class='shd_box']/descendant::h1//text()")[0].strip()
        delivery_url = 'http://www.shopclues.com/ajaxCall/getDeliveryDetails?itemId=' + p_id + '&pincode=' + pincode + '&user_segment=&user_id=&user_email=&price_tbp=4850&user_mobile='
        delivery_page = requests.get(delivery_url)
        delivery_dates = str(json.loads(delivery_page.content)['fdate']) + "-" + str(json.loads(delivery_page.content)['sdate'])
        payment_mode = str(json.loads(delivery_page.content)['pin_result_txt'])

        temp_json = {product_name: {"product_id": p_id, "product_name": product_name, "delivery_dates": delivery_dates,
                                    "description": description, "payment_mode_or_available_status": payment_mode}}
        return temp_json

    except Exception as e:
        print"exception,please check pincode/url"


def fetch():
    print"************fetch delivery with respect to each product*************"

    url = "http://www.shopclues.com/computers-monitors.html"
    print "Processing: " + url
    json = shopcluesreader(url)
    print"",flush(json,"products")
    sleep(5)


def fetch_delivery():
    extracted_data = {}
    print"\n************fetch delivery with respect to each product*************"

    urls = ['http://www.shopclues.com/acer-p166hql-15.6-inch-led-monitor-21.html', \
            'http://www.shopclues.com/yatharth-samsung-led-s22-monitar.html', \
            'http://www.shopclues.com/acer-p166hql-156-inch-led-backlit-lcd-monitor-5.html']

    pincodes = ['560056', '575001', '575001']

    for url, pincode in zip(urls, pincodes):
        print "Processing: " + url + "pincode: "+pincode
        extracted_data.update(shopclues_product_delivery(url, pincode))
    sleep(5)
    print"\nextracted_data-2", extracted_data
    print"",flush(extracted_data, "pincodes")


if __name__ == "__main__":
    fetch()
    fetch_delivery()
