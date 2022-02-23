import os
import sys
import threading
from random import randint
from threading import Timer
import psutil
import requests, socket
from PyQt5.QtWidgets import QApplication, QMainWindow
from flask import Flask, request, render_template, session, redirect, url_for

import time
import ui

app = Flask(__name__)
app.config['SECRET_KEY'] = 'renhaoyi000422###'

ico = '9999'
theme_num = 8
riliopen = 1
ver = "4.6"


def weather():
    global weather_sx
    weatherhq()
    wa = threading.Timer(900, weather)
    wa.start()


def weatherhq():
    cityCode = "101180901"
    hefengkey = '230ca71baf334fddb7be67c918f6aa5f'
    # 和风天气接口
    sxt = time.strftime('%H:%M:%S', time.localtime(time.time()))
    shuaxin = f"最近一次刷新时间：{sxt}"
    try:
        url = f'http://wthrcdn.etouch.cn/weather_mini?citykey={cityCode}'
        urlhf = f'https://devapi.qweather.com/v7/weather/now?key={hefengkey}&location={cityCode}'
        urlair = f'https://devapi.qweather.com/v7/air/now?key={hefengkey}&location={cityCode}'
        res = requests.get(url)
        hef = requests.get(urlhf)
        air = requests.get(urlair)
        res.encoding = 'utf-8'
        res_json = res.json()
        hef_json = hef.json()
        air_json = air.json()
        datahf = hef_json['now']
        dataair = air_json['now']
        data = res_json['data']
        global ico, run_code
        ico = datahf['icon']
        icos = f'''
            image: url(:/wico/{ico}.svg);
            background-image: url(:/theme{theme_num}/img/icon{theme_num}.png);
            '''
        # windir=datahf['windir']
        wtext = f"天气：{datahf['text']}"
        # humidity = datahf['humidity']
        # feelsLike = datahf['feelsLike']
        temp = f"实时温度：{datahf['temp']} 度"
        # city = f"城市：{data['city']}"
        zonghe = f"体感：{datahf['feelsLike']}度 湿度：{datahf['humidity']}%"
        # date = f"日期：{today['date']}"
        now = f"实时温度：{data['wendu']}度"
        # temperature = f"温度：{today['high']} {today['low']}"
        fengxiang = f"空气:{dataair['category']} {datahf['windDir']}"
        # today = data['forecast'][0]
        # typ = f"天气：{today['type']}"
        tips = f"贴士：{data['ganmao']}"
        result = temp + zonghe + now + fengxiang + wtext + tips
        print("天气刷新成功！")
        print(result)
        ui.sswd.setText(temp)
        ui.wd.setText(zonghe)
        ui.fx.setText(fengxiang)
        ui.tq.setText(wtext)
        ui.ts.setText(tips)
        ui.sx.setText(shuaxin)
        ui.icon.setStyleSheet(icos)
        run_code = "000"
    except:
        print("天气获取异常！")
        ui.sswd.setText('天气获取失败！')
        ui.wd.setText('请检查网络环境！')
        ui.fx.setText('')
        ui.tq.setText('NULL')
        ui.ts.setText('')
        ui.sx.setText(shuaxin)
        run_code = "200"


def ti():
    # 每秒获取一次时间
    t = time.strftime('%H:%M:%S', time.localtime(time.time()))
    d = time.strftime("%m/%d %a", time.localtime())
    ui.label.setText(t)
    ui.date.setText(d)
    x = threading.Timer(0.5, ti)
    x.start()


yiyanon = 1


def yiyan():
    global yiyanon
    if yiyanon == 1:
        yiyanhq()
        yy = threading.Timer(600, yiyan)
        yy.start()


def yiyanhq():
    yiyan_url = 'https://v1.hitokoto.cn/'
    try:
        yiyana = requests.get(yiyan_url)
        yiyana = yiyana.json()
        yiyant = yiyana['hitokoto']
        yiyanf = yiyana['from']
        yiyanf = f'——[{yiyanf}]'
        ui.db3.setText(yiyant)
        ui.yiyanfrom.setText(yiyanf)
        return yiyant
    except:
        print("一言获取失败！")


def time_initialization():
    print("加载时间组件...")
    ti()
    print("时间日期开始刷新，频率:0.5S")
    print("加载天气组件...")
    weather()
    print("天气开始刷新，频率：15mins")
    # tongbu()
    yiyan()


def zujian():
    global riliopen
    global yiyanon
    if riliopen == 1:
        ui.calendarWidget.setVisible(False)
        ui.db1.setVisible(True)
        ui.db2.setVisible(True)
        ui.db3.setVisible(True)
        ui.yiyanfrom.setVisible(True)
        riliopen = 0
        return '关闭'
    elif riliopen == 0:
        ui.calendarWidget.setVisible(True)
        ui.db1.setVisible(False)
        ui.db2.setVisible(False)
        ui.db3.setVisible(False)
        ui.yiyanfrom.setVisible(False)
        riliopen = 1
        return '打开'

theme=0
def randtheme():
    # 祖传代码，禁止乱动
    # 切换主题函数
    global theme_num,theme
    themerd = randint(0, theme_num)
    theme=themerd
    changetheme(themerd)


