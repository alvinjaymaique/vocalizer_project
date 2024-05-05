import sys, os, shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QToolButton, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import QStringListModel, QFileInfo, QSize, QDir
from resources_rc import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Vocalizer.ui", self)
        self.TV_Button.clicked.connect(self.open_tv_button_dialog)
        self.CV_Button.clicked.connect(self.open_cv_button_dialog)
        self.cv_files = []
        self.cv_model = QStringListModel()
        self.CV_List.setModel(self.cv_model)
        self.Tenor_List_2.hide()
        self.Soprano_List_2.hide()
        self.Bass_List_2.hide()
        self.Alto_List_2.hide()

        #Load
        self.load_files()


        # Connect button toggled signal to adjust button positions
        self.isPause = True
        self.Tenor_Bttn.toggled.connect(self.adjust_button_positions)
        self.Soprano_Bttn.toggled.connect(self.adjust_button_positions)
        self.Bass_Bttn.toggled.connect(self.adjust_button_positions)
        self.Alto_Bttn.toggled.connect(self.adjust_button_positions)

        # Set up Pause_Start_B button
        self.Pause_Start_B = self.findChild(QToolButton, "Pause_Start_B")
        self.Pause_Start_B.setIcon(QIcon("Raw_Image/Pause_bttn.png"))  # Set the path to the pause icon ("C:/Users/User/Documents/SF_&_AI/VOCA/Raw_Image/Pause_bttn.png")
        self.Pause_Start_B.setIconSize(QtCore.QSize(64, 64))  # Adjust the size as needed
        self.Pause_Start_B.clicked.connect(self.pause_start_action)  # Connect the clicked signal to the action

    def open_tv_button_dialog(self):
        self.openFileDialog("TV")

    def open_cv_button_dialog(self):
        self.openFileDialog("CV")

    def load_files(self):
        directory = QDir('cv_audio')
        file_list = directory.entryList()
        file_list = [file for file in file_list if file not in ['.','..']]
        for file_name in file_list:
            self.cv_files.append(file_name)
        self.cv_model.setStringList(self.cv_files)

    def openFileDialog(self, button_type):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Music files (*.mp3 *.wav *.ogg)")
        file_dialog.setDefaultSuffix("mp3")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setViewMode(QFileDialog.List)
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        if file_dialog.exec_():
            # Copy file to a specific folder
            destination_folder = "cv_audio"  # Change this to your desired destination folder
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            file_path = file_dialog.selectedFiles()[-1]
            print(f"Selected {button_type} file:", file_path)
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(destination_folder, file_name)

            if not os.path.exists(destination_path):
                shutil.copy(file_path, destination_path)
                if button_type == "CV":
                    self.cv_files.append(file_name)
                    self.cv_model.setStringList(self.cv_files)
                if file_path:
                    file_info = QFileInfo(file_path)
                    file_name = file_info.fileName()  # Extract filename from file path
                    # self.cv_model.setStringList([file_name])
                # QMessageBox.information(self, 'Success', 'File successfully copied')
            else:
                QMessageBox.critical(self, 'Error', f'The {file_name} file already exists')
        # After file dialog closes, adjust button positions
        self.adjust_button_positions()
        
    def showEvent(self, event):
        super().showEvent(event)
        # Adjust button positions when the window is shown
        self.adjust_button_positions()

    def adjust_button_positions(self):
        # Find all the QPushButtons within the SideBar
        buttons = self.SideBar.findChildren(QPushButton)
        
        # Calculate the center position of the SideBar widget
        sidebar_center = self.SideBar.rect().center()
        for button in buttons:
            # Adjust the button position to be centered horizontally within the SideBar
            button_rect = button.rect()
            button_center = button_rect.center()
            button.move(sidebar_center.x() - button_center.x(), button.y() + 1)  # Adjust vertical position

    def pause_start_action(self):
        # Toggle between Pause and Play icons
        if self.Pause_Start_B.icon().isNull() or self.Pause_Start_B.icon().name() == "C:/Users/User/Documents/SF_&_AI/VOCA/Raw_Image/Pause_bttn.png":
            self.Pause_Start_B.setIcon(QIcon("C:/Users/User/Documents/SF_&_AI/VOCA/Raw_Image/Play_bttn.png")) 
        else:
            self.Pause_Start_B.setIcon(QIcon("C:/Users/User/Documents/SF_&_AI/VOCA/Raw_Image/Pause_bttn.png")) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
