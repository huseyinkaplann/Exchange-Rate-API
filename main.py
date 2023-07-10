import sys
from PyQt5 import QtWidgets
from anaTasarim import Ui_MainWindow
import requests
import json

class Window(QtWidgets.QMainWindow):
    def __init__(self, apiKey):
        super(Window, self).__init__()
        
        self.apiKey = apiKey
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
        items = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLP', 'CNY', 'COP', 'CRC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'FOK', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KID', 'KMF', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD', 'SSP', 'STN', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TVD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW', 'ZWL']
        
        self.ui.cbBozdur.addItems(items)
        self.ui.cbAl.addItems(items)
        
        self.ui.cbBozdur.currentIndexChanged[str].connect(self.Hesap)
        self.ui.cbAl.currentIndexChanged[str].connect(self.Hesap)
        self.ui.sbBozdur.textChanged.connect(self.Hesap)
    
    
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