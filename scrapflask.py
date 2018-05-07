from bs4 import BeautifulSoup
import time
from selenium import webdriver
from flask import Flask,jsonify

def get_data():
    url = "https://cex.io/btc-usd"
    browser = webdriver.Chrome()

    browser.get(url)
    time.sleep(3)
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")

    containers = soup.findAll("tbody", {"id": "md-sell-tbody"})

    price = []
    id = []
    amount = []
    total = []

    start_price = 'price="'
    end_price = '" sty'
    start_id = 'id="md-sell-'
    end_id = '" price='
    start_amnt = 'icn-BTC"></i>'
    end_amnt = '''</td><td class="amount-sum">'''
    start_total = 'icn-USD"></i>'
    end_total = '</td></tr>'


    for data in containers:
        data1 = str(data)
        tmp1 = tmp2 = tmp3 = ''
        tmp1 = data1.split(start_price)
        for par in tmp1:
            if end_price in par:
                price.append(par.split(end_price)[0])
        tmp2 = data1.split(start_id)
        for par in tmp2:
            if end_id in par:
                id.append(par.split(end_id)[0])
        tmp3 = data1.split(start_amnt)
        for par in tmp3:
            if end_amnt in par:
                amount.append(par.split(end_amnt)[0])
        tmp4 = data1.split(start_total)
        for par in tmp4:
            if end_total in par:
                total.append(par.split(end_total)[0])

    browser.close()
    browser.quit()
    return jsonify({'id':id},{'price':price},{'amount':amount},{'total':total})


app = Flask(__name__)

@app.route('/')
def index():
    return get_data()



if __name__ == '__main__':
    app.run(debug=True)

