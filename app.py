from tkinter import *
from tkinter import filedialog, Listbox, messagebox
from PyPDF2 import PdfFileMerger, utils
import os

files = []
destination = "D:/"
mergedFileName = "Merged"

# colors
mainColor = "#eacdc2"
textColor = "#372549"
checkBoxColor = "#641220"
frameColor = "#f2e9e4"

root = Tk()
root.geometry("630x650")
root.title("Syntheziz")
root.configure(bg=mainColor)


class FrameItem():  # Individual Frame in list of files
    def __init__(self, file, index):
        self.file = file
        self.fileName = self.file[self.file.rfind("/")+1:]
        self.index = index

        self.fileFrame = Frame(frame, bg=mainColor, width=558, height=45)
        self.fileFrame.grid_propagate(0)
        self.fileFrame.grid
        self.fileFrame.grid(padx=1, pady=1)

        self.fileLabel = Label(self.fileFrame, bg=mainColor, text=f'~ {self.fileName}',
                               fg=textColor, width=48, anchor=W, font=("Times New Roman", 12))
        self.fileLabel.grid(column=0, row=0, columnspan=4)

        self.shiftUp = Button(self.fileFrame, bg=mainColor,
                              text="↑", fg=textColor, anchor=N, command=lambda: moveItemUp(self.index))
        self.shiftUp.grid(column=4, row=0, padx=5, pady=10)

        self.shiftDown = Button(
            self.fileFrame, bg=mainColor, text="↓", fg=textColor, anchor=N, command=lambda: moveItemDown(self.index))
        self.shiftDown.grid(column=5, row=0, pady=10, padx=(0, 40))

        self.removeFile = Button(self.fileFrame, bg=mainColor,
                                 text="X", fg=textColor, anchor=N, command=lambda: removeItem(self.index))
        self.removeFile.grid(column=6, row=0, pady=10)


def isDuplicate():  # Checks for duplicate files in files array and asks users for permission
    selectedFiles = filedialog.askopenfilenames(initialdir="/", title="Select Files",
                                                filetypes=(("PDF", "*.pdf"), ("All Files", "*.*")))
    for file in selectedFiles:
        if file in files:
            fileName = file[file.rfind("/")+1:]
            title = "Duplicate Files Detected!"
            content = f'Duplicate File detected \n Do you still want to include {fileName} in the merged result?'
            response = messagebox.askyesno(title, content)

            if(response == 1):
                addFile(file)
        else:
            addFile(file)


def addFile(file):  # Adds a file to files array and file name to frame
    addFrameItem = FrameItem(file, len(files))
    files.append(file)


def refreshFrameItems():  # Refreshes list of files if the order is changed or files are deleted

    for widget in frame.winfo_children():
        widget.destroy()

        index = 0

    for file in files:
        addFrameItem = FrameItem(file, index)
        index += 1


def convertFiles():  # Makes use of PyPDF library to merge selected files in files array
    merger = PdfFileMerger()

    if len(files) > 1:  # Check if more than one file is selected
        for file in files:
            merger.append(file)
            mergedFilePath = destAddress.get() + f'{mergedFileInput.get()}.pdf'

        # Check if same file already exists in the same directory
        if not os.path.exists(mergedFilePath):
            try:
                merger.write(mergedFilePath)

            except Exception as err:
                title = "Error!!!"
                content = err
                messagebox.showerror(title, content)

            merger.close()    # Close  merger before file deletion to avoid PermissionError
            title = "Merge Success!!!"
            content = f"The files have been successfully merged as {mergedFileInput.get()}.pdf\n Please check the result in {mergedFilePath}"
            messagebox.showinfo(title, content)
            deleteFiles()

        else:
            title = "File already exists!"
            content = "A file with the same name already exists in this directory \n Please select another name and try again"
            messagebox.showerror(title, content)

    else:
        title = "Insufficient Data!"
        content = "Please select more than one file"
        messagebox.showerror(title, content)


