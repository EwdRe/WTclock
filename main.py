import sys
import time
import threading
import requests
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow
import ui


def weather():
    cityCode = "101180901"
    url = f'http://wthrcdn.etouch.cn/weather_mini?citykey={cityCode}'
    res = requests.get(url)
    res.encoding = 'utf-8'
    res_json = res.json()
    data = res_json['data']
    city = f"城市：{data['city']}"
    today = data['forecast'][0]
    date = f"日期：{today['date']}"
    now = f"实时温度：{data['wendu']}度"
    temperature = f"温度：{today['high']} {today['low']}"
    fengxiang = f"风向：{today['fengxiang']}"
    typ = f"天气：{today['type']}"
    tips = f"贴士：{data['ganmao']}"
    result = city + date + now + temperature + fengxiang + typ + tips
    sxt = time.strftime('%H:%M:%S', time.localtime(time.time()))
    shuaxin = f"最近一次刷新时间：{sxt}"
    print("天气刷新成功！")
    print(result)
    ui.sswd.setText(now)
    ui.wd.setText(temperature)
    ui.fx.setText(fengxiang)
    ui.tq.setText(typ)
    ui.ts.setText(tips)
    ui.sx.setText(shuaxin)
    wa = threading.Timer(900.0, weather)
    wa.start()


def ti():
    t = time.strftime('%H:%M:%S', time.localtime(time.time()))
    ui.label.setText(t)
    x = threading.Timer(0.5, ti)
    x.start()


def button():
    print("开始运行时间及天气组件！")
    ti()
    print("时间开始刷新，频率:0.5S！")
    weather()


def ex():
    app = QApplication.instance()
    app.quit()
    os._exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = ui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    # MainWindow.show()
    MainWindow.showFullScreen()
    print("电子天气日历程序V1.5 By RHY")
    print("窗口加载完毕！")
    ui.pushButton.clicked.connect(button)
    ui.exit.clicked.connect(ex)
    sys.exit(app.exec_())
