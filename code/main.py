# (C) TobiasF./Bernd F. - Geltende LizenzTbedingungen - 15.12.2024

# IMPORTS
import os

import csv

from xlsxwriter.workbook import Workbook
import subprocess
import sys
import time
import json
from datetime import date

#PYFILES
from credits import make_credits

#TkInter
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


#CLASSES
class Windows:
    """
    Class to create windows with tkinter.
    """
    def __init__(self):
        self.title = ""

    def __str__(self):
        return "Class windows:\nFunctions:\n- makeWindow\n- makeDarkMode\n- makeLabel\n- makeButton\n- makeTextBox\n- makeEntry"

    def makeWindow(self, title, geo="500x500"):
        # INIT WINDOW
        window = tk.Tk()
        window.resizable(False, False)
        window.configure(bg="white")

        self.title = title
        window.title(self.title)
        window.geometry(geo)

        return window

    def makeDarkMode(self):
        ... # TODO: Implement dark mode(v0.4.9x)

    def makeLabel(self, root, text, row, column, sticky="W", pady=10):
        label = Label(root, text=text)
        label.grid(row=row, column=column, sticky=sticky, pady=pady)
        return label

    def makeButton(self, type, root, text, command, row, column, sticky="W", pady=5):
        # TODO: Implement button types
        match type:
            case _:
                return Button(root, text=text, command=command).grid(row=row, column=column, sticky=sticky, pady=pady)

    # TODO TESTING
    def makeTextBox(self, root, text, scrollbar_config=True, width=None, height=None, put_type="pack", row=0, column=0):
        if width == None:
            width = root.winfo_width()
        if height == None:
            height = root.winfo_height()

        text_widget = Text(root, wrap="word", width=width, height=height)
        if scrollbar_config:
            scrollbar = Scrollbar(root, command=text_widget.yview)
            scrollbar.pack(side="right", fill="y")

            text_widget.config(yscrollcommand=scrollbar.set)

        if put_type == "pack":
            try:
                text_widget.pack(side="left", fill="both", expand=True)
            except:
                try:
                    text_widget.grid(row=row, column=column)
                except:
                    RaiseError("1301")
        #elif put_type == "grid": #TODO BUGFIX
        #    try:
        #        text_widget.grid(row=row, column=column)
        #    except:
        #        try:
        #            text_widget.pack(side="left", fill="both", expand=True)
        #        except:
        #            RaiseError("1301")
        else:
            RaiseError("1201")

        text_widget.insert("1.0", text)

        return text_widget

    def makeEntry(self, root, text, row, column, sticky="WE", pady=10): #TODO
        self.makeLabel(root, text, row, column, sticky, pady).configure(font=("Arial", 10), bg="white")
        entry = Entry(root)
        entry.grid(row=row, column=column+1, sticky=sticky, pady=pady)
        return entry

    # INFO: If making a new function, add it to the __str__ function