def changetheme(theme):
    # 祖传代码，禁止乱动
    # 切换主题函数
    global ico
    # pyqt5的sytlesheet
    # timebg = f'''
    # color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));
    # background-image: url(:/theme{theme}/img/time{theme}.png);'''
    # tmpbg = f'''
    # color: rgb(255, 255, 255);
    # background-image: url(:/theme{theme}/img/now{theme}.png);'''
    # shidubg = f'''
    # color: rgb(255, 255, 255);
    # background-image: url(:/theme{theme}/img/tmp{theme}.png);'''
    # fengxiangbg = f'''
    # color: rgb(255, 255, 255);
    # background-image: url(:/theme{theme}/img/fengxiang{theme}.png);'''
    # tianqibg = f'''
    # color: rgb(255, 255, 255);
    # background-image: url(:/theme{theme}/img/type{theme}.png);'''
    # ticonbg = f'''
    # image: url(:/wico/{ico}.svg);
    # background-image: url(:/theme{theme}/img/icon{theme}.png);'''
    # tipsbg = f'''
    # color: rgb(255, 255, 255);
    # background-image: url(:/theme{theme}/img/tips{theme}.png);'''
    # shuaxinbg = f'''
    # color: rgb(255, 255, 255);
    # background-image: url(:/theme{theme}/img/shuaxin{theme}.png);'''
    # rilibg = f'''
    # background-image: url(:/theme{theme}/img/rl{theme}.png);
    # '''
    # 更改MainWindows的stylesheet（不需要.ui）
    MainWindow.setStyleSheet(f"background-image: url(:/bg/img/bg{theme}.jpg);")
    # 更改ui的sytlesheet background-image: url(:/bg/img/bg0.jpg);
    # ui.label.setStyleSheet(timebg)
    # ui.sswd.setStyleSheet(tmpbg)
    # ui.wd.setStyleSheet(shidubg)
    # ui.fx.setStyleSheet(fengxiangbg)
    # ui.tq.setStyleSheet(tianqibg)
    # ui.ts.setStyleSheet(tipsbg)
    # ui.sx.setStyleSheet(shuaxinbg)
    # ui.icon.setStyleSheet(ticonbg)
    # ui.calendarWidget.setStyleSheet(rilibg)


def ex():
    # 退出程序
    app = QApplication.instance()
    app.quit()
    os.exit()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', title="No Found", error="404 No Found", shuoming="请求的目录没有找到", ver=ver), 404


@app.errorhandler(500)
def internal_Server_error(e):
    return render_template('error.html', title="Internal Server Error", error="500 Internal Server Error",
                           shuoming="服务器无法处理请求", ver=ver), 500


@app.errorhandler(400)
def bad_requests(e):
    return render_template('error.html', title="Bad Requests", error="400 Bad Requests", shuoming="请求出现错误",
                           ver=ver), 500


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('error.html', title="Method Not Allowed", error="405 Method Not Allowed", shuoming="不被允许的请求",
                           ver=ver), 500


run_status = ""
run_status_ch = " "
run_status_server = " "
run_status_weather = " "
run_status_time = " "
run_status_tongbu = " "
run_code = '000'


@app.route('/', methods=['GET', 'POST'])
def dashbroad(interval=1):  # put application's code here
    if 'password' in session:
        mem = psutil.virtual_memory()
        # 系统总计内存
        zj = float(mem.total) / 1024 / 1024 / 1024
        # 系统已经使用内存
        ysy = float(mem.used) / 1024 / 1024 / 1024
        # 格式化
        memq = '%.1fG/%.1fG' % (ysy, zj)
        # cpu信息
        cpuq = str(psutil.cpu_percent(interval)) + "%   " + str(psutil.cpu_count()) + "核心"
        # 磁盘信息
        diski = psutil.disk_partitions()
        disk_name_arr = diski[0].device.split(':')
        disk_name = disk_name_arr[0]
        disk_info = psutil.disk_usage(diski[0].device)
        # 磁盘剩余空间，单位G
        free_disk_size = disk_info.free // 1024 // 1024 // 1024
        # 当前磁盘使用率和剩余空间G信息
        hddq = "%s%%   可用：%iG\n" % (str(disk_info.percent), free_disk_size)

        global run_status, run_code, theme_num
        if run_code == '000':
            run_status = "success"
            run_status_ch = "正常"
            run_status_server = "正常"
            run_status_weather = "正常"
            run_status_time = "正常"
            run_status_tongbu = "正常"
        elif run_code == '200':
            run_status = "danger"
            run_status_ch = "天气同步失败！"
            run_status_server = "正常"
            run_status_weather = "失败"
            run_status_time = "正常"
            run_status_tongbu = "正常"

        return render_template('index.html',
                               theme="2", ver=ver, memq=memq, cpuq=cpuq, hddq=hddq, used=ysy, left=zj,
                               themebg=theme, run_status=run_status, run_status_server=run_status_server,
                               run_status_ch=run_status_ch, time=timecontrol(0), run_status_time=run_status_time,
                               run_status_weather=run_status_weather, run_status_tongbu=run_status_tongbu)
    else:
        return render_template('login.html', pwd=0)


