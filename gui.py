#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################################################
#                                                                                    #
#                          DEVELOPED BY RAPHAEL MARQUES                              #
#                           Copyright (C) 2010 / 2011                                #
#                          See LICENCE for more details                              #
#                                                                                    #
######################################################################################
 
import sys, os, tempfile
from Manage import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *

######################################################################################

def main():
    app = QApplication(sys.argv)
    gui = Interface()
    if gui.valid:
        gui.show()
        res = app.exec_()
        sys.exit(res)
    else: 
        sys.exit(1)

######################################################################################

class Interface(QMainWindow):

######################################################################################

    def error(self, msg):
        QMessageBox.critical(self, "Error", "<center><b><font color = red>An error has occured.</font></b><br/><br/>%s</center>" % str(msg), QMessageBox.StandardButton(QMessageBox.Ok))

######################################################################################

    def good(self, msg):
        QMessageBox.information(self, "Success", "<center><b><font color = lightgreen>Operation completed.</font></b><br/><br/>%s</center>" % str(msg), QMessageBox.StandardButton(QMessageBox.Ok))

######################################################################################

    @pyqtSlot()
    def _help(self):
        os.system("chromium-browser ~/PassManager/.datas/help.html")

######################################################################################

    @pyqtSlot()
    def _update_master_pwd(self):
        pwd = QInputDialog.getText(self, "Change password", "Type your current password :", QLineEdit.Password)
        if str(pwd) != "(PyQt4.QtCore.QString(u''), False)":
            if self.control.check_pwd(str(pwd)): 
                pwd = QInputDialog.getText(self, "New password", "Type your NEW password :", QLineEdit.Password)
                if str(pwd) != "(PyQt4.QtCore.QString(u''), False)":
                    pwd2 = QInputDialog.getText(self, "New password", "RETYPE your NEW password :", QLineEdit.Password)
                    if str(pwd2) != "(PyQt4.QtCore.QString(u''), False)":
                        if str(pwd) == str(pwd2):
                            if self.control.update_pwd(str(pwd)): self.good("Password successfully changed !")
                        else: self.error("Password diverged. Try again ...")
            else: self.error("Please verify your password, then try again ...")

######################################################################################

    @pyqtSlot(QModelIndex)
    def choice(self, index):
        index = index.sibling(index.row(), 4)
        selectedID = index.data(Qt.DisplayRole)
        self.ID = selectedID.toString()

        test = QDialog()
        
        valid = QPushButton("Update")
        reject = QPushButton("Delete")
        
        layout = QGridLayout()
        layout.addWidget(valid, 0, 0)
        layout.addWidget(reject, 0, 1)

        self.connect(valid, SIGNAL('clicked()'), self, SLOT('modif_pwd()'))
        self.connect(valid, SIGNAL('clicked()'), test, SLOT('close()'))
        self.connect(reject, SIGNAL('clicked()'), self, SLOT('del_pwd()'))
        self.connect(reject, SIGNAL('clicked()'), test, SLOT('close()'))
        
        test.setLayout(layout)
        test.setWindowTitle("Choose")
        test.exec_()

######################################################################################

    @pyqtSlot()
    def modif_pwd(self):
        try:
            res = self.control.get_pwd_by_id(str(self.ID))
            if res == None: raise Exception, "No password match, maybe database is corrupted ..."
            else:
                test = QDialog()

                self.place = QLineEdit(res[1])
                self.pseudo = QLineEdit(res[2])
                self.mail = QLineEdit(res[3])
                self.pwd = QLineEdit((res[4].decode("hex")).decode("base64"))

                #self.control.del_pwd_by_id(str(self.ID))

                lplace = QLabel("Place : ")
                lpseudo = QLabel("Pseudo : ")
                lpwd = QLabel("Password : ")
                lmail = QLabel("E-mail : ")
        
                valid = QPushButton("Update")
                reject = QPushButton("Cancel")
        
                layout = QGridLayout()
                layout.addWidget(lplace, 0, 0)
                layout.addWidget(self.place, 0, 1)
                layout.addWidget(lpseudo, 1, 0)
                layout.addWidget(self.pseudo, 1, 1)
                layout.addWidget(lmail, 2, 0)
                layout.addWidget(self.mail, 2, 1)
                layout.addWidget(lpwd, 3, 0)
                layout.addWidget(self.pwd, 3, 1)
                layout.addWidget(valid, 4, 0)
                layout.addWidget(reject, 4, 1)

                self.connect(valid, SIGNAL('clicked()'), self, SLOT('datapwd()'))
                self.connect(valid, SIGNAL('clicked()'), test, SLOT('close()'))
                self.connect(reject, SIGNAL('clicked()'), test, SLOT('close()'))
        
                test.setLayout(layout)
                test.setWindowTitle("Update Password")
                test.exec_()

        except Exception as e: self.error(e)
                

