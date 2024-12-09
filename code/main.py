# (C) TobiasF./Bernd F. - Geltende Lizenzbedingungen - 06.12.2024

# IMPORTS
import os
from asyncio import wait_for
from email.policy import default
from idlelib.configdialog import is_int

from colorama import Fore, Back, Style
import csv
import glob
from xlsxwriter.workbook import Workbook
import sys
import time

#TkInter
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

#TODO: Error handling

#CODE
def main():
    """
    Main-Funktion des Programms.
    Ruft die Funktionen auf und gibt die Begrüßung aus.
    """
    tk_window = tk.Tk()
    tk_window.title("CSV-Converter")
    #TODO LOGO
    tk_window.configure(bg="white") # TODO: Darkmode?
    tk_window.geometry("500x500")
    tk_window.resizable(False, False)
    make_menu(tk_window)
    check_vars = make_checkbt_outputtype_tk(tk_window)
    make_file_explorer_tk(tk_window, check_vars)
    tk_window.mainloop()

def make_menu(root):
    menu = Menu(root)
    root.config(menu=menu)
    file_menu = Menu(menu)
    menu.add_cascade(label="Datei", menu=file_menu)
    file_menu.add_command(label="Einstellungen", command=lambda: messagebox.showinfo("Einstellungen", "Einstellungen sind aktuell nicht verfügbar.")) #TODO: Einstellungen
    file_menu.add_command(label="Beenden", command=root.quit)
    help_menu = Menu(menu)
    menu.add_cascade(label="Hilfe", menu=help_menu)
    help_menu.add_command(label="Über", command=lambda: messagebox.showinfo("Über", "CSV-Converter\nVersion 1.0\n(C) TobiasF./Bernd F."))
    help_menu.add_command(label="Hilfe", command=lambda: messagebox.showinfo("Hilfe", "Wählen Sie die Datei aus, die Sie konvertieren möchten. Anschließend wählen Sie das gewünschte Format aus und klicken auf 'Konvertieren'."))
    help_menu.add_command(label="Lizenz", command=lambda: messagebox.showinfo("Lizenz", "Lizenzbedingungen:\n\nDas Programm CSV-Converter ist ein Open-Source-Projekt und unterliegt der MIT-Lizenz."))


def make_file_explorer_tk(root, check_vars):
    """
    Erstellt ein Fenster, in dem der Benutzer eine Datei auswählen kann.
    """
    def open_file_explorer():
        try:
            file = filedialog.askopenfilename(filetypes=[("CSV files",".csv")])
        except:
            RaiseError("1105")
        if file == '':
            RaiseError("1105")
        make_convert_bt(root, file.replace("/", "\\"), check_vars)
        Label(root, text=f"Die ausgewählte Datei ist: {file}", wraplength=400).grid(row=4, column=0, sticky="W", pady=10)
    Label(text="Wählen Sie die Datei aus, die Sie konvertieren möchten:").grid(row=0, column=0, sticky="W", pady=10)
    file_explorer_button = Button(root, text="Datei auswählen", command=open_file_explorer)
    file_explorer_button.grid(row=0, column=1)

def make_checkbt_outputtype_tk(root):
    """
    Erstellt Radiobuttons, um den Dateityp auszuwählen.
    """
    try:
        Label(root, text="Wählen Sie den Dateityp aus, in den Sie konvertieren möchten: ").grid(row=1, column=0, sticky="W", pady=10)
    except:
        RaiseError("1301")
    try:
        output_type = IntVar(value=1)
        r1 = Checkbutton(root, text=".xlsx", variable=output_type)
        r2 = Checkbutton(root, text=".pdf", variable=IntVar())
        r3 = Checkbutton(root, text=".ods", variable=IntVar())
        r1.configure(state = DISABLED)
        r2.configure(state = DISABLED)
        r3.configure(state = DISABLED)
        r1.grid(row=1, column=1)
        r1.select()
        r2.grid(row=2, column=1)
        r3.grid(row=3, column=1)
        return output_type
    except:
        RaiseError("1201/1202")

def make_convert_bt(root, file, check_vars):
    """
    Erstellt die GUI für den Benutzer.
    """
    convert_text = Label(root, text="Mit dem Klick auf den Button wird die Datei konvertiert: ").grid(row=5, column=0, sticky="W", pady=10)
    convert_button = Button(root, text="Konvertieren", command=lambda: convert(file, check_vars, root)).grid(row=5, column=1)

def convert(file, check_vars, root):
    """
    Konvertiert die Datei in das gewünschte Format.
    """
    file_exists_cont = False
    while True:
        if not os.path.isfile(file.replace(".csv", ".xlsx")) or file_exists_cont:
            if check_vars.get() == 1:
                convert_csv_to_xlsx(file, root)
                break
            #elif output_type2.get() == 1:
                #convert_csv_to_pdf(file)   # IN WORK
            #elif output_type3.get() == 1:
                #convert_csv_to_ods(file)
        else:
            user_input = messagebox.askyesno("Datei existiert bereits!", "Die Datei existiert bereits. Trotzdem fortfahren?")
            if user_input:
                file_exists_cont = True
                continue
            else:
                RaiseError("0000")




def convert_csv_to_xlsx(file_path, root):
    """
    Konvertiert eine CSV-Datei in eine XLSX-Datei.
    """
    # Erstellt eine neue XLSX-Datei
    file_path_no_ending = file_path.replace(".csv", "")
    workbook = Workbook(file_path_no_ending + ".xlsx")
    worksheet = workbook.add_worksheet()
    # Öffnet die CSV-Datei
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        # Schreibt die Daten in die XLSX-Datei
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()
    Label(root, text=f"Datei wurde unter folgendem Namen gespeichert: {file_path_no_ending + ".xlsx"}", wraplength=400).grid(row=6, column=0, sticky="W", pady=10)

def RaiseError(error_code):
    """
    Gibt Fehlermeldungen aus und beendet das Programm.
    """
    messagebox.showerror(f'CSV-Converter - Error {error_code}', f'An error occurred!\nError code: {error_code}')
    sys.exit(int(error_code))

if __name__ == "__main__":
    try:
        main() # Startet das Programm
    except:
        if not KeyboardInterrupt:
            RaiseError('1099')