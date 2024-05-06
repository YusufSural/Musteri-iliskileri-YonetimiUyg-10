import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, \
    QMessageBox, QListWidget, QListWidgetItem, QDialog
from PyQt5.QtGui import QIcon
import re


class Kullanıcı:
    def __init__(self, name, contact_info):
        self.name = name
        self.contact_info = contact_info
        self.sales = []
        self.support_tickets = []

    def add_sale(self, sale_number, products):
        self.sales.append({"sale_number": sale_number, "products": products})

    def create_support_ticket(self, ticket_number, details):
        self.support_tickets.append({"ticket_number": ticket_number, "details": details})


class EditCustomerWindow(QDialog):
    def __init__(self, name, contact_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Müşteri Düzenle")
        self.name = name
        self.contact_info = contact_info
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label_customer_name = QLabel("Müşteri Adı Soyadı")
        layout.addWidget(self.label_customer_name)
        self.entry_customer_name = QLineEdit(self.name)
        layout.addWidget(self.entry_customer_name)

        self.label_contact_info = QLabel("İletişim Bilgisi (E-posta veya Telefon Numarası)")
        layout.addWidget(self.label_contact_info)
        self.entry_contact_info = QLineEdit(self.contact_info)
        layout.addWidget(self.entry_contact_info)

        self.button_edit = QPushButton("Düzenle")
        self.button_edit.clicked.connect(self.editCustomer)
        layout.addWidget(self.button_edit)

        self.setLayout(layout)

    def editCustomer(self):
        edited_name = self.entry_customer_name.text()
        edited_contact_info = self.entry_contact_info.text()

        self.parent().setCustomerInfo(edited_name, edited_contact_info)
        QMessageBox.information(self, "Bilgi", "Müşteri başarıyla güncellendi.")
        self.accept()  # Pencereyi kapat


class CRMApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Müşteri İlişkileri Yönetimi")
        self.setWindowIcon(QIcon('logo.png'))  # İkon eklendi
        self.initUI()

        self.customers = []

    def initUI(self):
        main_layout = QVBoxLayout()

        # Müşteri bilgileri giriş alanları
        customer_layout = QVBoxLayout()
        self.label_customer_name = QLabel("Müşteri Adı Soyadı")
        customer_layout.addWidget(self.label_customer_name)
        self.entry_customer_name = QLineEdit()
        customer_layout.addWidget(self.entry_customer_name)
        self.label_contact_info = QLabel("İletişim Bilgisi (E-posta veya Telefon Numarası)")
        customer_layout.addWidget(self.label_contact_info)
        self.entry_contact_info = QLineEdit()
        customer_layout.addWidget(self.entry_contact_info)
        main_layout.addLayout(customer_layout)

        # Müşteri listesi
        self.customer_list = QListWidget()
        self.customer_list.setMaximumHeight(80)  # Yükseklik ayarı
        main_layout.addWidget(self.customer_list)

        # Satış bilgileri giriş alanları
        sales_layout = QVBoxLayout()
        self.label_sale_number = QLabel("Satış Numarası")
        sales_layout.addWidget(self.label_sale_number)
        self.entry_sale_number = QLineEdit()
        sales_layout.addWidget(self.entry_sale_number)
        self.label_products = QLabel("Satılan Ürünler")
        sales_layout.addWidget(self.label_products)
        self.entry_products = QLineEdit()
        sales_layout.addWidget(self.entry_products)
        main_layout.addLayout(sales_layout)

        # Destek talebi giriş alanları
        support_layout = QVBoxLayout()
        self.label_ticket_number = QLabel("Destek Talep Numarası")
        support_layout.addWidget(self.label_ticket_number)
        self.entry_ticket_number = QLineEdit("0212 212 44 44")  # Sabit destek talep numarası
        self.entry_ticket_number.setReadOnly(True)  # Değiştirilemez
        support_layout.addWidget(self.entry_ticket_number)
        self.label_details = QLabel("Talep Detayları")
        support_layout.addWidget(self.label_details)
        self.text_details = QTextEdit()
        self.text_details.setMaximumHeight(90)  # Yükseklik ayarı
        support_layout.addWidget(self.text_details)
        main_layout.addLayout(support_layout)

        # İşlem düğmeleri
        button_layout = QHBoxLayout()

        self.button_add_customer = QPushButton("Müşteri Ekle")
        self.button_add_customer.clicked.connect(self.add_customer)
        self.button_add_customer.setObjectName("button_add_customer")
        button_layout.addWidget(self.button_add_customer)

        self.button_add_sale = QPushButton("Satış Ekle")
        self.button_add_sale.clicked.connect(self.add_sale)
        self.button_add_sale.setObjectName("button_add_sale")
        button_layout.addWidget(self.button_add_sale)

        self.button_create_ticket = QPushButton("Talebi Oluştur")
        self.button_create_ticket.clicked.connect(self.create_support_ticket)
        self.button_create_ticket.setObjectName("button_create_ticket")
        button_layout.addWidget(self.button_create_ticket)

        self.button_delete_customer = QPushButton("Müşteriyi Sil")
        self.button_delete_customer.clicked.connect(self.delete_customer)
        self.button_delete_customer.setObjectName("button_delete_customer")
        button_layout.addWidget(self.button_delete_customer)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # CSS
        self.setStyleSheet("""
            QLineEdit {
            border-radius: 5px;
            padding: 10px 30px;
            font-size: 17px;
            border-bottom: 2px solid #cc9633;
            }
            QLabel {
            font-size: 17px;
            font-family :Arial;
            }
            #button_add_customer, #button_delete_customer, #button_add_sale, 
                #button_create_ticket {
                color: white;
                font-family : Arial;
                padding: 12px 20px;
                font-size: 16px;
                border-radius:3px;
            }
            #button_add_customer {
                background-color: green;
            }
            #button_delete_customer {
                background-color: red;
            }
            #button_add_sale {
                background-color: green;
            }
            #button_create_ticket {
                background-color: #cc9633;
            }
        """)

    def add_customer(self):
        name = self.entry_customer_name.text()
        contact_info = self.entry_contact_info.text()

        if self.is_valid_contact_info(contact_info):
            self.customers.append(Kullanıcı(name, contact_info))
            self.customer_list.addItem(name)  # Müşteriyi listeye ekle
            # QMessageBox.information(self, "Bilgi", "Müşteri başarıyla eklendi.")
            self.label_customer_name.setText("Müşteri Adı: " + name)
            self.label_contact_info.setText("İletişim Bilgisi: " + contact_info)
        else:
            QMessageBox.warning(self, "Uyarı", "Geçerli bir e-posta veya telefon numarası girin.")

    def delete_customer(self):
        selected_customer = self.customer_list.currentItem()
        if selected_customer:
            index = self.customer_list.row(selected_customer)
            del self.customers[index]
            self.customer_list.takeItem(index)  # Müşteriyi listeden kaldır
            QMessageBox.information(self, "Bilgi", "Müşteri başarıyla silindi.")

            self.entry_customer_name.clear()
            self.entry_contact_info.clear()
            self.entry_sale_number.clear()
            self.entry_products.clear()
            self.entry_ticket_number.clear()
            self.text_details.clear()

            self.label_customer_name.setText("Müşteri Adı")
            self.label_contact_info.setText("İletişim Bilgisi (E-posta veya Telefon Numarası)")
            self.label_sale_number.setText("Satış Numarası")
            self.label_products.setText("Satılan Ürünler")
            self.label_ticket_number.setText("Destek Talep Numarası")
            self.text_details.setText("")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir müşteri seçin.")

    def add_sale(self):
        sale_number = self.entry_sale_number.text()
        products = self.entry_products.text().split(",")
        if self.customers:
            self.customers[-1].add_sale(sale_number, products)
            self.label_sale_number.setText("Satış Numarası: " + sale_number)
            self.label_products.setText("Satılan Ürünler: " + ", ".join(products))
        else:
            QMessageBox.warning(self, "Uyarı", "Önce bir müşteri ekleyin.")

    def create_support_ticket(self):
        ticket_number = '0212 212 44 44'
        details =  "Müşteri: " + self.entry_customer_name.text() + "\n" + \
                  "İletişim Bilgisi: " + self.entry_contact_info.text() + "\n" + \
                  "Satış Numarası: " + self.entry_sale_number.text() + "\n" + \
                  "Satılan Ürünler: " + self.entry_products.text() + "\n" + \
                  self.text_details.toPlainText()
        if self.customers:
            self.customers[-1].create_support_ticket(ticket_number, details)
            self.label_ticket_number.setText("Destek Talep Numarası: " + ticket_number)
            self.text_details.setText("<b>- Talep Detayları - </b>\n\n" + details.replace('\n', '<br>'))
            QMessageBox.information(self, "Bilgi", "Destek talebi başarıyla oluşturuldu.")
        else:
            QMessageBox.warning(self, "Uyarı", "Önce bir müşteri ekleyin.")

    def is_valid_contact_info(self, contact_info):
        email_pattern = r'^\S+@\S+\.\S+$'
        phone_pattern = r'^\d{10}$'
        return re.match(email_pattern, contact_info) or re.match(phone_pattern, contact_info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CRMApp()
    window.show()
    sys.exit(app.exec_())
