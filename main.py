import speech_recognition as sr
import smtplib
import sqlite3
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

class InventoryApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Input Nama Perusahaan
        self.layout.add_widget(Label(text='Nama Perusahaan'))
        self.nama_perusahaan = TextInput()
        self.layout.add_widget(self.nama_perusahaan)

        # Input Nama Barang
        self.layout.add_widget(Label(text='Nama Barang'))
        self.nama_barang = TextInput()
        self.layout.add_widget(self.nama_barang)

        # Input Harga Beli
        self.layout.add_widget(Label(text='Harga Beli'))
        self.harga_beli = TextInput()
        self.layout.add_widget(self.harga_beli)

        # Input Harga Jual
        self.layout.add_widget(Label(text='Harga Jual'))
        self.harga_jual = TextInput()
        self.layout.add_widget(self.harga_jual)

        # Input Stok
        self.layout.add_widget(Label(text='Stok'))
        self.stok = TextInput()
        self.layout.add_widget(self.stok)

        # Tombol Simpan Data
        self.simpan_btn = Button(text='Simpan Data')
        self.simpan_btn.bind(on_press=self.simpan_data)
        self.layout.add_widget(self.simpan_btn)

        # Chat Output
        self.chat_output = Label(text='')
        self.layout.add_widget(self.chat_output)

        # Database Setup
        self.conn = sqlite3.connect('inventory.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nama TEXT, harga_beli REAL, harga_jual REAL, stok INTEGER)''')
        self.conn.commit()

        return self.layout

    def simpan_data(self, instance):
        nama = self.nama_barang.text
        beli = self.harga_beli.text
        jual = self.harga_jual.text
        stok = self.stok.text

        if not nama or not beli or not jual or not stok:
            self.chat_output.text = "Harap isi semua data"
            return
        
        try:
            beli = float(beli)
            jual = float(jual)
            stok = int(stok)
        except ValueError:
            self.chat_output.text = "Harga dan stok harus berupa angka"
            return

        self.cursor.execute("INSERT INTO inventory (nama, harga_beli, harga_jual, stok) VALUES (?, ?, ?, ?)",
                            (nama, beli, jual, stok))
        self.conn.commit()
        self.chat_output.text = "Data berhasil disimpan"

    def kirim_email(self):
        sender = "your_email@example.com"
        recipient = "admin@example.com"
        message = "Subject: Laporan Penjualan\n\nLaporan terlampir."

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, "your_password")
            server.sendmail(sender, recipient, message)
            server.quit()
            self.chat_output.text = "Email berhasil dikirim"
        except Exception as e:
            self.chat_output.text = f"Gagal mengirim email: {e}"

if __name__ == "__main__":
    InventoryApp().run()




