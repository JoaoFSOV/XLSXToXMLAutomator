import tkinter as tk
from tkinter import filedialog

from .xmlUpdater import updateXmlFile
from .excelReader import readCredentials, readUris, extractApplicationName, filterData

def runGui():
    def browseFile(entryField, filetypes):
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            entryField.delete(0, tk.END)
            entryField.insert(0, filepath)

    def submit():
        file1 = file1Entry.get()
        file2 = file2Entry.get()
        file3 = file3Entry.get()
       
        print("File 1 (Credentials):", file1)
        print("File 2 (URIs):", file2)
        print("File 3 (XML):", file3)
        print("Application Name: ", extractApplicationName(file3))

        if file1 and file2 and file3:
            print("I AM READING BOTH XLSX FILES AND UPDATING XML FILE'S PASSWORDS AND PATHS")
            #credentials = readCredentials(file1, file3)
            #uriMappings = readUris(file2)
            #updateXmlFile(file3, credentials, uriMappings, mode=1)
        elif file1 and file3:
            print("I AM READING THE PASSWORD XLSX FILE AND UPDATING XML FILE'S PASSWORDS")
            credentials = readCredentials(file1, file3)
            updateXmlFile(file3, credentials, None, mode=2)
        elif file2 and file3:
            print("I AM READING THE PORT EXPORTS XLSX FILE AND UPDATING XML FILE'S PATHS")
            #uriMappings = readUris(file2)
            #updateXmlFile(file3, None, uriMappings, mode=3)

    root = tk.Tk()
    root.title("BizTalk Binding Updater")

    # File 1 - Excel (Credentials)
    tk.Label(root, text="Excel File (Credentials):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    file1Entry = tk.Entry(root, width=50)
    file1Entry.grid(row=0, column=1, padx=5)
    tk.Button(root, text="Browse", command=lambda: browseFile(file1Entry, [("Excel files", "*.xlsx")])).grid(row=0, column=2, padx=5)

    # File 2 - Excel (URIs)
    tk.Label(root, text="Excel File (URI Mapping):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    file2Entry = tk.Entry(root, width=50)
    file2Entry.grid(row=1, column=1, padx=5)
    tk.Button(root, text="Browse", command=lambda: browseFile(file2Entry, [("Excel files", "*.xlsx")])).grid(row=1, column=2, padx=5)

    # File 3 - XML File
    tk.Label(root, text="Binding XML File:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    file3Entry = tk.Entry(root, width=50)
    file3Entry.grid(row=2, column=1, padx=5)
    tk.Button(root, text="Browse", command=lambda: browseFile(file3Entry, [("XML files", "*.xml")])).grid(row=2, column=2, padx=5)

    # Submit button
    tk.Button(root, text="Run", command=submit).grid(row=4, column=1, pady=10)

    root.mainloop()

