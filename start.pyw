from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
import json
import os
import webbrowser


def read_stat(stat):
    with open(os.path.join("files", "stats.json"), "r") as file:
        data = json.load(file)
        return data[stat]

def save_stat(stat, value):
    with open(os.path.join("files", "stats.json"), "r") as file:
        data = json.load(file)

    data[stat] = value

    with open(os.path.join("files", "stats.json"), "w") as file:
        json.dump(data, file, indent=4)

class ConfigMenu(QMainWindow):
    def __init__(self):
        super(ConfigMenu, self).__init__()
        uic.loadUi(os.path.join('files', 'config_menu.ui'), self)
        self.show()
        self.playButton.clicked.connect(self.play)
        self.repoLinkButton.clicked.connect(self.repoSee)
        self.issueLinkButton.clicked.connect(self.repoIssue)
        
    def play(self): # 1 - Easy | 2 - Medium | 3 = Hard | 4 - Very Hard | 5 - Extreme | 6 - Insane
        if self.diffBox.currentText() == "Easy":
            difficulty = 1
        elif self.diffBox.currentText() == "Medium":
            difficulty = 2
        elif self.diffBox.currentText() == "Hard":
            difficulty = 3
        elif self.diffBox.currentText() == "V. Hard":
            difficulty = 4
        elif self.diffBox.currentText() == "Extreme":
            difficulty = 5
        elif self.diffBox.currentText() == "Insane":
            difficulty = 6
        else:
            difficulty = 7

        one_shot = self.oneshotCheckBox.isChecked()

        save_stat("current_difficulty", difficulty)
        save_stat("one_shot_enabled", one_shot)

        print(f"Choosen difficulty: {self.diffBox.currentText()} ({difficulty})")
        print(f"One-shot: {one_shot}")

        self.close()

        os.startfile("game.pyw")
        
        exit()

    def repoSee(self):
        webbrowser.open("https://github.com/vDeresh/Circle_Game", 2, True)
    
    def repoIssue(self):
        webbrowser.open("https://github.com/vDeresh/Circle_Game/issues", 2, True)

def show_config_menu():
    APP = QApplication([])
    APP_WINDOW = ConfigMenu()
    APP.setWindowIcon(QtGui.QIcon(os.path.join('files', 'icon.png')))
    APP_WINDOW.setWindowIcon(QtGui.QIcon(os.path.join('files', 'icon.png')))
    APP.exec()

show_config_menu()