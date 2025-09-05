from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sqlite3
import random
import datetime
import pyautogui
import easygui
database=sqlite3.connect("rising.db")
cursor=database.cursor()

class school(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(school,self).__init__()
        uic.loadUi("design.ui",self)
        self.stackedWidget.setCurrentIndex(0)
        self.frame2.hide()
        self.frame_2.hide()
        self.B_SignUp.clicked.connect(self.RegistrationForm)
        self.B_SignIn.clicked.connect(self.ConnectionForm)
        self.Clear1.clicked.connect(self.ClearConnectionForm)
        self.Clear2.clicked.connect(self.ClearRegistrationForm)
        self.PBSignIn.clicked.connect(self.Login)
        self.SignUpPushButton.clicked.connect(self.CreateUsers)
        self.showMaximized() #in order to show entire screen
        self.GoTo.clicked.connect(self.student_infos_page)
        self.B_back.clicked.connect(self.back)
        self.B_back.hide()
        self.B_InsertStudent.clicked.connect(self.student_infos)
        self.B_Ref.clicked.connect(self.showData)
        self.B_search.clicked.connect(self.Search)
        self.Ledit_search.textChanged.connect(self.Search)
        self.SearchTraining.currentTextChanged.connect(self.Search_byTraining)
        self.SearchDate.dateChanged.connect(self.Search_byDate)
        ToDay=datetime.date.today()
        self.SearchDate.setDate(ToDay)
        self.showData()
        self.ImportImage.clicked.connect(self.open_image)
        self.ImagePath.hide()
        self.B_Del.clicked.connect(self.Delete_Student)
        self.B_Del.hide()


    def showDelButton(self):
        self.B_Del.show()


    def Delete_Student(self):
        try:
            x=pyautogui.confirm("are u sure..?")
            if x=="OK":
                row=self.tableWidget.currentRow()
                ID=self.tableWidget.item(row,0).text()
                cursor.execute(f"""delete from students where ID="{ID}" """)
                database.commit()
                self.showData()
                self.B_Del.hide()
        except Exception as error:
            pyautogui.alert(error)


    def TheSame(self):
        try:
            data=cursor.fetchall()
            self.tableWidget.setRowCount(0)
            for i,values in enumerate(data):
                self.tableWidget.insertRow(i)
                for j,value in enumerate(values):
                    self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(value))
        except Exception as error:
            print(error) 


    def Search_byDate(self):
        try:
            search=self.SearchDate.date().toString("yyyy-MM-dd")
            cursor.execute(f""" select * from students where creatdon ="{search}" """)
            self.TheSame()
        except Exception as error:
            print(error)



    def Search_byTraining(self):
        try:
            search=self.SearchTraining.currentText()
            cursor.execute(f""" select * from students where Training ="{search}" """)
            self.TheSame()
        except Exception as error:
            print(error)


    def Search(self):
        try:
            search=self.Ledit_search.text()
            cursor.execute(f""" select * from students where ID like "%{search}%" or
                                                             Name like "%{search}%" or
                                                             LastName like "%{search}%" or
                                                             PhoneNumber like "%{search}%" """)
            self.TheSame()
        except Exception as error:
            print(error)

    def showData(self):
        try:
            cursor.execute(""" select * from students""")
            self.TheSame()
        except Exception as error:
            print(error)


    def open_image(self):
        try:
            path=easygui.fileopenbox()
            image=QtGui.QPixmap(path)
            self.MyImage.setPixmap(image)
            self.ImagePath.setText(path)
        except Exception as error:
            print(error)


    def CreateUsers(self):
        try:
            ID=random.randrange(1000000000)
            UserName=self.LEUserName2.text()
            Email=self.LEEmail.text()
            Password=self.LEPwd2.text()
            RePassword=self.LERePwd.text()
            #create database
            cursor.execute("""create table if not exists users(id,UserName,Email,Password,RePassword)""")

            cursor.execute(f"""insert into users values("{ID}","{UserName}","{Email}","{Password}","{RePassword}")""")
        
            database.commit()

            #clear the LineEdit after the Registration
            self.LEUserName2.clear()
            self.LEEmail.clear()
            self.LEPwd2.clear()
            self.LERePwd.clear()
            
        except Exception as error:
            print("error number 01", error)
    
    def RegistrationForm(self):
        self.frame2.show()
        self.frame1.hide()
        
    def ConnectionForm(self):
        self.frame2.hide()
        self.frame1.show()
        
    def ClearRegistrationForm(self):
        #function of button clear
        self.LEUserName2.clear()
        self.LEEmail.clear()
        self.LEPwd2.clear()
        self.LERePwd.clear()

    def ClearConnectionForm(self):
        #function of button clear
        self.LEUserName1.clear()
        self.LEPwd1.clear()

    def back(self):
        self.stackedWidget.setCurrentIndex(1)
        self.B_back.hide()
        
    def student_infos_page(self):
        self.stackedWidget.setCurrentIndex(2)
        self.B_back.show()

    def student_infos(self):
        try:
            ID=random.randrange(1000000000)
            createdon=datetime.date.today()
            Name=self.Name.text()
            LastName=self.LastName.text()
            Email=self.Email.text()
            PhoneNumber=self.PhoneNumber.value()
            BirthDate=self.BirthDate.date().toString("yyyy-MM-dd")
            BirthPlace=self.BirthPlace.text()
            Training=self.Training.currentText()
            Groupe=self.Groupe.currentText()
            Note=self.Note.toPlainText()
            Image=self.ImagePath.text()
            if Name=="":
                self.Name.setStyleSheet("border: 2px solid red")
            elif LastName=="":
                self.LastName.setStyleSheet("border: 2px solid red")
            else:
                #create students table
                cursor.execute("""create table if not exists students(ID,Creatdon,Name,LastName,Email,PhoneNumber,BirthDate,BirthPlace,Training,Groupe,Note,Image)""")

                cursor.execute(f"""insert into students values("{ID}","{createdon}","{Name}","{LastName}","{Email}","{PhoneNumber}","{BirthDate}","{BirthPlace}","{Training}","{Groupe}","{Note}","{Image}")""")
        
                database.commit()

                pyautogui.alert("Success")
                self.stackedWidget.setCurrentIndex(1)
                self.Name.clear()
                self.LastName.clear()
                self.Email.clear()
                self.PhoneNumber.setValue(0)
                self.BirthDate.setDate(createdon)
                self.BirthPlace.clear()
                self.Training.setCurrentIndex(0)
                self.Groupe.setCurrentIndex(0)
                self.Note.clear()
                self.showData()
            
        except Exception as error:
            print(error)

    def Login(self):
        try:
            name=self.LEUserName1.text()
            password=self.LEPwd1.text()
            cursor.execute(f""" select * from users where UserName="{name}" and Password="{password}" """)
            data=cursor.fetchall()
            if data:
                self.stackedWidget.setCurrentIndex(1)
                #clear the LineEdit after the Connection
                self.LEUserName1.clear()
                self.LEPwd1.clear()
                self.LabelError.setText("")
                self.frame_2.show()
            else:
                self.LabelError.setText("Wrong Password")
                #clear the LineEdit after the Connection filed
                self.LEUserName1.clear()
                self.LEPwd1.clear()
        except Exception as error:
            print(error)

        



if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = school()
    window.show()
    sys.exit(app.exec_())
