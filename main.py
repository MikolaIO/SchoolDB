from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
import sqlite3

root = Tk()
root.title("Dane osobowe")
root.geometry("1000x500")

conn = sqlite3.connect('address_book.db') #create or connect database
c = conn.cursor() #create cursor

sql = "SELECT * FROM addresses"
c.execute("SELECT *, oid FROM addresses")
rows = c.fetchall()

tv = ttk.Treeview(root, columns=(1, 2, 3, 4, 5), show="headings", height="5")
tv.grid(row=12, column=0, columnspan=5)

tv.heading(1, text="Imię")
tv.heading(2, text="Nazwisko")
tv.heading(3, text="Adres")
tv.heading(4, text="Miasto")
tv.heading(5, text="Kod")

for i in rows:
    tv.insert('', 'end', values=i)

'''
c.execute("""CREATE TABLE addresses (
        imie text,
        nazwisko text,
        adres text,
        miasto text,
        kod_pocztowy integer
        )""")
'''

def delete():
     
    conn = sqlite3.connect('address_book.db') #create or connect database
    c = conn.cursor() #create cursor

    c.execute("DELETE from addresses WHERE oid= " + delete_box.get())    

    conn.commit()

    conn.close()


def submit():
    
    conn = sqlite3.connect('address_book.db') #create or connect database
    c = conn.cursor() #create cursor
    
    c.execute("INSERT INTO addresses VALUES (:imie, :nazwisko, :adres, :miasto, :kod_pocztowy)",
          {
              'imie': imie.get(),
              'nazwisko': nazwisko.get(),
              'adres': adres.get(),
              'miasto': miasto.get(),
              'kod_pocztowy': kod_pocztowy.get()

          })
    
    
    conn.commit()
    conn.close()
    
    imie.delete(0, END)
    nazwisko.delete(0, END)
    adres.delete(0, END)
    miasto.delete(0, END)
    kod_pocztowy.delete(0, END)

def query():
    
    conn = sqlite3.connect('address_book.db') #create or connect database
    c = conn.cursor() #create cursor
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    
    print_records = ''
    for record in records:
        print_records += str(record) + "\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=11, column=0, columnspan=2)

    conn.commit()
    conn.close()

def update():
    
    conn = sqlite3.connect('address_book.db')

    c = conn.cursor()


    record_id = delete_box.get()

    c.execute("""UPDATE addresses SET
        imie = :im,
        nazwisko = :nazw,
        adres = :adr,
        miasto = :mia,
        kod_pocztowy = :kod

        WHERE oid = :oid""",
        {
        'im': imie_editor.get(),
        'nazw': nazwisko_editor.get(),
        'adr': adres_editor.get(),
        'mia': miasto_editor.get(),
        'kod': kod_pocztowy_editor.get(),
        'oid': record_id
        
        })

    conn.commit()
    conn.close()

    editor.destroy()

def edit():
    global editor
    editor = Tk()
    editor.title("Edytuj dane")
    editor.geometry("400x170")

    conn = sqlite3.connect('address_book.db')

    c = conn.cursor()
    
    record_id = delete_box.get()

    c.execute("SELECT * FROM addresses WHERE oid = " + record_id)
    records = c.fetchall()

    global imie_editor
    global nazwisko_editor
    global adres_editor
    global miasto_editor
    global kod_pocztowy_editor


    imie_editor = Entry(editor, width=30)
    imie_editor.grid(row=0, column=1, padx=20)

    nazwisko_editor = Entry(editor, width=30)
    nazwisko_editor.grid(row=1, column=1)

    adres_editor = Entry(editor, width=30)
    adres_editor.grid(row=2, column=1)

    miasto_editor = Entry(editor, width=30)
    miasto_editor.grid(row=3, column=1)

    kod_pocztowy_editor = Entry(editor, width=30)
    kod_pocztowy_editor.grid(row=4, column=1)

    imie_label = Label(editor, text="Imię")
    imie_label.grid(row=0, column=0)

    nazwisko_label = Label(editor, text="Nazwisko")
    nazwisko_label.grid(row=1, column=0)

    adres_label = Label(editor, text="Adres")
    adres_label.grid(row=2, column=0)

    miasto_label = Label(editor, text="Miasto")
    miasto_label.grid(row=3, column=0)

    kod_pocztowy_label = Label(editor, text="Kod Pocztowy")
    kod_pocztowy_label.grid(row=4, column=0)

    
    for record in records:
        imie_editor.insert(0, record[0])
        nazwisko_editor.insert(0, record[1])
        adres_editor.insert(0, record[2])
        miasto_editor.insert(0, record[3])
        kod_pocztowy_editor.insert(0, record[4])

    edit_btn = Button(editor, text="Zapisz pole", command=update)
    edit_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=142)


imie = Entry(root, width=30)
imie.grid(row=0, column=1, padx=20)

nazwisko = Entry(root, width=30)
nazwisko.grid(row=1, column=1)

adres = Entry(root, width=30)
adres.grid(row=2, column=1)

miasto = Entry(root, width=30)
miasto.grid(row=3, column=1)

kod_pocztowy = Entry(root, width=30)
kod_pocztowy.grid(row=4, column=1)

delete_box = Entry(root, width=30)
delete_box.grid(row=8, column=1)

imie_label = Label(root, text="Imię")
imie_label.grid(row=0, column=0)

nazwisko_label = Label(root, text="Nazwisko")
nazwisko_label.grid(row=1, column=0)

adres_label = Label(root, text="Adres")
adres_label.grid(row=2, column=0)

miasto_label = Label(root, text="Miasto")
miasto_label.grid(row=3, column=0)

kod_pocztowy_label = Label(root, text="Kod Pocztowy")
kod_pocztowy_label.grid(row=4, column=0)

delete_box_label = Label(root, text="Numer ID")
delete_box_label.grid(row=8, column=0)

submit_btn = Button(root, text="Dodaj do bazy danych", command=submit)
submit_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

query_btn = Button(root, text="Pokaż dane", command=query)
query_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

delete_btn = Button(root, text="Wybierz ID", command=delete)
delete_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=138)


edit_btn = Button(root, text="Edytuj ID", command=edit)
edit_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=142)


conn.commit()

conn.close()

root.mainloop()