class ShowWindows:
    def __init__(self):
        ...

    def __str__(self):
        return "Class ShowWindows:\nFunctions:\n- show_changelogs\n- show_about\n- show_settings\n- show_feedback\n- show_credits"

    def show_changelogs(self):
        """
        Creates a new window to display the changelogs.
        """
        changelog_window = Windows().makeWindow(language_file_windows["changelogs"]["title"])

        text_widget = Windows().makeTextBox(changelog_window, "Changelogs", scrollbar_config=True)

        with open("../changelogs.txt", "r") as f:
            changelog = f.read()
        f.close()

        text_widget.insert("1.0", changelog)
        text_widget.config(state=DISABLED)

        if json.load(open("../config/config.json", "r"))["settings"]["intern"]["language"] == "DE":
            messagebox.showinfo("Changelogs", "Diese Funktion ist noch nicht auf Deutsch verfügbar!")
            changelog_window.focus()

    def show_about(self):
        """
        Creates a new window to display the about.
        """
        about_window = Windows().makeWindow(language_file_windows["about"]["title"])

        text_widget = Windows().makeTextBox(about_window, "About", scrollbar_config=False)
        with open("../config/config.json", "r") as config_file:
            config = json.load(config_file)
        config_file.close()

        text_widget.insert("1.0", f"CSV-Converter\nVersion {config["settings"]["version"]}\n(C) Tobias F./Bernd F.")
        # UPDATE IN LANGUAGE SETTINGS
        text_widget.config(state=DISABLED)

    def show_settings(self, root):
        """
        Creates a new window to display the settings.
        """

        def make_setting_point(root, text, row, column, command):
            label = Windows().makeLabel(root, text + ":", row, column)
            button = Windows().makeButton("normal", root, text, command, row, column + 1)

        settings_window = Windows().makeWindow(language_file_windows["settings"]["title"])

        title = Windows().makeLabel(settings_window, language_file_windows["settings"]["title"], 0, 0, pady=10)
        title.configure(font=("Arial", 16), fg="black", bg="yellow", relief="groove", borderwidth=2, padx=10, pady=5)

        Windows().makeLabel(settings_window,
                            ''.join(s + "\u0332" for s in language_file_windows["settings"]["language"]), 1, 0,
                            pady=10).configure(font=("Arial", 12))

        lang_var = json.load(open("../config/config.json", "r"))["settings"]["intern"]["language"]
        beta_var = json.load(open("../config/config.json", "r"))["settings"]["intern"]["beta-features"]

        def lang_var_set_de():
            nonlocal lang_var
            lang_var = "DE"

        def lang_var_set_en():
            nonlocal lang_var
            lang_var = "EN"

        def beta_var_set():
            nonlocal beta_var
            beta_var = not beta_var

        make_setting_point(settings_window, "Deutsch", 2, 0, command=lang_var_set_de)
        Windows().makeLabel(settings_window, "Nicht 100% fertig!", 2, 2, pady=10).configure(font=("Arial", 8))
        make_setting_point(settings_window, "English", 3, 0, command=lang_var_set_en)

        def safe_data():
            sure = messagebox.askyesno("Save settings", "Are you sure you want to save the settings?")  # TODO LANGUAGE
            if sure:
                with open("../config/config.json", "r+") as config_file:
                    config = json.load(config_file)
                    config["settings"]["intern"]["language"] = lang_var
                    config["settings"]["intern"]["beta-features"] = beta_var
                    config_file.seek(0)
                    config_file.write(json.dumps(config, indent=4))
                    config_file.truncate()
                root.destroy()
                settings_window.destroy()
                main()

        Windows().makeLabel(settings_window, "BETA-TEST:", 4, 0, pady=10).configure(font=("Arial", 12))
        Windows().makeButton("normal", settings_window, "BETA-TEST", beta_var_set, 4, 1, pady=10)  # TODO

        Windows().makeButton("normal", settings_window, language_file_windows["settings"]["save_button"], row=5,
                             column=0, sticky="W", pady=10, command=safe_data)
        Windows().makeButton("normal", settings_window, language_file_windows["settings"]["cancel_button"],
                             lambda: settings_window.destroy(), 5, 1, sticky="W", pady=10)
        Windows().makeButton("normal", settings_window, "Reset settings",
                             lambda: messagebox.showinfo("Reset settings", "This feature is not available yet."), 5, 2,
                             pady=10)  # TODO

        settings_window.mainloop()

    def show_feedback(self):
        """
        Creates a new window to display the feedback.
        """

        # PACK METHODE USED!!!!

        feedback_window = Windows().makeWindow("Feedback[BETA]")

        title = Label(feedback_window, text="Feedback", wraplength=300, justify="center")
        title.pack()
        title.configure(font=("Arial", 16), fg="black", bg="yellow", relief="groove", borderwidth=2, padx=10, pady=5,
                        justify="center")

        expl_feedback = Label(feedback_window, text="Please enter your feedback here:", wraplength=300, justify="center")
        expl_feedback.pack()

        input_feedback = Text(feedback_window, wrap="word", height=10, width=50)
        input_feedback.pack()

        def limit_chars(event):
            if len(input_feedback.get("1.0", "end-1c")) > 256:
                input_feedback.delete("1.0 + 257c", "end-1c")
            if len(input_feedback.get("1.0", "end-1c")) > 256:
                char_limit_label.pack()
            else:
                char_limit_label.pack_forget()


        # Bind the function to the Text widget
        input_feedback.bind("<KeyPress>", limit_chars)

        char_limit_label = Label(feedback_window, text="Max. 256 characters", wraplength=300, justify="center")
        char_limit_label.configure(fg="red", bg="white")

        send_feedback = Button(feedback_window, text="Send feedback", command=lambda: messagebox.showinfo("Feedback", "This feature is not available yet."))
        send_feedback.pack()

        feedback_window.mainloop()

    def show_donate(self):
        """
        Creates a new window to display the donate options.
        """
        donate_window = Windows().makeWindow("Donate")

        Label(donate_window, text="", height=5, justify="center", bg="white").pack()

        title = Label(donate_window, text="Donate", wraplength=300, justify="center")
        title.pack()
        title.configure(font=("Arial", 16), fg="black", bg="yellow", relief="groove", borderwidth=2, padx=10, pady=5, justify="center")
        donate_value = Entry(donate_window, width=10, justify="center", font=("Arial", 12), bg="white", relief="groove")
        donate_value.pack()
        donate_value.insert(0, "5$")
        donate_value.focus()
        def print_value():
            label = Label(donate_window, text=f"Thank you for your donation of {donate_value.get()}.", wraplength=300, justify="center").pack()
        donate_value.bind("<Return>", lambda event: (donate_value.insert("end", "$") if not donate_value.get().endswith("$") else None, print_value()))

        Label(donate_window, text="Press ENTER to accept value!", height=5, justify="center", bg="white").pack()


        donate_window.mainloop()

    # INFO: If making a new function, add it to the __str__ function






