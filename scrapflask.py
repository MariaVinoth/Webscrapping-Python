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

    for data in containers:
        tmp1 = data.findAll('tr')
        tmp2 = data.findAll('td',{'class':'amount'})
        tmp3 = data.findAll('td', {'class': 'amount-sum'})
    for data1 in tmp1:
        price.append(data1.attrs['price'])
        id.append(data1.attrs['id'])
    for data2 in tmp2:
        amount.append(data2.text)
    for data3 in tmp3:
        total.append(data3.text)

    browser.close()
    browser.quit()
    return jsonify({'id':id},{'price':price},{'amount':amount},{'total':total})


app = Flask(__name__)

@app.route('/')
def index():
    return get_data()



if __name__ == '__main__':
    app.run(debug=True)

