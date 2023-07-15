import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from anaTasarim import Ui_MainWindow
import requests
import json

class Window(QtWidgets.QMainWindow):
    def __init__(self, apiKey):
        super(Window, self).__init__()
        
        self.apiKey = apiKey
        self.mvctPara = {}
            
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
        self.items = ['TRY', 'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'SEK', 'KRW', 'NOK', 'NZD', 'INR', 'MXN', 'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CDF', 'CLP', 'CNY', 'COP', 'CRC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'FJD', 'FKP', 'FOK', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'KES', 'KGS', 'KHR', 'KID', 'KMF', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NPR', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD', 'SSP', 'STN', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TTD', 'TVD', 'TWD', 'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW', 'ZWL']
        
        self.ui.cbBozdur.addItems(self.items)
        self.ui.cbAl.addItems(self.items)
        
        self.anlikKur()
        
        self.ui.cbBozdur.currentIndexChanged[str].connect(self.Hesap)
        self.ui.cbAl.currentIndexChanged[str].connect(self.Hesap)
        self.ui.sbBozdur.textChanged.connect(self.Hesap)
        
        self.ui.btnOnay.clicked.connect(self.Onay)
        
        self.ui.btnParaEkle.clicked.connect(self.ParaEkleme)
    
    
    def Hesap(self, text):
        if (self.ui.cbBozdur.currentText() == "Bozdurmak İstediğiniz Döviz Türünü Seçin" or self.ui.cbAl.currentText() == "Satın Almak İstediğiniz Döviz Türünü Seçiniz"):
            self.ui.lblAl.setText("0")   
        else:
            apiUrl = "https://v6.exchangerate-api.com/v6/" + self.apiKey + "/latest/" + self.ui.cbBozdur.currentText()
            apiJson = requests.get(apiUrl)
            apiJson = json.loads(apiJson.text)
            
            miktar = self.ui.sbBozdur.value()
            top_para = miktar * apiJson["conversion_rates"][self.ui.cbAl.currentText()]
            
            self.ui.lblAl.setText(f"{top_para:.4f}")
    
    
    def Onay(self):
        if ((self.ui.cbBozdur.currentText() != "Bozdurmak İstediğiniz Döviz Türünü Seçin") and (self.ui.cbAl.currentText() != "Satın Almak İstediğiniz Döviz Türünü Seçiniz") and (self.ui.sbBozdur.value() != 0)):
            msg = QMessageBox()
            
            msg.setWindowTitle("İşlem Onayı")
            msg.setText("İşleminizi Onaylıyor musunuz?")
            
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Ok)
            
            msg.setDetailedText(f"{self.ui.sbBozdur.value()} {self.ui.cbBozdur.currentText()} karşılığında {self.ui.lblAl.text()} {self.ui.cbAl.currentText()} hesabınıza eklenecektir.")
            
            x = msg.exec_()
            
            if x == 1024:
                if self.ui.cbBozdur.currentText() in self.mvctPara.keys() and self.ui.sbBozdur.value() <= self.mvctPara[self.ui.cbBozdur.currentText()]:
                    self.mvctPara[self.ui.cbBozdur.currentText()] -= self.ui.sbBozdur.value()
                    
                    miktar = float(self.ui.lblAl.text())
                    
                    if self.ui.cbAl.currentText() in self.mvctPara.keys():
                        self.mvctPara[self.ui.cbAl.currentText()] += miktar
                    else:
                        self.mvctPara[self.ui.cbAl.currentText()] = miktar
                    
                    self.mevcutParaGüncel()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Hata")
                    msg.setInformativeText("İşlemi gerçekleştimek için mevcut paranız yetersizdir")
                    msg.setWindowTitle("Yetersiz Bakiye")
                    msg.exec_()
                        
    
    def anlikKur(self):
        kurlar = ["USD", "EUR", "GBP", "AUD", "CAD", "CHF", "DKK"]
        
        apiUrl = "https://v6.exchangerate-api.com/v6/" + self.apiKey + "/latest/" + "TRY"
        apiJson = requests.get(apiUrl)
        apiJson = json.loads(apiJson.text)
        
        items = self.ui.groupKurlar.findChildren(QtWidgets.QLabel)
        
        kurIndex = 0
        
        for index, item in enumerate(items):
            if index % 2 == 0:
                item.setText(f"1 {kurlar[kurIndex]}")
            else:
                item.setText(f"{(1 / (apiJson['conversion_rates'][kurlar[kurIndex]])):.4f} TRY")
                kurIndex += 1
                
    
    def ParaEkleme(self):
        x = 0
        
        miktar, ok = QInputDialog.getInt(self, "Para Ekleme", "Eklemek istediğiniz tutarı giriniz:\n(tek seferde en fazla 100.000 birim eklenebilir)", 0, 0, 100000, 1)
        
        if ok and miktar is not None:
            cins, ok = QInputDialog.getItem(self, "Para Ekleme", "Eklemek istediğiniz döviz cinsini seçiniz: ", self.items)
          
        if cins not in self.items:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Hata")
            msg.setInformativeText("Geçerli bir döviz türü seçmediniz")
            msg.setWindowTitle("Hatalı tür")
            msg.exec_()
            return
                 
        if ok and cins is not None:
            msg = QMessageBox()
        
            msg.setWindowTitle("İşlem Onayı")
            msg.setText("İşleminizi Onaylıyor musunuz?")
            
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Ok)
            
            msg.setDetailedText(f"Hesabınıza {miktar} {cins} eklenecektir.")
            
            x = msg.exec_()
        
        if x == 1024:
            if cins in self.mvctPara.keys():
                self.mvctPara[cins] += miktar
            else:
                self.mvctPara[cins] = miktar
                
            self.mevcutParaGüncel()
    
    
    def mevcutParaGüncel(self):
        removeKey = []
        for key in self.mvctPara.keys():
            if self.mvctPara[key] == 0:
                removeKey.append(key)
        
        for key in removeKey:
            self.mvctPara.pop(key)
        
        self.ui.listTopPara.clear()
        
        for cins, miktar in self.mvctPara.items():
            self.ui.listTopPara.addItem(f"{cins}: {miktar:.4f}")
        
        
def app(apiKey):
    app = QtWidgets.QApplication(sys.argv)
    win = Window(apiKey)
    win.show()
    sys.exit(app.exec_())


def main():
    apiKey = str(input("'https://www.exchangerate-api.com' sitesi için API anahtarınızı giriniz: "))
    app(apiKey) 
    
    
main()