######################################################################################

    @pyqtSlot()
    def del_pwd(self):
        try:
            self.control.del_pwd_by_id(str(self.ID))
        except Exception as e: self.error(e)
        else: self.update_pwd_list()

######################################################################################

    @pyqtSlot()
    def _add_pwd(self):
        test = QDialog()

        self.place = QLineEdit()
        self.pseudo = QLineEdit()
        self.mail = QLineEdit()
        self.pwd = QLineEdit()

        lplace = QLabel("Place : ")
        lpseudo = QLabel("Pseudo : ")
        lpwd = QLabel("Password : ")
        lmail = QLabel("E-mail : ")
        
        valid = QPushButton("Add")
        reject = QPushButton("Cancel")
        
        layout = QGridLayout()
        layout.addWidget(lplace, 0, 0)
        layout.addWidget(self.place, 0, 1)
        layout.addWidget(lpseudo, 1, 0)
        layout.addWidget(self.pseudo, 1, 1)
        layout.addWidget(lmail, 2, 0)
        layout.addWidget(self.mail, 2, 1)
        layout.addWidget(lpwd, 3, 0)
        layout.addWidget(self.pwd, 3, 1)
        layout.addWidget(valid, 4, 0)
        layout.addWidget(reject, 4, 1)

        self.connect(valid, SIGNAL('clicked()'), self, SLOT('datapwd()'))
        self.connect(valid, SIGNAL('clicked()'), test, SLOT('close()'))
        self.connect(reject, SIGNAL('clicked()'), test, SLOT('close()'))
        
        test.setLayout(layout)
        test.setWindowTitle("Add Password")
        test.exec_()

######################################################################################

    @pyqtSlot()
    def datapwd(self):
        try:
            if self.pwd.text() == "": raise Exception, "No password typed.<br/>Only Place, Pseudo and E-mail are optionals !"
            elif self.control.isExisting(str(self.ID)): self.control.update_click(str(self.ID), self.place.text(), self.pseudo.text(), self.mail.text(), self.pwd.text())
            else: self.control.add_pwd(self.place.text(), self.pseudo.text(), self.mail.text(), self.pwd.text())
        except Exception as e: self.error(e)
        else: self.update_pwd_list()

######################################################################################

    @pyqtSlot()
    def about(self):
        QMessageBox.about(self, "About PassManager", "<center>PassManager is a password manager written in Python with PyQt by<br/>Rapha&euml;l MARQUES.<br/><br/>Copyright (c) 2010 / 2011. See LICENCE for details.</center>")

######################################################################################

    def update_pwd_list(self):
        self.view.clear()
        res = self.control.list_db()
        if res != []:
            for i in res: 
                item = QTreeWidgetItem(self.view, 1000)
                item.setText(0, "%s" % i[1])
                item.setText(1, "%s" % i[2])
                item.setText(2, "%s" % i[3])
                item.setText(3, "%s" % (i[4].decode("hex")).decode("base64"))
                item.setText(4, "%s" % i[0])
                self.view.addTopLevelItem(item)

