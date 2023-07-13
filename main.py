import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from anaTasarim import Ui_MainWindow
import requests
import json

class Window(QtWidgets.QMainWindow):
    def __init__(self, apiKey):
        super(Window, self).__init__()
        
        self.apiKey = apiKey
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
        items = ['TRY', 'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'SEK', 'KRW', 'NOK', 'NZD', 'INR', 'MXN', 'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CDF', 'CLP', 'CNY', 'COP', 'CRC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'FJD', 'FKP', 'FOK', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'KES', 'KGS', 'KHR', 'KID', 'KMF', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NPR', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD', 'SSP', 'STN', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TTD', 'TVD', 'TWD', 'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW', 'ZWL']
        
        self.ui.cbBozdur.addItems(items)
        self.ui.cbAl.addItems(items)
        
        self.ui.cbBozdur.currentIndexChanged[str].connect(self.Hesap)
        self.ui.cbAl.currentIndexChanged[str].connect(self.Hesap)
        self.ui.sbBozdur.textChanged.connect(self.Hesap)
        
        self.ui.btnOnay.clicked.connect(self.Onay)
    
    
    def Hesap(self, text):
        if (self.ui.cbBozdur.currentText() == "Bozdurmak İstediğiniz Döviz Türünü Seçin" or self.ui.cbAl.currentText() == "Satın Almak İstediğiniz Döviz Türünü Seçiniz"):
            self.ui.lblAl.setText("0")
        #elif self.ui.sbBozdur.text() == "":
        #    self.ui.lblAl.setText("0")    
        else:
            apiUrl = "https://v6.exchangerate-api.com/v6/" + self.apiKey + "/latest/" + self.ui.cbBozdur.currentText()
            apiJson = requests.get(apiUrl)
            apiJson = json.loads(apiJson.text)
            
            miktar = self.ui.sbBozdur.value()
            top_para = miktar * apiJson["conversion_rates"][self.ui.cbAl.currentText()]
            
            self.ui.lblAl.setText(str(top_para))
    
    
    def Onay(self):
        msg = QMessageBox()
        
        msg.setWindowTitle("İşlem Onayı")
        msg.setText("İşleminizi Onaylıyor musunuz?")
        
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Ok)
        
        msg.setDetailedText(f"{self.ui.sbBozdur.value()} {self.ui.cbBozdur.currentText()} karşılığında {self.ui.lblAl.text()} {self.ui.cbAl.currentText()} hesabınıza eklenecektir.")
        
        x = msg.exec_()
        
        print(x)
            
        
def app(apiKey):
    apiKey = apiKey
    app = QtWidgets.QApplication(sys.argv)
    win = Window(apiKey)
    win.show()
    sys.exit(app.exec_())


def main():
    apiKey = str(input("'https://www.exchangerate-api.com' sitesi için API anahtarınızı giriniz: "))
    app(apiKey) 
    


main()