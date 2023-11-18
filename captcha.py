import deathbycaptcha
import sys
import takess as ts
import time


def read_captcha():
    time.sleep(1)
    # img = sys.argv[1]
    # img='test.jpg'
    ts.take_ss()
    ts.crop_ss()
    # time.sleep(2)
    client = deathbycaptcha.HttpClient('AjayD', '38xLAgsiO{Xe')
    # client = deathbycaptcha.HttpClient('AjayD', '38xLAgsiO{Xe')

    balance = client.get_balance()
    captcha = client.decode(ts.captcha_name, 5)
    print(balance)
    # print('output:' + captcha["text"])
    return str(captcha['text'])

# d=read_captcha()
# print(d)