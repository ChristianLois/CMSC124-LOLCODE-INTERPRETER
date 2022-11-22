from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename      # for choosing file
from tkinter import ttk                 #for tables of lexemes and symbols
from tkinter import messagebox

from Lexer import Lexer
from Parser import Parser
from SymbolAnalyzer import SymbolAnalyzer

import tkinter.font as tkfont

def openFile():        #for opening file
    global label3
    fp = askopenfilename(
        filetypes=[("LOL CODE Files", "*.lol"), ("All Files", "*.*")]
    )
    if not fp:
        return
    txt_edit.delete(1.0, END)
    label3.config(text = fp)
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
    global txt_edit, stdin, stdout

    lex = Lexer(txt_edit.get("1.0",'end-1c'))

    lexemes = lex.tokenize()

    lexemeTable.delete(*lexemeTable.get_children())     #reset lexeme table
    symbolTable.delete(*symbolTable.get_children()) 

    symbolTree = None

    stdout.delete('1.0', 'end')

    if (len(lexemes) > 0):
        parser = Parser(lexemes)
        symbolTree = parser.lolProgram()
    
    for lex in lexemes:         #insert values
        if (lex.type != 'Linebreak' and
            lex.type != 'Comment' and
            lex.type != 'Comment Delimiter' and 
            lex.type != 'EOF' and 
            lex.type != 'Multiline Comment' and
            lex.type != 'Multiline Comment Start' and
            lex.type != 'Multiline Comment End'):
            lexemeTable.insert(parent='', index='end', values=(lex.value, lex.type))  
    
    if(symbolTree):
        inputs = stdin.get("1.0",'end-1c').split('\n')
        symbolAnalyer = SymbolAnalyzer(symbolTree, stdin = inputs)
        symbols, output = symbolAnalyer.analyze()
    
    for symbol in symbols.keys():         #insert values
        symbolTable.insert(parent='', index='end', values=(symbol, symbols[symbol].value))  
    
    if len(output) > 0:
        stdout.insert(END, output)

window = Tk()
window.title("LOL CODE Interpreter")
window.configure(background = "gray")
window.geometry("1200x655")

#labels

label1 = Label(window, text = "LEXEMES", background = "white")
label2 = Label(window, text = "SYMBOL TABLE", background = "white")
label3 = Label(window, text = 'No file opened', background = "white")
label4 = Label(window, text = 'STDIN', background = "white")

#text editor
txt_edit = Text(window, height=16, width=80)
font = tkfont.Font(font=txt_edit['font'])
tab = font.measure('    ')
txt_edit.config(tabs=tab)

btn_open = Button(text="Open", command=openFile, height=1, background = 'lightgrey', fg = 'black')
btn_save = Button(text="Save As...", command=saveFile, background = 'lightgrey', fg = 'black')

executeButton = Button(window, text="Execute", command=execute, width = 91, background = 'lightgrey', fg = 'black')
executeButton.place(x=20, y=313)

btn_open.place(x = 560, y = 10)
btn_save.place(x = 605, y = 10)

txt_edit.place(x = 20, y = 40)

#lexemes
lexemeTable = ttk.Treeview(window, height=14)

lexemeTable['column'] = ("Lexeme", "Classification")
lexemeTable.column("#0", width=0, stretch=NO)
lexemeTable.column("Lexeme", anchor=W, width=123)
lexemeTable.column("Classification", anchor=W, width=123)
lexemeTable.heading("#0", text="", anchor=W)
lexemeTable.heading("Lexeme", text="Lexeme", anchor=W)
lexemeTable.heading("Classification", text="Classification", anchor=W)

#symbols
symbolTable = ttk.Treeview(window, height=14)

symbolTable['column'] = ("Identifier", "Value")
symbolTable.column("#0", width=0, stretch=NO)
symbolTable.column("Identifier", anchor=W, width=123)
symbolTable.column("Value", anchor=W, width=123)
symbolTable.heading("#0", text="", anchor=W)
symbolTable.heading("Identifier", text="Identifier", anchor=W)
symbolTable.heading("Value", text="Value", anchor=W)

#listbox for execution
stdout = Text(window, height = 18, width = 112)

stdin = Text(window, height=17, width=30)
font = tkfont.Font(font=stdin['font'])
tab = font.measure('    ')
stdin.config(tabs=tab)

#placing to gui
lexemeTable.place(x = 675, y = 28)
symbolTable.place(x = 935, y = 28)
stdout.place(x = 20, y = 350)
stdin.place(x = 935, y = 366)

label1.place(x = 769, y = 3)    #lexemes label
label2.place(x = 1015, y = 3)    #symbol table label
label3.place(x = 20, y = 10)    #symbol table label
label4.place(x = 1035, y= 340)

mainloop()