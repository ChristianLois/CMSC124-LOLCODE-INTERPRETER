from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename      # for choosing file
from tkinter import ttk                 #for tables of lexemes and symbols
from tkinter import messagebox

from Lexer import Lexer
from Parser import Parser
from SymbolAnalyzer import SymbolAnalyzer

import tkinter.font as tkfont

def openFile():        #for opening file
    fp = askopenfilename(
        filetypes=[("LOL CODE Files", "*.lol"), ("All Files", "*.*")]
    )
    if not fp:
        return
    txt_edit.delete(1.0, END)
    with open(fp, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(END, text)
    window.title(f"Text Editor Application - {fp}")

def saveFile():        #for saving file
    fp = asksaveasfilename(
        defaultextension="lol",
        filetypes=[("LOL CODE Files", "*.lol"), ("All Files", "*.*")],
    )
    if not fp:
        return
    with open(fp, "w") as output_file:
        text = txt_edit.get(1.0, END)
        output_file.write(text)
    window.title(f"Text Editor Application - {fp}")

def execute():
    global txt_edit

    lex = Lexer(txt_edit.get("1.0",'end-1c'))

    lexemes = lex.tokenize()

    lexemeTable.delete(*lexemeTable.get_children())     #reset lexeme table

    symbolTree = None

    if (len(lexemes) > 0):
        parser = Parser(lexemes)
        symbolTree = parser.lolProgram()

    # for i in symbolTree.children_nodes:
    #     print(i.type)
    
    # if(symbolTree):
    #     symbolAnalyer = SymbolAnalyzer(symbolTree)
    #     codeExecution = symbolAnalyer.analyze()

    if isinstance(lexemes,str):         #catch if error
        messagebox.showinfo("Error",lexemes)
    else:
        for lex in lexemes:         #insert values
            if lex.type != 'Linebreak':
                lexemeTable.insert(parent='', index='end', values=(lex.value, lex.type))
    
            

window = Tk()
window.title("LOL CODE Interpreter")
window.configure(background = "gray")
window.geometry("1200x700")

#labels
label1 = Label(window, text = "LEXEMES", background = "gray")
label2 = Label(window, text = "SYMBOL TABLE", background = "gray")

#text editor
txt_edit = Text(window, height=18, width=53)
font = tkfont.Font(font=txt_edit['font'])
tab = font.measure('    ')
txt_edit.config(tabs=tab)
fr_buttons = Frame(window, relief=RAISED, bd=2)
btn_open = Button(fr_buttons, text="Open", command=openFile, height=1)
btn_save = Button(fr_buttons, text="Save As...", command=saveFile)

executeButton = Button(window, text="Execute", command=execute)
executeButton.place(x=500, y=313)

btn_open.grid(row=0, column=0, sticky="ew")
btn_save.grid(row=0, column=1, sticky="ew")

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=1, column=0, sticky="nsew")

#lexemes
lexemeTable = ttk.Treeview(window, height=13)

lexemeTable['column'] = ("Lexeme", "Classification")
lexemeTable.column("#0", width=0, stretch=NO)
lexemeTable.column("Lexeme", anchor=W, width=180)
lexemeTable.column("Classification", anchor=W, width=180)
lexemeTable.heading("#0", text="", anchor=W)
lexemeTable.heading("Lexeme", text="Lexeme", anchor=W)
lexemeTable.heading("Classification", text="Classification", anchor=W)

#symbols
symbolTable = ttk.Treeview(window, height=13)

symbolTable['column'] = ("Identifier", "Value")
symbolTable.column("#0", width=0, stretch=NO)
symbolTable.column("Identifier", anchor=W, width=180)
symbolTable.column("Value", anchor=W, width=180)
symbolTable.heading("#0", text="", anchor=W)
symbolTable.heading("Identifier", text="Identifier", anchor=W)
symbolTable.heading("Value", text="Value", anchor=W)

#listbox for execution
execBox = Listbox(window, height = 22, width = 190)

#placing to gui
lexemeTable.place(x = 430, y = 28)
symbolTable.place(x = 800, y = 28)
execBox.place(x = 5, y = 340)

label1.place(x = 580, y = 3)    #lexemes label
label2.place(x = 930, y = 3)    #symbol table label

mainloop()