#####################################################################################

    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        pwd = QInputDialog.getText(self, "Password", "Type your password :", QLineEdit.Password)
        if str(pwd) == "(PyQt4.QtCore.QString(u''), False)":
            self.valid = False
        else:
            try:
                self.control = Manage(str(pwd))
                self.valid = True
                
                img_src = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAKfSURBVHjaYvz//z8DJQAggFhgDDaz2ccVJHgt3rz8cu/9+z9FDGKCGxnYeRkY/rMxMLBzMTDwANlMnAwMzNwMDNxcDP9n84P1AQQQE8wA9v8MBqV5Vgyz+9yVlFRFNjB8+DWV4e8/MQZG/C4ACCC4Af+APnn3n4lB20qWYU6/J0NYoHoW089/exn+/vfDZwBAAMEN+MHA+u7I8VcM+6/+Y3jwn5shM8OUoavCREdChGstw+//k4A2cGIzACCAGGGByGi5xJLhF/MEFV05Myt3PQY+IV4GI2kGBsH/3xlmrnnKsOv010v/2LmyGTh5jjDwAMNgFiQMAAIIYYDNMiDBwcvwg6mSW0IoV8lAhYdLQpJBV4aRwVvzH8OFax8YJq/7/OHdF5aZDMI8jcBA/A7SBxBAaAawQzAnrxEDM/t0bjERMxYxeQZeblaGRFsGBlX+3wwzdnxlOHaX6cT/eXyWIH0AAQSPRgYxDWBIMkAx4ydeLsbv7CzMDB9//Gf4+JuBYdYRBgZPbWag2RwMTKwM8PAACCAWtDDhZvj9L0dCgqvUQFtM+M53YYZvXxgZlET/M/z5+Yth2a4/P379YJrHwM1cBdMAEEAIA/7/12D8zzBdUUXQQVJRhuHcO3aG70DfSQn+ZXj36hfD2w9/7/77z5zHwMa4HaQapg0ggJBcwLRdQEZM4Y+YJMPpZ0wMPBwMDHysvxiePP7J8OMX82IGFpY8oPc+gL2IBAACCG4AIxuHxDdmAYbvX5kYBDj/Mvz58Z3h2cu/9/4zsjQysDAuwpWQAAIIbsB/FnYGJiYmBm7GXwyf3n4H2sqwjIGZuR4odQdfSgQIIHhKZGRmv/X3+3eG92+/vgRqjmVgYY4G5oM7DAQyK0AAMVKanQECDADMwNCYef7LugAAAABJRU5ErkJggg==".decode('base64')
                
                self.logo = QPixmap()
                self.logo.loadFromData(QByteArray(img_src))
                
                self.tmp = tempfile.NamedTemporaryFile()
                self.tmp_logo = self.tmp.name
                self.tmp.write(img_src)
                self.tmp.flush()
                
                self.setContentsMargins(0, 0, 0, 0)
                
                self.fileMenu = self.menuBar().addMenu("&File")
                
                self.quit = self.fileMenu.addAction("Quit")
                self.quit.setIcon(QIcon(self.logo))
                self.connect(self.quit, SIGNAL('triggered()'), qApp, SLOT('quit()'))
                
                self.cmdMenu = self.menuBar().addMenu("&Commands")
                
                self.addpwd_ = self.cmdMenu.addAction("Add password")
                self.addpwd_.setIcon(QIcon(self.logo))
                self.connect(self.addpwd_, SIGNAL('triggered()'), self, SLOT('_add_pwd()'))

                self.cmdMenu.addSeparator()

                self.changepwd_ = self.cmdMenu.addAction("Change master password")
                self.changepwd_.setIcon(QIcon(self.logo))
                self.connect(self.changepwd_, SIGNAL('triggered()'), self, SLOT('_update_master_pwd()'))

                self.help_ = self.cmdMenu.addAction("Help")
                self.help_.setIcon(QIcon(self.logo))
                self.connect(self.help_, SIGNAL('triggered()'), self, SLOT('_help()'))
                
                self.aboutMenu = self.menuBar().addMenu("&?")
                
                self.about_ = self.aboutMenu.addAction("About PassManager")
                self.about_.setIcon(QIcon(self.logo))
                self.connect(self.about_, SIGNAL('triggered()'), self, SLOT('about()'))
                 
                self.view = QTreeWidget(self)
                self.view.setAlternatingRowColors(True);
                self.view.setHeaderLabels(QStringList() << "Place" << "Pseudo" << "E-mail" << "Password" << "ID");
                self.connect(self.view, SIGNAL('doubleClicked(QModelIndex)'), self, SLOT('choice(QModelIndex)'))

                self.update_pwd_list()

                self.setCentralWidget(self.view)
                self.resize(700, 400)
                self.setWindowTitle("PassManager")
                self.setWindowIcon(QIcon(self.logo))
                
            except Exception as e:
                self.error(e)
                self.valid = False

######################################################################################
                
if __name__ == "__main__":    
    main()
