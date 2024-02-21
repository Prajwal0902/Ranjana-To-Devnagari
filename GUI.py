from tkinter import *
from mytranslator import MyTranslator
import textblob
from tkinter import ttk, messagebox, simpledialog
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('translation_app.db')
c = conn.cursor()


class Translation:
#Defines a Translation class to store translation details
# (original text, translated text, from language, to language).
    def __init__(self, original, translated, from_lang, to_lang):
        self.original = original
        self.translated = translated
        self.from_lang = from_lang
        self.to_lang = to_lang


def login():
    username = simpledialog.askstring("Login", "Enter your username:")
    password = simpledialog.askstring("Login", "Enter your password:", show="*")

    # Perform basic authentication (replace this with secure authentication)
    if username == "admin" and password == "admin":
        root.deiconify()  # Show the main window
    else:
        messagebox.showerror("Login Failed", "Invalid username or password, please try again")
        root.destroy()  # Close the application


def translate_it():
    # Delete any previous Translations
    translated_text.delete(1.0, END)
    try:
        # Get Languages From Dictionary Keys
        # Get the From Language Key
        for key, value in languages.items():
            if value == orginal_combo.get():
                from_language_key = key

        # Get the to Language Key
        for key, value in languages.items():
            if value == translated_combo.get():
                to_language_key = key

        # Turn Original Text into a Textblob
        words = textblob.TextBlob(orginal_text.get(1.0, END))

        # Translate Text
        words = words.translate(from_lang=from_language_key, to=to_language_key)

        # Output translated text to screen
        translated_text.insert(1.0, words)

        # Append translation to history
        translation = translated_text.get(1.0, END).strip()
        history_listbox.insert(END, translation)

        # Create a translation object
        translation = Translation(
            orginal_text.get(1.0, END).strip(),
            translated_text.get(1.0, END).strip(),
            orginal_combo.get(),
            translated_combo.get()
        )

        # Display translation details in the history_listbox
        history_listbox.insert(END, f"From: {translation.from_lang}, To: {translation.to_lang}\n"
                                     f"Original: {translation.original}\n"
                                     f"Translated: {translation.translated}\n\n")

    except Exception as e:
        messagebox.showerror("Translator", e)


def reverse_translate():
    #Translates text from the original language to the selected target language and displays it in the GUI. 
    # It also updates the translation history.
    # Exchange text between orginal_text and translated_text
    original_text_content = orginal_text.get(1.0, END).strip()
    translated_text_content = translated_text.get(1.0, END).strip()

    orginal_text.delete(1.0, END)
    translated_text.delete(1.0, END)

    orginal_text.insert(1.0, translated_text_content)
    translated_text.insert(1.0, original_text_content)

    # Change combo grid currents
    orginal_index = orginal_combo.current()
    translated_index = translated_combo.current()

    orginal_combo.current(translated_index)
    translated_combo.current(orginal_index)


def clear():
    # Clear the text boxes
    orginal_text.delete(1.0, END)
    translated_text.delete(1.0, END)


def clear_history():
    # Clear the translation history listbox
    history_listbox.delete(0, END)


# language_list = (1,2)

# Grabe Language List From GoogleTrans
languages = MyTranslator.LANGUAGES

# Convert to List
language_list = list(languages.values())


def on_hover(event):
    # Change color on hover
    event.widget.config(bg="#b3e0ff")

def copy_translated_text():
    translated_text_content = translated_text.get(1.0, END).strip()
    root.clipboard_clear()
    root.clipboard_append(translated_text_content)
    root.update()

root = Tk()
# root.withdraw()  # Hide the main window until login is successful
root.title('Trail - Translation')
root.geometry("1200x400")

# Login
login()

# Text Boxes
orginal_text = Text(root, height=10, width=40)
orginal_text.grid(row=0, column=0, pady=20, padx=10)

translate_button = Button(root, text="Transalate", font=("Helvetica", 24), command=translate_it)
translate_button.grid(row=0, column=1, padx=10)
translate_button.bind("<Enter>", on_hover)
translate_button.bind("<Leave>", lambda event: translate_button.config(bg="SystemButtonFace"))

# Copy button
copy_button = Button(root, text="Copy", command=copy_translated_text)
copy_button.grid(row=0, column=3, padx=10)
copy_button.bind("<Enter>", on_hover)
copy_button.bind("<Leave>", lambda event: copy_button.config(bg="SystemButtonFace"))

translated_text = Text(root, height=10, width=40)
translated_text.grid(row=0, column=2, pady=20, padx=10)


# combo boxes
orginal_combo = ttk.Combobox(root, width=50, value=language_list)
orginal_combo.current(0)
orginal_combo.grid(row=1, column=0)

translated_combo = ttk.Combobox(root, width=50, value=language_list)
translated_combo.current(1)
translated_combo.grid(row=1, column=2)

# Clear button
clear_button = Button(root, text="Clear", command=clear)
clear_button.grid(row=2, column=1)

# Reverse translation button
reverse_translate_button = Button(root, text="Reverse Translate", command=reverse_translate)
reverse_translate_button.grid(row=1, column=1)

# History Listbox
history_label = Label(root, text="Translation History")
history_label.grid(row=3, column=0, columnspan=3, pady=5)

history_listbox = Listbox(root, height=5, width=80)
history_listbox.grid(row=4, column=0, columnspan=3, pady=5, padx=10, sticky="nsew")

# Scrollbar for the history listbox
history_scrollbar = Scrollbar(root, orient="vertical")
history_scrollbar.config(command=history_listbox.yview)
history_scrollbar.grid(row=4, column=3, pady=5, sticky="ns")

history_listbox.config(yscrollcommand=history_scrollbar.set)

# Clear history button
clear_history_button = Button(root, text="X", command=clear_history, fg="Red")
clear_history_button.grid(row=3, column=3, columnspan=2, pady=(5, 10))

# Footer for the development information
footer_label = Label(root, text="© 2023 Translation App. All rights reserved.", font=("Helvetica", 10), fg="gray")
footer_label.grid(row=6, column=0, columnspan=3, pady=(20, 5))

root.mainloop()