# ~~~~~~~~~~~~~~~~~~~~~~~~~~~CODE~~~~~~~~~~~~~~~~~~~~~~~~~~~







# TODO: LANGUAGE Updates

# INSTALLING
def install_packages():
    # FOR INSTALLING ONLY!
    subprocess.check_call([sys.executable, "install_requirements.py"])




def main():
    """
    Main-Funktion des Programms.
    Ruft die Funktionen auf und gibt die Begrüßung aus.
    """
    # LANGUAGE
    global language_file_windows
    global language_file_menubar
    try:
        with open("../config/config.json", "r") as config_file:
            config = json.load(config_file)
            if config["settings"]["intern"]["language"] == "DE":
                with open("lan_packs/DE/lang_DE_windows.json", "r") as language_file:
                    language_file_windows = json.load(language_file)
                    language_file_windows = language_file_windows["DE"]["main"]
                language_file.close()
                with open("lan_packs/DE/lang_DE_menubar.json", "r") as language_file_menu:
                    language_file_menubar = json.load(language_file_menu)
                    language_file_menubar = language_file_menubar["DE"]["main"]
                language_file_menu.close()
            elif config["settings"]["intern"]["language"] == "EN":
                with open("lan_packs/EN/lang_EN_windows.json", "r") as language_file:
                    language_file_windows = json.load(language_file)
                    language_file_windows = language_file_windows["EN"]["main"]
                language_file.close()
                with open("lan_packs/EN/lang_EN_menubar.json", "r") as language_file_menu:
                    language_file_menubar = json.load(language_file_menu)
                    language_file_menubar = language_file_menubar["EN"]["main"]
                language_file_menu.close()
        config_file.close()
    except:
       RaiseError("1001")

    # NOTE: Due to incompatibility with the dark mode, the background color is set to white. Dark mode will be implemented in the future.
    tk_window = Windows().makeWindow(language_file_windows["mainwindow"]["title"])
    make_menu(tk_window)
    check_vars = make_checkbt_outputtype_tk(tk_window)
    make_file_explorer_tk(tk_window, check_vars)
    tk_window.mainloop()


