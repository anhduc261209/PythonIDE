from tkinter import *
from tkinter import filedialog
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator
import os
#initalize
root = Tk()
root.title('PythonIDE')
root.iconbitmap('ico.ico')
root.geometry("1200x660")
#Set variable for open filename
global open_status_name, selected
open_status_name, selected = False, False
#create new file function
def new_file():
    my_text.delete("1.0", END)
    #Update file
    root.title('New File - PythonIDE')
    status_bar.config(text="New file        ")
    open_status_name = False
#Create new file function
def open_file():
    #delete previous text
    my_text.delete("1.0", END)
    #Grab filename
    text_file = filedialog.askopenfilename(initialdir="/", title="Open File", filetypes=(("Normal Text Files", "*.txt"), ("HTML files", "*.html"), ("CSS Files", "*.css"), ("JavaScript Files", "*.js"), ("Python Files", "*.py"), ("C++ File", "*cpp"), ("C Files", "*.c"), ("Java Files", "*.java"), ("Go files", "*.go"), ("PHP Files", "*.php"), ("C# Files", ".cs"), ("TypeScript Files", "*.ts"), ("Ruby Files", "*.rb"), ("Swift Files", "*.swift"), ("Visual Basic Files", "*.vb"), ("Pascal Files", ".pas"), ("Objective-C Files", "*.mm"), ("All Files", "*")))
    #Check if there is a file name
    if text_file:
        #Make Filename glbbal
        global open_status_name
        open_status_name = text_file
    #update status bar
    name = text_file
    status_bar.config(text=str(name))
    root.title(str(name) + " - PythonIDE")
    #open files
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    #Add file to textbox
    my_text.insert(END, stuff)
    #close opened file
    text_file.close()
#Create Save As file function
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="/", title="Save File", filetypes=(("Normal Text Files", "*.txt"), ("HTML files", "*.html"), ("CSS Files", "*.css"), ("JavaScript Files", "*.js"), ("Python Files", "*.py"), ("C++ File", "*cpp"), ("C Files", "*.c"), ("Java Files", "*.java"), ("Go files", "*.go"), ("PHP Files", "*.php"), ("C# Files", ".cs"), ("TypeScript Files", "*.ts"), ("Ruby Files", "*.rb"), ("Swift Files", "*.swift"), ("Visual Basic Files", "*.vb"), ("Pascal Files", ".pas"), ("Objective-C Files", "*.mm"), ("All Files", "*")))
    if text_file:
        #update status bar
        name = text_file
        status_bar.config(text="Saved: "+str(name))
        root.title(str(name) + " - PythonIDE")
        #Save the file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        #Close the files
        text_file.close()
#Save file
def save_file():
    global open_status_name
    if open_status_name:
        #Save the file
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        #Close the files
        text_file.close()
        #Status update or popup code
        status_bar.config(text="Saved: "+str(open_status_name))
    else:
        save_as_file()
#cut text
def cut_text(e):
    global selected
    #Check if keyboard shortcut
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            #Grab selected text from text box
            selected = my_text.selection_get()
            #Delete selected text from text textbox
            my_text.delete("sel.first", "sel.last")
            #Clear the clipboard and append to the clipboard
            root.clipboard_clear()
            root.clipboard_append(selected)
    #copy text
def copy_text(e):
    global selected
    #Check if we used keyboard shortcut
    if e:
        selected = root.clipboard_get()
    if my_text.selection_get():
        #Grab selected text from text box
        selected = my_text.selection_get()
        #Clear the clipboard and append to the clipboard
        root.clipboard_clear()
        root.clipboard_append(selected)
#paste text
def paste_text(e):
    global selected
    #Check if keyboard shortcut
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            pos = my_text.index(INSERT)
            my_text.insert(pos, selected)
def runCode():
    code = my_text.get('1.0', END)
    exec(code)
    
def openTerminal():
    os.system('cls')

cdg = ColorDelegator()
cdg.tagdefs['MYGROUP'] = {'foreground': '#ff5555', 'background': '#282a36'}

# These five lines are optional. If omitted, default colours are used.
cdg.tagdefs['COMMENT'] = {'foreground': '#6272a4', 'background': '#282a36'}
cdg.tagdefs['KEYWORD'] = {'foreground': '#50fa7b', 'background': '#282a36'}
cdg.tagdefs['BUILTIN'] = {'foreground': '#ff79c6', 'background': '#282a36'}
cdg.tagdefs['STRING'] = {'foreground': '#f1fa8c', 'background': '#282a36'}
cdg.tagdefs['DEFINITION'] = {'foreground': '#8be9fd', 'background': '#282a36'}
#Create main frame
my_frame = Frame(root)
my_frame.pack(pady=5)
#Create scroll bar for text box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT,fill=Y)
#create text box
global my_text
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set)
my_text["bg"] = "#282a36"
my_text["fg"] = "#f8f8f2"
my_text.config(insertbackground='white')
my_text.pack()
Percolator(my_text).insertfilter(cdg)
#Configure Scrollbar
text_scroll.config(command=my_text.yview)
#Create menu
my_menu = Menu(root)
root.config(menu=my_menu)
#Add file menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit PythonIDE", command=root.quit)
#Add the edit menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut     Ctrl+X", command=lambda:cut_text(False))
edit_menu.add_command(label="Copy    Ctrl+X", command=lambda:copy_text(False))
edit_menu.add_command(label="Paste   Ctrl+V", command=lambda:paste_text(False))
edit_menu.add_command(label="Undo", command=my_text.edit_undo)
edit_menu.add_command(label="Redo", command=my_text.edit_redo)
command_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Command", menu=command_menu)
command_menu.add_command(label="Run", command=runCode)
command_menu.add_command(label="Open Terminal", command=openTerminal)
#Add status bar to bottom of app
status_bar = Label(root, text="Ready        ", anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)
#Edit binding
root.bind('<Control-x>', cut_text)
root.bind('<Control-c>', copy_text)
root.bind('<Control-v>', paste_text)
root.mainloop()
