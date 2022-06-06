#All the imported class which will be used in this application
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QFileDialog, QTableWidget
from PyQt5.QtGui import QPixmap
import base64
import sqlite3
import random
import string
from datetime import datetime
import time
from abc import ABC, abstractmethod


#Class WelcomeScreen inheriting from PyQt5.QtWidgets.QDialog.
class WelcomeScreen(QDialog):  

    def __init__(self):
        '''It is used to load the file welcomescreen.ui as well as calling the base class __init__ for display.'''
        super(WelcomeScreen, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\welcomescreen.ui",self)
        self.Login.clicked.connect(self.gotologinscreen)
        self.Signup.clicked.connect(self.gotocreate)

    def gotologinscreen(self):
        '''Functionality behind Login Button. It will stack the loaded screen (login.ui) on widget1'''
        admin_user = LoginScreen()
        widget1.addWidget(admin_user)
        widget1.setCurrentIndex(widget1.currentIndex()+1)

    def gotocreate(self):
        '''Functionality behind Signup Button. It will stack the loaded screen (signin.ui) on widget1'''
        create = CreateAccScreen()
        widget1.addWidget(create)
        widget1.setCurrentIndex(widget1.currentIndex()+1)


#Class LoginScreen inheriting from PyQt5.QtWidgets.QDialog. 
class LoginScreen(QDialog):

    def __init__(self):
        '''It is used to load the file login.ui as well as calling the base class __init__ for display. It will display 2 buttons.'''
        super(LoginScreen, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\login.ui",self)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Login1.clicked.connect(self.logging_in)
        self.Forget_password.clicked.connect(self.forget_password)

    def logging_in(self):
        '''Functionality behind Login Button. It will take username and password as input and will calculate datetime on runtime (for Shopping History class). 
        It will check if the conditions of login are met by checking it from ConfirmPassword database otherwise it will show error. 
        When the suitable conditions are met, it will save data into History Database and we will proceed to the Menu Screen.'''
        global user
        user = self.Username.text()
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")
        password = self.Password.text()
        if len(user) == 0 or len(password) == 0:
            error1 = First_Error()
            widget2.addWidget(error1)
            widget2.setCurrentIndex(widget2.currentIndex()+1)
            widget2.show()
        else:  
            conn = sqlite3.connect("D:\Python\Object-oriented Programming\CEP\Account.db")
            cur = conn.cursor()
            query = 'INSERT INTO History(Username, DateTime) VALUES(?,?)'
            cur.execute(query, (user, now))
            conn.commit()
            conn = sqlite3.connect("D:\Python\Object-oriented Programming\CEP\Account.db")
            cur = conn.cursor()
            query = 'SELECT * FROM ConfirmPassword where Username=? AND password=?'
            result = cur.execute(query, (user, password))
            result1 = result.fetchone()
            if result1:
                market = MenuScreen()
                widget1.setFixedHeight(500)
                widget1.setFixedWidth(500)
                widget1.addWidget(market)
                widget1.setCurrentIndex(widget1.currentIndex()+1)  
            else:
                error2 = Second_Error()
                widget2.addWidget(error2)
                widget2.setCurrentIndex(widget2.currentIndex()+1)
                widget2.show()

    def forget_password(self):
        '''Functionality behind Forget password button. It will take username and password as input. It will check the conditions otherwise generate error.
        If all the suitable conditions are met then it will call the instance of change_password. '''
        user1 = self.Username.text()
        password1 = self.Password.text()
        if len(user1) == 0 or len(password1) == 0:
            error1 = First_Error()
            widget2.addWidget(error1)
            widget2.setCurrentIndex(widget2.currentIndex()+1)
            widget2.show()
        else:
            forget = Change_Password(user1)
            widget2.addWidget(forget)
            widget2.setCurrentIndex(widget2.currentIndex()+1)
            widget2.show()


#Class Change_Password inheriting from PyQt5.QtWidgets.QDialog. 
class Change_Password(QDialog):

    def __init__(self, user1):
        '''It is used to load the file passnew.ui as well as calling the base class __init__ for display. A new random password will be generated
        for the user and it will replace the previous password in the ConfirmPassword Database.'''
        super(Change_Password, self).__init__()
        loadUi("D:\\Python\\Object-oriented Programming\\CEP\\passnew.ui",self)
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(8))
        self.new_pass.setText(password)
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        c.execute("UPDATE ConfirmPassword SET Password=? WHERE Username=?", (password, user1))
        conn1.commit()
        conn1.close()


#Class CreateAccScreen inheriting from PyQt5.QtWidgets.QDialog. 
class CreateAccScreen(QDialog):

    def __init__(self):
        '''It is used to load the file signin.ui as well as calling the base class __init__ for display. Here all the options are given that are essential for
        creating an account.'''
        super(CreateAccScreen, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\signin.ui",self)
        self.Create_Account.clicked.connect(self.create_account)
        self.Password1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Con_Pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Browse.clicked.connect(self.browse_image)

    def create_account(self):
        '''Functionality behind Create Account button. It will take name, email, gender, username, password, date of birth, profile picture as input. 
        It will check the conditions, if any of them are not true then error will be generated. If all the conditions are met then it will save all
        the info of the user in SignIn database.'''
        name = self.Name.text()
        email = self.Email.text()
        gender = self.Gender.text()
        user_name = self.Username1.text()
        pass_word = self.Password1.text()
        confirm_password = self.Con_Pass.text()
        dob = self.DOB.text()
        try:
            image = self.picture.encode()
            image = base64.b64encode(image)
        except:
            image = None
        if len(name) == 0 or len(email) == 0 or len(gender) == 0 or len(user_name) == 0 or len(pass_word) == 0 or len(confirm_password) == 0 or len(dob) == 0 or image == None:
            error1 = First_Error()
            widget2.addWidget(error1)
            widget2.setCurrentIndex(widget2.currentIndex()+1)
            widget2.show()
        else:
            if self.Robot.isChecked():
                if pass_word == confirm_password:
                    conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
                    c = conn1.cursor()
                    c.execute("INSERT INTO SignIn(Username, Password, Gender, DOB, Email, ConfirmPassword, Image) \
                           VALUES(?, ?, ?, ?, ?, ?, ?)", (user_name, pass_word, gender, dob, email, confirm_password, image))
                    conn1.commit()
                    conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
                    c = conn1.cursor()
                    c.execute("INSERT INTO ConfirmPassword(Username, Password) \
                           VALUES(?, ?)", (user_name, pass_word))
                    conn1.commit()
                    confirm = Confirmation_account()
                    widget2.addWidget(confirm)
                    widget2.setCurrentIndex(widget2.currentIndex()+1)
                    widget2.show()

                else:
                    error4 = Fourth_Error()
                    widget2.addWidget(error4)
                    widget2.setCurrentIndex(widget2.currentIndex()+1)
                    widget2.show()
            else:
                error3 = Third_Error()
                widget2.addWidget(error3)
                widget2.setCurrentIndex(widget2.currentIndex()+1)
                widget2.show()

    def browse_image(self):
        '''Functionality behind Browse Button. It will give the user the facility to browse the image for his/her profile picture. '''
        self.picture, path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
       'c:\\',"Image files (*.jpg *.png)")
        self.pixmap = QPixmap(self.picture)
        self.DP.setPixmap(self.pixmap)


#Class MenuScreen inheriting from PyQt5.QtWidgets.QDialog.
class MenuScreen(QDialog):
    def __init__(self):
        '''It is used to load the file menu.ui as well as calling the base class __init__ for display. It will display the menu as well as display
        the profile picture and name of user.'''
        super(MenuScreen, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\menu.ui", self)
        self.Cart.clicked.connect(self.shopping_cart)
        self.History.clicked.connect(self.shopping_history)
        self.Market.clicked.connect(self.market)
        self.Quit.clicked.connect(QApplication.instance().quit)
        conn2 = sqlite3.connect("D:\Python\Object-oriented Programming\CEP\Account.db")
        cur2 = conn2.cursor()
        query = 'SELECT Image FROM SignIn WHERE username =\''+user+"\'"
        result = cur2.execute(query)
        image = result.fetchone()[0]
        self.label_name.setText(user)
        image = base64.b64decode(image)
        image = image.decode('utf-8')
        self.DP2.setPixmap(QPixmap(image))
        self.DP2.setScaledContents(True)
    
    def market(self):
        '''It will load the Shopping Market for the user'''
        mart = Shopping_Market()
        widget2.addWidget(mart)
        widget2.setFixedHeight(900)
        widget2.setFixedWidth(1200)
        widget2.setCurrentIndex(widget2.currentIndex()+1)
        widget2.show()
    
    def shopping_cart(self):
        '''It will load the Shopping Cart for the user'''
        cart = Cart()
        widget2.addWidget(cart)
        widget2.setFixedHeight(701)
        widget2.setFixedWidth(1001)
        widget2.setCurrentIndex(widget2.currentIndex()+1)
        widget2.show()
    
    def shopping_history(self):
        '''It will load the Shopping History for the user'''
        history = Shopping_History()
        widget2.addWidget(history)
        widget2.setFixedHeight(701)
        widget2.setFixedWidth(1001)
        widget2.setCurrentIndex(widget2.currentIndex()+1)
        widget2.show()


#Class Shopping_Market inheriting from PyQt5.QtWidgets.QDialog.
class Shopping_Market(QDialog):

    def __init__(self):
        '''It is used to load the file market.ui as well as calling the base class __init__ for display. It will display all the products
        so that the user can buy them. Whenever the Market is opened, it will empty the shopping cart.'''
        super(Shopping_Market, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\market.ui", self)
        self.BuyNow1.clicked.connect(self.Adding_to_cart1)
        self.BuyNow2.clicked.connect(self.Adding_to_cart2)
        self.BuyNow3.clicked.connect(self.Adding_to_cart3)
        self.BuyNow4.clicked.connect(self.Adding_to_cart4)    
        self.BuyNow5.clicked.connect(self.Adding_to_cart5)
        self.BuyNow6.clicked.connect(self.Adding_to_cart6)
        self.BuyNow7.clicked.connect(self.Adding_to_cart7)
        self.BuyNow8.clicked.connect(self.Adding_to_cart8)
        self.BuyNow9.clicked.connect(self.Adding_to_cart9)
        self.BuyNow10.clicked.connect(self.Adding_to_cart10)
        self.Search.clicked.connect(self.Searching_item)
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        c.execute("DELETE FROM Cart")
        conn1.commit()
        conn1.close()
    
    def Searching_item(self):
        '''Functionality behind Search Bar. If the product is not found then the error message will be displayed.'''
        if self.searchbar.text() == "Basmati Rice" or self.searchbar.text() == "basmati rice" or self.searchbar.text() == "basmatirice" or self.searchbar.text() == "BasmatiRice":
            item = Basmati_Rice()
            widget4.addWidget(item)
            widget4.setFixedHeight(450)
            widget4.setFixedWidth(500)
            widget4.setCurrentIndex(widget4.currentIndex()+1)
            widget4.show()

        elif self.searchbar.text() == "Iphone 11" or self.searchbar.text() == "iphone" or self.searchbar.text() == "iphone11":
            item = Iphone_11()
            widget4.addWidget(item)
            widget4.setFixedHeight(450)
            widget4.setFixedWidth(500)
            widget4.setCurrentIndex(widget4.currentIndex()+1)
            widget4.show()
        
        elif self.searchbar.text() == "Shaving Kit" or self.searchbar.text() == "shaving kit" or self.searchbar.text() == "ShavingKit":
            item = Shaving_Kit()
            widget4.addWidget(item)
            widget4.setFixedHeight(450)
            widget4.setFixedWidth(500)
            widget4.setCurrentIndex(widget4.currentIndex()+1)
            widget4.show()
        
        elif self.searchbar.text() == "Mangoes Box" or self.searchbar.text() == "mango box" or self.searchbar.text() == "mangoes box":
            item = Mango_Box()
            widget4.addWidget(item)
            widget4.setFixedHeight(450)
            widget4.setFixedWidth(500)
            widget4.setCurrentIndex(widget4.currentIndex()+1)
            widget4.show()
        
        elif self.searchbar.text() == "Potato Chips" or self.searchbar.text() == "Chips" or self.searchbar.text() == "chips" or self.searchbar.text() == "potato chips":
            item = Potato_Chips()
            widget4.addWidget(item)
            widget4.setFixedHeight(450)
            widget4.setFixedWidth(500)
            widget4.setCurrentIndex(widget4.currentIndex()+1)
            widget4.show()

        elif self.searchbar.text() == "Cheese Slices" or self.searchbar.text() == "Cheese" or self.searchbar.text() == "cheese" or self.searchbar.text() == "cheese slices":
            item = Cheese_Slices()
            widget4.addWidget(item)
            widget4.setFixedHeight(450)
            widget4.setFixedWidth(500)
            widget4.setCurrentIndex(widget4.currentIndex()+1)
            widget4.show()
        
        elif self.searchbar.text() == "Rubiks Cube" or self.searchbar.text() == "rubiks cube" or self.searchbar.text() == "RubiksCube":
            item = Rubiks_Cube()
            widget4.addWidget(item)
            widget4.setFixedHeight(450)
            widget4.setFixedWidth(500)
            widget4.setCurrentIndex(widget4.currentIndex()+1)
            widget4.show()

        elif self.searchbar.text() == "Body Spray" or self.searchbar.text() == "body spray" or self.searchbar.text() == "AXE Body Spray":
            item = Rubiks_Cube()
            widget4.addWidget(item)
            widget4.setFixedHeight(450)
            widget4.setFixedWidth(500)
            widget4.setCurrentIndex(widget4.currentIndex()+1)
            widget4.show()
        
        elif self.searchbar.text() == "Chicken Nuggets" or self.searchbar.text() == "chicken nuggets" or self.searchbar.text() == "ChickenNuggets":
            item = Chicken_Nuggets()
            widget4.addWidget(item)
            widget4.setFixedHeight(450)
            widget4.setFixedWidth(500)
            widget4.setCurrentIndex(widget4.currentIndex()+1)
            widget4.show()

        elif self.searchbar.text() == "Towels" or self.searchbar.text() == "towels":
            item = Towels()
            widget4.addWidget(item)
            widget4.setFixedHeight(450)
            widget4.setFixedWidth(500)
            widget4.setCurrentIndex(widget4.currentIndex()+1)
            widget4.show()
        
        else:
            item = Fifth_Error()
            widget4.addWidget(item)
            widget4.setFixedHeight(450)
            widget4.setFixedWidth(500)
            widget4.setCurrentIndex(widget4.currentIndex()+1)
            widget4.show()

    def Adding_to_cart1(self):
        '''Functionality behind BuyNow1 Button. The product will be added to cart.'''
        item = "BasmatiRice"
        price = 250
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        c.execute("INSERT INTO Cart(Item, Price ) \
                    VALUES(?, ?)", (item, price))
        conn1.commit()
        quantity = AddToCart()
        widget3.addWidget(quantity)
        widget3.setCurrentIndex(widget3.currentIndex()+1)
        widget3.show()

    def Adding_to_cart2(self):
        '''Functionality behind BuyNow2 Button. The product will be added to cart.'''
        item = "IPhone11"
        price = 156300
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        c.execute("INSERT INTO Cart(Item, Price ) \
                    VALUES(?, ?)", (item, price))
        conn1.commit()
        quantity = AddToCart()
        widget3.addWidget(quantity)
        widget3.setCurrentIndex(widget3.currentIndex()+1)
        widget3.show()
    
    def Adding_to_cart3(self):
        '''Functionality behind BuyNow3 Button. The product will be added to cart.'''
        item = "ShavingKit"
        price = 6000
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        c.execute("INSERT INTO Cart(Item, Price ) \
                    VALUES(?, ?)", (item, price))
        conn1.commit()
        quantity = AddToCart()
        widget3.addWidget(quantity)
        widget3.setCurrentIndex(widget3.currentIndex()+1)
        widget3.show()
        
    def Adding_to_cart4(self):
        '''Functionality behind BuyNow4 Button. The product will be added to cart.'''
        item = "MangoBox"
        price = 800
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        c.execute("INSERT INTO Cart(Item, Price ) \
                    VALUES(?, ?)", (item, price))
        conn1.commit()
        quantity = AddToCart()
        widget3.addWidget(quantity)
        widget3.setCurrentIndex(widget3.currentIndex()+1)
        widget3.show()

    def Adding_to_cart5(self):
        '''Functionality behind BuyNow5 Button. The product will be added to cart.'''
        item = "PotatoChips"
        price = 100
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        c.execute("INSERT INTO Cart(Item, Price ) \
                    VALUES(?, ?)", (item, price))
        conn1.commit()
        quantity = AddToCart()
        widget3.addWidget(quantity)
        widget3.setCurrentIndex(widget3.currentIndex()+1)
        widget3.show()
    
    def Adding_to_cart6(self):
        '''Functionality behind BuyNow6 Button. The product will be added to cart.'''
        item = "CheeseSlices"
        price = 250
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        c.execute("INSERT INTO Cart(Item, Price ) \
                    VALUES(?, ?)", (item, price))
        conn1.commit()
        quantity = AddToCart()
        widget3.addWidget(quantity)
        widget3.setCurrentIndex(widget3.currentIndex()+1)
        widget3.show()
    
    def Adding_to_cart7(self):
        '''Functionality behind BuyNow7 Button. The product will be added to cart.'''
        item = "RubickCube"
        price = 200
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        c.execute("INSERT INTO Cart(Item, Price ) \
                    VALUES(?, ?)", (item, price))
        conn1.commit()
        quantity = AddToCart()
        widget3.addWidget(quantity)
        widget3.setCurrentIndex(widget3.currentIndex()+1)
        widget3.show()
    
    def Adding_to_cart8(self):
        '''Functionality behind BuyNow8 Button. The product will be added to cart.'''
        item = "BodySpray"
        price = 450
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        c.execute("INSERT INTO Cart(Item, Price ) \
                    VALUES(?, ?)", (item, price))
        conn1.commit()
        quantity = AddToCart()
        widget3.addWidget(quantity)
        widget3.setCurrentIndex(widget3.currentIndex()+1)
        widget3.show()
    
    def Adding_to_cart9(self):
        '''Functionality behind BuyNow9 Button. The product will be added to cart.'''
        item = "ChickenNuggets"
        price = 800
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        c.execute("INSERT INTO Cart(Item, Price ) \
                    VALUES(?, ?)", (item, price))
        conn1.commit()
        quantity = AddToCart()
        widget3.addWidget(quantity)
        widget3.setCurrentIndex(widget3.currentIndex()+1)
        widget3.show()
    
    def Adding_to_cart10(self):
        '''Functionality behind BuyNow10 Button. The product will be added to cart.'''
        item = "Towels"
        price = 800
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        c.execute("INSERT INTO Cart(Item, Price ) \
                    VALUES(?, ?)", (item, price))
        conn1.commit()
        quantity = AddToCart()
        widget3.addWidget(quantity)
        widget3.setCurrentIndex(widget3.currentIndex()+1)
        widget3.show()




#Class Cart inheriting from PyQt5.QtWidgets.QDialog.
class Cart(QDialog):

    def __init__(self):
        '''It will load the cart.ui file and set the QtableWidget to display the cart info in table format. There are 3 buttons.'''
        super(Cart, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\cart.ui", self)
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(1,250)
        self.tableWidget.setHorizontalHeaderLabels(["Item", "Price"])
        self.load()
        self.Remove.clicked.connect(lambda:self.tableWidget.removeRow(self.tableWidget.currentRow()))
        self.Purchase.clicked.connect(self.purchase)
        self.Cost.clicked.connect(self.costing)

    def load(self):
        '''It will load the data from Cart Database and display it in QTableWidget.'''
        connection = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        cur = connection.cursor()
        sqlstr = 'SELECT * FROM Cart'
        tablerow=0
        results = cur.execute(sqlstr)
        results = results.fetchall()
        for row in results:
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            tablerow+=1
        connection.commit()
    
    def costing(self):
        '''Functionality behind Price Button. It will calculate the total cost of the products.'''
        self.price = []
        for i in range(self.tableWidget.rowCount()):
                thing = self.tableWidget.item(i,1)
                if thing != None and thing.text() != '':
                    self.price.append(int(thing.text()))
        self.cost = sum(self.price)
        self.costLabel.setText(str(self.cost))
    
    def purchase(self):
        '''Functionality behind Purchase Button. It will first collect items in a list and save it in History database then it will show confirmation box.'''
        self.collection_of_items = []
        for row in range(self.tableWidget.rowCount()):
                thing = self.tableWidget.item(row,0)
                if thing != None and thing.text() != '':
                    self.collection_of_items.append(thing.text())
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        self.items = repr(self.collection_of_items)
        print(self.items)
        c.execute("UPDATE History SET ItemsPurchased = ? WHERE Username = ?", [self.items, user])
        conn1.commit()
        conn1.close()
        pur = Items_Purchased()
        widget3.addWidget(pur)
        widget3.setCurrentIndex(widget3.currentIndex()+1)
        widget3.show()


#Class Shopping_History inheriting from PyQt5.QtWidgets.QDialog.
class Shopping_History(QDialog):

    def __init__(self):
        '''It will load the history.ui file and set the QtableWidget to display the history info in table format. There is 1 button.'''
        super(Shopping_History, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\history.ui", self)
        self.tableHistory.setColumnWidth(0,250)
        self.tableHistory.setColumnWidth(1,250)
        self.tableHistory.setColumnWidth(2,300)
        self.tableHistory.setHorizontalHeaderLabels(["Username", "Date/Time", "Items Purchased"])
        self.RemoveHistory.clicked.connect(self.clearHistory)
        self.load()
    
    def load(self):
        '''It will load the history from History Database into History table.'''
        connection = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        cur = connection.cursor()
        sqlstr = 'SELECT * FROM History'
        tablerow=0
        results = cur.execute(sqlstr)
        results = results.fetchall()
        for row in results:
            self.tableHistory.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableHistory.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableHistory.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            tablerow+=1
        connection.commit()
        connection.close()
    
    def clearHistory(self):
        '''It will clear the whole History table as well as History Database.'''
        conn1 = sqlite3.connect('D:\Python\Object-oriented Programming\CEP\Account.db')
        c = conn1.cursor()
        c.execute("DELETE FROM History")
        conn1.commit()
        conn1.close()
        self.tableHistory.clear()
        self.tableHistory.setHorizontalHeaderLabels(["Username", "Date/Time", "Items Purchased"])


#All Confirmations Classes that are inheriting from PyQt5.QtWidgets.QDialog.
#******************************************************************************************************************************
class Confirmation_account(QDialog):
    def __init__(self):
        super(Confirmation_account, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\confirmation.ui",self)

class AddToCart(QDialog):
    def __init__(self):
        super(AddToCart, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\AddToCart.ui", self) 

class Items_Purchased(QDialog):
    def __init__(self):
        super(Items_Purchased, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\purchase.ui", self)
#****************************************************************************************************************************** 


#All Errors Classes that are inheriting from PyQt5.QtWidgets.QDialog.
#******************************************************************************************************************************
class First_Error(QDialog):
    def __init__(self):
        super(First_Error, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\error1.ui",self)

class Second_Error(QDialog):
    def __init__(self):
        super(Second_Error, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\error2.ui",self)

class Third_Error(QDialog):
    def __init__(self):
        super(Third_Error, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\error3.ui",self)

class Fourth_Error(QDialog):
    def __init__(self):
        super(Fourth_Error, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\error4.ui",self)

class Fifth_Error(QDialog):
    def __init__(self):
        super(Fifth_Error, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\error5.ui", self) 
#******************************************************************************************************************************


#All Products Classes that are inheriting from PyQt5.QtWidgets.QDialog. They are used during searching.
#******************************************************************************************************************************
class Basmati_Rice(Shopping_Market, QDialog):
    def __init__(self):
        super(Basmati_Rice, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\basmatiRice.ui", self)
        self.BuyNow1.clicked.connect(Shopping_Market.Adding_to_cart1)

class Iphone_11(Shopping_Market, QDialog):
    def __init__(self):
        super(Iphone_11, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\Iphone11.ui", self)
        self.BuyNow2.clicked.connect(Shopping_Market.Adding_to_cart2)

class Shaving_Kit(Shopping_Market, QDialog):
    def __init__(self):
        super(Shaving_Kit, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\ShavingKit.ui", self)
        self.BuyNow3.clicked.connect(Shopping_Market.Adding_to_cart3)

class Mango_Box(Shopping_Market, QDialog):
    def __init__(self):
        super(Mango_Box, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\MangoBox.ui", self)
        self.BuyNow4.clicked.connect(Shopping_Market.Adding_to_cart4)

class Potato_Chips(Shopping_Market, QDialog):
    def __init__(self):
        super(Potato_Chips, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\PotatoChips.ui", self)
        self.BuyNow5.clicked.connect(Shopping_Market.Adding_to_cart5)

class Cheese_Slices(Shopping_Market, QDialog):
    def __init__(self):
        super(Cheese_Slices, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\CheeseSlices.ui", self)
        self.BuyNow6.clicked.connect(Shopping_Market.Adding_to_cart6)

class Rubiks_Cube(Shopping_Market, QDialog):
    def __init__(self):
        super(Rubiks_Cube, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\RubiksCube.ui", self)
        self.BuyNow7.clicked.connect(Shopping_Market.Adding_to_cart7)

class Body_Spray(Shopping_Market, QDialog):
    def __init__(self):
        super(Body_Spray, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\BodySpray.ui", self)
        self.BuyNow8.clicked.connect(Shopping_Market.Adding_to_cart8)

class Chicken_Nuggets(Shopping_Market, QDialog):
    def __init__(self):
        super(Chicken_Nuggets, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\ChickenNuggets.ui", self)
        self.BuyNow9.clicked.connect(Shopping_Market.Adding_to_cart9)

class Towels(Shopping_Market, QDialog):
    def __init__(self):
        super(Towels, self).__init__()
        loadUi("D:\Python\Object-oriented Programming\CEP\\Towels.ui", self)
        self.BuyNow10.clicked.connect(Shopping_Market.Adding_to_cart10) 
#******************************************************************************************************************************

#Starting time of the Program       
start = time.time()

#Making instance of Class QtWidget.QApplication
app = QApplication(sys.argv) 

#Making instance of Class WelcomeScreen
welcome = WelcomeScreen()   

#Widget1 is the instance of QtWidgets.QstackedWidget(). Its dimensions are also specified
widget1 = QtWidgets.QStackedWidget()                       
widget1.addWidget(welcome)
widget1.setFixedHeight(701)
widget1.setFixedWidth(1001)
widget1.show()

#Widget2 is the instance of QtWidgets.QstackedWidget(). Its dimensions are also specified
widget2 = QtWidgets.QStackedWidget()                       
widget2.setFixedHeight(200)
widget2.setFixedWidth(600)

#Widget3 is the instance of QtWidgets.QstackedWidget(). Its dimensions are also specified
widget3 = QtWidgets.QStackedWidget()                       
widget3.setFixedHeight(200)
widget3.setFixedWidth(600)

#Widget4 is the instance of QtWidgets.QstackedWidget(). Its dimensions are also specified
widget4 = QtWidgets.QStackedWidget()                       

#Try Except block is introduced. If the execution at any instant fails, the app will exit.
try:
    sys.exit(app.exec_())
except:
    print("Exiting")


#Ending time of the Program
end = time.time()

#An Abstract class is defined
class Time(ABC):
    @abstractmethod
    def load(self):
        pass
    
#Total time of execution of Program
class Time_of_execution(Time):
    def load(self, start, end):
        print('Total Time: ',end - start)
        
A = Time_of_execution()
A.load(start, end)