def _from_rgb(rgb):
    """
    translates a rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


def make_menu(root):
    menu = Menu(root)
    root.config(menu=menu)

    file_menu = Menu(menu)
    menu.add_cascade(label=language_file_menubar["file"], menu=file_menu)
    file_menu.add_command(label=language_file_menubar["settings"], command=lambda: ShowWindows().show_settings(root))
    file_menu.add_separator()
    file_menu.add_command(label=language_file_menubar["quit"], command=root.quit)

    help_menu = Menu(menu)
    menu.add_cascade(label=language_file_menubar["help"], menu=help_menu)
    help_menu.add_command(label=language_file_menubar["about"], command=lambda: ShowWindows().show_about())
    help_menu.add_command(label=language_file_menubar["changelogs"], command=lambda: ShowWindows().show_changelogs())
    help_menu.add_command(label=language_file_menubar["help"], command=lambda: messagebox.showinfo(language_file_menubar["help"], "Wählen Sie die Datei aus, die Sie konvertieren möchten. Anschließend wählen Sie das gewünschte Format aus und klicken auf 'Konvertieren'.\n\nINFO: DIESE FUNKTION IST NOCH IN ARBEIT!"))
    help_menu.add_command(label=language_file_menubar["licence"], command=lambda: messagebox.showinfo(language_file_menubar["licence"], "Lizenzbedingungen:\n\nDas Programm CSV-Converter ist ein Open-Source-Projekt und unterliegt der MIT-Lizenz(CC BY-NC-SA 4.0)."))

    # BETA
    if json.load(open("../config/config.json", "r"))["settings"]["intern"]["beta-features"]:
        file_menu.add_separator()
        file_menu.add_command(label="Beta-Features", command=..., state=DISABLED)
        file_menu.add_command(label="Feedback", command=lambda: ShowWindows().show_feedback())  # TODO LANGUAGE
        help_menu.add_separator()
        help_menu.add_command(label="Beta-Features", command=..., state=DISABLED)
        help_menu.add_command(label="Credits", command=lambda: make_credits()) #TODO LANGUAGE
        help_menu.add_command(label="Donate", command=lambda: ShowWindows().show_donate()) #TODO LANGUAGE

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
        Label(root, text=f"{language_file_windows["mainwindow"]["opened_file"]}{file}", wraplength=300).grid(row=4, column=0, sticky="W", pady=10)
    Label(text=f"{language_file_windows["mainwindow"]["open_button_label"]}").grid(row=0, column=0, sticky="W", pady=10)
    file_explorer_button = Button(root, text=language_file_windows["mainwindow"]["open_button"], command=open_file_explorer)
    file_explorer_button.grid(row=0, column=1)

def make_checkbt_outputtype_tk(root):
    """
    Erstellt Radiobuttons, um den Dateityp auszuwählen.
    """
    Label(root, text=f"{language_file_windows["mainwindow"]["file_type_label"]}").grid(row=1, column=0, sticky="W", pady=10)
    Label(root, text="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", bg="white").grid(row=1, column=0, sticky="W")
    Label(root, text="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", bg="white").grid(row=2, column=0, sticky="W")
    Label(root, text="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", bg="white").grid(row=3, column=0, sticky="W")
    try:
        output_type = IntVar(value=1)
        r1 = Checkbutton(root, text=".xlsx", variable=output_type)
        r2 = Checkbutton(root, text=".pdf", variable=IntVar())
        r3 = Checkbutton(root, text=".ods", variable=IntVar())
        r1.configure(state = DISABLED)
        r2.configure(state = DISABLED)
        r3.configure(state = DISABLED)
        r1.grid(row=1, column=1, pady=10)
        r1.select()
        r2.grid(row=2, column=1, pady=10)
        r3.grid(row=3, column=1, pady=10)
        return output_type
    except:
        RaiseError("1201/1202")

def make_convert_bt(root, file, check_vars):
    """
    Erstellt die GUI für den Benutzer.
    """
    convert_text = Label(root, text=f"{language_file_windows["mainwindow"]["convert_button_label"]}").grid(row=5, column=0, sticky="W", pady=10)
    convert_button = Button(root, text=f"{language_file_windows["mainwindow"]["convert_button"]}", command=lambda: convert(file, check_vars, root)).grid(row=5, column=1)

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
            user_input = messagebox.askyesno("File already existing", "File already existing. Continue?") # TODO LANGUAGE
            if user_input:
                file_exists_cont = True
                continue
            else:
                break




def convert_csv_to_xlsx(file_path, root):
    """
    Konvertiert eine CSV-Datei in eine XLSX-Datei.
    """
    # Erstellt eine neue XLSX-Datei
    file_path_no_ending = file_path.replace(".csv", "")
    workbook = Workbook(file_path_no_ending + ".xlsx", {'strings_to_numbers': True})
    worksheet = workbook.add_worksheet()
    # Öffnet die CSV-Datei
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        # Schreibt die Daten in die XLSX-Datei
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()
    Label(root, text=f"{language_file_windows["mainwindow"]["saved_to_path_msg"]}{file_path_no_ending + ".xlsx"}", wraplength=300).grid(row=6, column=0, sticky="W", pady=10)

def RaiseError(error_code):
    """
    Gibt Fehlermeldungen aus und beendet das Programm.
    """
    i = 1
    while True:
        if not os.path.exists(f"../logs/error-log_{date.today().strftime('%d-%m-%Y')}_{i}.json"):
            with open(f"../logs/error-log_{date.today().strftime('%d-%m-%Y')}_{i}.json", "w") as error_file:
                error_data = {
                    "error_code": error_code,
                    "error_message": f"An error occurred! Error code: {error_code}",
                    "date": date.today().strftime('%d/%m/%Y') + " // " + time.strftime('%H:%M:%S')
                }
                error_file.write(json.dumps(error_data, indent=4))
            error_file.close()
            break
        i += 1
    messagebox.showerror(f'CSV-Converter - Error {error_code}', f'An error occurred!\nError code: {error_code}')
    sys.exit(int(error_code))


if __name__ == "__main__":
    """    
    try:
        install_packages()
    except:
        RaiseError("1401")
    """
    try:
        main() # Startet das Programm
    except:
       if not KeyboardInterrupt:
            RaiseError('1099')