def changePath():  # Allows the user to choose the directory in which the merged file is stored
    mergedFilePath = filedialog.askdirectory(
        initialdir="/", title="Select Destination Folder")
    destAddress.config(state=NORMAL)
    destAddress.delete(0, END)
    destAddress.insert(0, f"{mergedFilePath}/")
    destAddress.config(state=DISABLED)


def deleteFiles():  # deletes files after merging if checkbox is selected
    if varCheck.get() == 1:
        title = "Delete Files!"
        content = "Are you sure that you want to delete the individual files that were used for merging?"
        response = messagebox.askyesno(title, content)

        if response == 1:
            for file in files:
                fileName = file[file.rfind("/")+1:]
                try:
                    os.remove(file)

                except PermissionError as err:
                    title = "Delete Error"
                    content = f" {fileName} file could not be deleted.\n Please make sure that the file is not being used before deletion."
                    messagebox.showerror(title, content)

                except Exception as err:
                    title = "Delete Error"
                    content = err
                    messagebox.showerror(title, content)

            clearFiles()


def moveItemUp(index):  # Move a file up in the list when the up arrow button is clicked
    if index > 0:
        tmp = files[index]
        files[index] = files[index-1]
        files[index-1] = tmp

        refreshFrameItems()


def moveItemDown(index):  # Move a file down in the list when the down arrow button is clicked
    if index < len(files) - 1:
        tmp = files[index]
        files[index] = files[index+1]
        files[index+1] = tmp

        refreshFrameItems()


def removeItem(index):  # Remove an item from the list when the delete(X) button is pressed
    removed = files.pop(index)
    refreshFrameItems()


def clearFiles():  # Clears all files from the array and frame
    for widget in frame.winfo_children():
        widget.destroy()
    files.clear()


frame = Frame(root, bg=frameColor, width=560, height=400)
frame.grid_propagate(0)
frame.grid(row=0, column=0, padx=30, pady=30, columnspan=6, rowspan=6)

destAddress_label = Label(
    root, text="Destination Address:", bg=mainColor, fg=textColor)
destAddress_label.grid(row=7, column=0)

destAddress = Entry(root, width=50)
destAddress.grid(row=7, column=1, columnspan=3)
destAddress.insert(0, destination)
destAddress.config(state=DISABLED)

mergedFile_label = Label(
    root, text="New file name:", bg=mainColor, fg=textColor)
mergedFile_label.grid(row=8, column=0)

mergedFileInput = Entry(root, width=50)
mergedFileInput.grid(row=8, column=1, columnspan=3)
mergedFileInput.insert(0, mergedFileName)

fileFormatLabel = Label(root, bg=mainColor, fg=textColor,
                        text=".pdf")
fileFormatLabel.grid(row=8, column=4)

findPath = Button(root, bg=mainColor, fg=textColor,
                  text="...", command=changePath)
findPath.grid(row=7, column=4)

varCheck = IntVar()
deleteBox = Checkbutton(
    root, text="Delete files after merging", bg=mainColor, fg=checkBoxColor, variable=varCheck)
deleteBox.deselect()
deleteBox.grid(row=9, column=0)

openFile = Button(root, text="Open File", padx=10, pady=5, width=10,
                  bg=mainColor, fg=textColor, command=isDuplicate)
openFile.grid(row=7, column=5)

convertFiles = Button(root, text="Convert Files", fg=textColor, width=10,
                      bg=mainColor, padx=10, pady=5, command=convertFiles)
convertFiles.grid(row=8, column=5, pady=15)

clear = Button(root, text="Clear", padx=10, pady=5, width=10,
               bg=mainColor, fg=textColor, command=clearFiles)
clear.grid(row=9, column=5)

root.mainloop()

# Features
# Grid
# file duplication
# change destination
# custom file name
# delete files
# File merged message
# Exceptions: Invalid File Names(Same file in same directory, Null name), File paths(Adding ".","/","\")
# PermissionError
# Order of files
# design

# Scroll Bars
# Last 5 saved locations in selection menu
# Position in Center
