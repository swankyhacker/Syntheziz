from tkinter import *
from tkinter import filedialog, Listbox, messagebox
from PyPDF2 import PdfFileMerger, utils
import os

files = []
destination = "D:/Bruce/Documents/"

root = Tk()
root.geometry("630x650")
root.title("Syntheziz")
root.configure(bg="#263D42")


def isDuplicate():  # Checks for duplicate files in files array and asks users for permission
    selectedFiles = filedialog.askopenfilenames(initialdir="/", title="Select Files",
                                                filetypes=(("PDF", "*.pdf"), ("All Files", "*.*")))
    for file in selectedFiles:
        if file in files:
            title = "Duplicate Files Detected!"
            content = "Duplicate Files were detected \n Do you still want to include duplicates in the merged result?"
            response = messagebox.askyesno(title, content)

            if(response == 1):
                addFile(file)

        else:
            addFile(file)


def addFile(file):  # Adds a file to files array and file name to frame
    files.append(file)
    fileName = file[file.rfind("/")+1:]
    label = Label(frame, text=f"~ {fileName}", bg="#263D42", fg="white", width=20, anchor=W,
                  font=("Helvetica", 12))
    label.grid()


def convertFiles():  # Makes use of PyPDF library to merge selected files in files array
    merger = PdfFileMerger()

    if len(files) > 0:
        for file in files:
            merger.append(file)
        if not os.path.exists(destAddress.get() + 'merged.pdf'):
            merger.write(destAddress.get() + 'Merged.pdf')
    merger.close()


def changePath():
    mergedFilePath = filedialog.askdirectory(
        initialdir="/", title="Select Destination Folder")
    destAddress.config(state=NORMAL)
    destAddress.delete(0, END)
    destAddress.insert(0, f"{mergedFilePath}/")
    destAddress.config(state=DISABLED)


def clearFiles():  # Clears all files from the array and frame
    for widget in frame.winfo_children():
        widget.destroy()
    files.clear()


def test():
    return


frame = Frame(root, bg="white", width=560, height=400)
frame.grid_propagate(0)
frame.grid(row=0, column=0, padx=30, pady=30, columnspan=6, rowspan=6)

destAddress_label = Label(
    root, text="Destination Address:", bg="#263D42", fg="white")
destAddress_label.grid(row=7, column=0)

destAddress = Entry(root, width=50)
destAddress.grid(row=7, column=1, columnspan=3)
destAddress.insert(0, destination)
destAddress.config(state=DISABLED)

findPath = Button(root, bg="#263D42", fg="white",
                  text="...", command=changePath)
findPath.grid(row=7, column=4)

deleteFiles = Checkbutton(
    root, text="Delete files after merging", bg="#263D42", fg="white")
deleteFiles.grid(row=9, column=0)

openFile = Button(root, text="Open File", padx=10, pady=5, width=10,
                  bg="#263D42", fg="white", command=isDuplicate)
openFile.grid(row=7, column=5)

convertFiles = Button(root, text="Convert Files", fg="white", width=10,
                      bg="#263D42", padx=10, pady=5, command=convertFiles)
convertFiles.grid(row=8, column=5, pady=15)

clear = Button(root, text="Clear", padx=10, pady=5, width=10,
               bg="#263D42", fg="white", command=clearFiles)
clear.grid(row=9, column=5)

testButton = Button(root, text="Test", padx=10, pady=5, width=10,
                    bg="#263D42", fg="white", command=test)
testButton.grid(row=10, column=5)

root.mainloop()

# # Grid
# Order of files
# file duplication
# custom file name
# delete files
# change destination
# Exceptions
# design
