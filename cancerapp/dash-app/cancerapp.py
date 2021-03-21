# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 20:11:14 2020

@author: Asus
"""

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QLineEdit
from PyQt5 import uic
from PyQt5.QtCore import QDate, Qt, QDateTime
import sys
import pandas as pd
import pickle
import datetime


class DiabetesApp(QMainWindow):
    def __init__(self):
        super(DiabetesApp, self).__init__()
        uic.loadUi("cancerapp.ui", self)
        self.submit.clicked.connect(self.form)
        self.clear.clicked.connect(self.clear_data)
        self.show()
        
    def form(self):
        #now = QDate.currentDate()
        now = QDateTime.currentDateTime()
        model_name = 'model_cancer.pkl'
        #self.model = pd.read_pickle(model_name)
        self.model = pickle.load(open(model_name, 'rb'))
        Name = self.name.text()
        Genre = self.genre.text()
        Age = int(self.age.text())
        mean_radius = float(self.radius.text())
        mean_texture = float(self.texture.text())
        mean_perimeter = float(self.perimeter.text())
        mean_area = float(self.area.text())
        mean_smoothness = float(self.smoothness.text())
                
        self.result = self.model.predict([[mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness]])
        if self.result == ["Normal"]:
            self.output.setText("Congratulations you normal.")
        elif self.result == ["Cancer"]:
            self.output.setText("You have cancer. Please consult a doctor.")
    
        output_data = {"Date": now.toString(Qt.ISODate), "Name": [Name], "Genre": [Genre], "Age": [Age], "Mean Radius":mean_radius, "Mean Texture": mean_texture, "Mean Perimeter": mean_perimeter, "Mean Area": mean_area, "Mean Smoothness": mean_smoothness, "Result": self.result}
        data = pd.DataFrame(output_data)
        data.to_csv("database.csv")
        with open("database.csv","a") as f:
            data.to_csv(f,header=False,index=False)       
    
    def clear_data(self):
       self.radius.clear()
       self.texture.clear()
       self.perimeter.clear()
       self.area.clear()
       self.smoothness.clear()
       self.name.clear()
       self.genre.clear()
       self.age.clear()       
       self.output.setText(" ") 
                       
 

app = QApplication(sys.argv)
window = DiabetesApp()
window.setWindowTitle("Diabetes Check")
window.showMaximized()
app.exec_()