def timecontrol(format):  # put application's code here
    if format == 0:
        return time.strftime("%Y-%m-%d %H:%M", time.localtime())
    elif format == 1:
        return time.strftime("%Y-%m-%d", time.localtime())
    else:
        return time.strftime("%H:%M:%S", time.localtime())


@app.route('/change/theme', methods=['GET'])
def theme_change_web():
    global theme_num,theme
    themen = randint(0, theme_num)
    theme=themen
    MainWindow.setStyleSheet(f"background-image: url(:/bg/img/bg{themen}.jpg);")
    r = str(themen)
    return r


@app.route('/change/weather', methods=['GET'])
def weather_change_web():
    weatherhq()
    return "成功"


@app.route('/change/rili', methods=['GET'])
def change_rili():  # put application's code here
    return zujian()


# 控制消息的三个函数
@app.route('/change/msg1', methods=['POST'])
def msg1():  # put application's code here
    ms1 = request.form['msg1']
    ui.db1.setText(ms1)
    return redirect(url_for('send'))


@app.route('/change/yiyan', methods=['GET'])
def yiyans():  # put application's code here\
    global yiyanon
    if yiyanon == 1:
        yiyanon = 0
        ui.yiyanfrom.setVisible(False)
        ui.db3.setText(' ')
        return '关闭'
    elif yiyanon == 0:
        yiyanon = 1
        yiyan()
        ui.yiyanfrom.setVisible(True)
        return '打开'


@app.route('/change/yiyan/refresh', methods=['GET'])
def yiyanr():  # put application's code here\
    global yiyanon
    yt = yiyanhq()
    return yt


@app.route('/change/msg2', methods=['POST'])
def msg2():  # put application's code here
    ms2 = request.form['msg2']
    ui.db2.setText(ms2)
    return redirect(url_for('send'))


@app.route('/change/msg3', methods=['POST'])
def msg3():  # put application's code here
    ms3 = request.form['msg3']
    ui.db3.setText(ms3)
    return redirect(url_for('send'))


@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    global ms
    pwd = request.form['pwd']
    global key
    if pwd == 'renhaoyi':
        session['password'] = pwd
        return redirect(url_for('dashbroad'))
        # return render_template('index.html',theme="2",ver=ver)
    else:
        return render_template('login.html', pwd=1)


@app.route('/clear_login', methods=['GET'])
def clear():  # put application's code here
    session.clear()
    return render_template('login.html', pwd=0)


@app.route('/send_msg', methods=['GET'])
def send():  # put application's code here
    return render_template('send_msg.html')


@app.route('/control', methods=['GET'])
def control():  # put application's code here
    return render_template('control.html')


@app.route('/setting', methods=['GET'])
def set():  # put application's code here
    return render_template('setting.html')


def Windows_initialization():
    ui.db1.setVisible(False)
    ui.db2.setVisible(False)
    ui.db3.setVisible(False)
    ui.yiyanfrom.setVisible(False)
    randtheme()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    k = {'host': '0.0.0.0', 'port': port, 'threaded': True, 'use_reloader': False, 'debug': False}
    threading.Thread(target=app.run, daemon=True, kwargs=k).start()
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = ui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    # MainWindow.show()
    MainWindow.showFullScreen()
    print('————————————————————————————')
    print(
        '╦╦╦╦╦╦▄▀▀▀▀▀▀▄╦╦╦╦╦╦\n▒▓▒▓▒█╗░░▐░░░╔█▒▓▒▓▒\n▒▓▒▓▒█║░░▐▄▄░║█▒▓▒▓▒\n▒▓▒▓▒█╝░░░░░░╚█▒▓▒▓▒\n╩╩╩╩╩╩▀▄▄▄▄▄▄▀╩╩╩╩╩╩')
    print(f"—————Pad-Panel V{ver}—————")
    print("Author:RHY 2022/2/18 compile")
    print('————————————————————————————')
    Windows_initialization()
    print("前端窗口加载完毕！")
    time_initialization()
    print("组件加载完成：当前有4个主题")
    info = '''
    ____            _     ____                      _ 
    |  _ \  __ _ ___| |__ | __ ) _ __ ___   __ _  __| |
    | | | |/ _` / __| '_ \|  _ \| '__/ _ \ / _` |/ _` |
    | |_| | (_| \__ \ | | | |_) | | | (_) | (_| | (_| |
    |____/ \__,_|___/_| |_|____/|_|  \___/ \__,_|\__,_|
    '''
    print(info)
    print("加载控制面板...")
    print("==================================================")
    hostname = socket.gethostname()
    bip = socket.gethostbyname(hostname)
    print(f"主机:{hostname}  程序启动完成！")
    print(f"地址：http://{bip}:80/")
    print("==================================================")
    # 定义按钮动作
    ui.pushButton.clicked.connect(zujian)
    ui.exit.clicked.connect(ex)
    ui.change.clicked.connect(randtheme)
    sys.exit(app.exec_())
