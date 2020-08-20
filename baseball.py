import requests

from bs4 import BeautifulSoup
import json

import requests

cookies = {
    '_ga': 'GA1.2.930351172.1597235144',
    '_gid': 'GA1.2.1155097111.1597235144',
    'ASP.NET_SessionId': '1pt30p025ilkpbkapvwzpl1q',
    'Cookie_Id': 'didtlahs652',
    '_gat': '1',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Whale/2.8.105.22 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.koreabaseball.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

from datetime import datetime

today = datetime.today()
now_date = str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2)


data = {
  'leId': '1',
  'srId': '0,1,3,4,5,7,8,9',
  'date': now_date
}



def return_score(game_data, is_home):
    kia_score = 0
    anemy_score = 0
    if is_home == True:
        kia_score = int(game_data['B_SCORE_CN'])
        anemy_score = int(game_data['T_SCORE_CN'])
    else:
        kia_score = int(game_data['T_SCORE_CN'])
        anemy_score = int(game_data['B_SCORE_CN'])
    return int(kia_score), int(anemy_score)




def get_score(list_game):
    kia_score = 0
    anemy_score = 0
    anemy_name = None
    for game in list_game:
        if game['AWAY_NM'] == 'KIA':
            kia_score, anemy_score = return_score(game, is_home=False)
            anemy_name = game['HOME_NM']
        elif game["HOME_NM"] == 'KIA':
            kia_score, anemy_score = return_score(game, is_home=True)
            anemy_name = game['AWAY_NM']
    return kia_score, anemy_score, anemy_name

import threading
import os


# from PyQt4 import QtCore, QtGui
# import sys, os
#
#
# class MyCustomWidget(QtGui.QWidget):
#
#     def __init__(self, parent=None):
#         super(MyCustomWidget, self).__init__(parent)
#         layout = QtGui.QVBoxLayout(self)
#
#         # Create a progress bar and a button and add them to the main layout
#         self.progressBar = QtGui.QProgressBar(self)
#         self.progressBar.setRange(0, 1)
#         layout.addWidget(self.progressBar)
#         button = QtGui.QPushButton("Start", self)
#         layout.addWidget(button)
#
#         button.clicked.connect(self.onStart)
#
#         self.myLongTask = TaskThread()
#         self.myLongTask.taskFinished.connect(self.onFinished)
#
#     def onStart(self):
#         self.progressBar.setRange(0, 0)
#         self.myLongTask.start()
#
#     def onFinished(self):
#         # Stop the pulsation
#         self.progressBar.setRange(0, 1)
#         self.progressBar.setValue(1)
#
#
# class TaskThread(QtCore.QThread):
#     taskFinished = QtCore.pyqtSignal()
#
#     def run(self):
#         print("hello world" * 100000)
#         self.taskFinished.emit()


# if __name__ == "__main__":
#     app = QtGui.QApplication(sys.argv)
#     window = MyCustomWidget()
#     window.resize(640, 480)
#     window.show()
#     sys.exit(app.exec_())

def request_game_data():
    response = requests.post('https://www.koreabaseball.com/ws/Main.asmx/GetKboGameList', headers=headers,
                             cookies=cookies, data=data)

    json_file = json.loads(response.text)
    return json_file['game']

import tkinter
from tkinter import messagebox
def roop_main(arg):
    list_game = request_game_data()
    kia_score, anemy_score, anemy_name = get_score(list_game)

    if kia_score > anemy_score:
        tkinter.messagebox.showerror("이기고", "이기고 이싸!\n볼꺼니말꺼니")
    elif kia_score > arg[0]:

        tkinter.messagebox.showwarning("점수 냈다", "점수냈다 볼래? !\n볼꺼니말꺼니")

        arg[0] = kia_score

    # os.system('cls')
    print(f"{anemy_name} = ", anemy_score)
    print("기아 = ", kia_score)


    threading.Timer(10, roop_main, [arg]).start()


if __name__ == '__main__':

    list_game = request_game_data()
    past_kia_score, _, _ = get_score(list_game)
    roop_main([past_kia_score])
