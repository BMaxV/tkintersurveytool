import tkinter 
from tkinter.filedialog import askopenfilename

import os

import surveytypes

class myApp:
    def __init__(self, question_fn=None):
        self.core = surveytypes.App(question_fn)
        
        
        
        self.root = tkinter.Tk()
        self.MenuBar = tkinter.Menu(self.root)
        self.FileMenu = tkinter.Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(label="File", menu=self.FileMenu)

        self.active_var = None

        width = 600
        height = 400
        # center the window
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()

        left = (screenWidth / 2) - (width / 2)
        top = (screenHeight / 2) - (height / 2)

        self.root.geometry('%dx%d+%d+%d' % (width, height, left, top))
        self.root.config(menu=self.MenuBar)

        self.root.title("Surveytool")
        self.FileMenu.add_command(label="Open", command=self.openFile)
               
        
        self.load_next_question()
        
    def run(self):
        self.root.mainloop()

    def openFile(self):

        self.filename = askopenfilename(
            defaultextension=".txt", filetypes=[
                ("All Files", "*.*"), ("Text Documents", "*.txt")])
        print(self.filename)
        if len(self.filename) == 0:
            self.filename = None
        else:
            # try to open the file
            # set the window title
            self.root.title(os.path.basename(self.filename) + "- Survey")
            
            with open(self.filename, "r") as f:
                text = f.read()
                
            self.core.questions+=surveytypes.load_questions_from_text(text)
            self.load_next_question()

    def build_question_window(self, question):
        #zero everything
        length = len(question.option_list)
        c = 0
        var = tkinter.IntVar()
        self.active_var = var
        self.active_stuff = []
        
        #this is the question
        w = tkinter.Label(self.root, text=question.question_text)
        w.pack()
        self.active_stuff.append(w)

        for option in question.option_list:
            # radiobutton
            w = tkinter.Radiobutton(
                self.root,
                text=option,
                variable=var,
                value=c,
            )
            
            w.pack()
            self.active_stuff.append(w)
            c += 1
        #another one for "other"
        w = tkinter.Radiobutton(
            self.root,
            text="other",
            variable=var,
            value=c,
        )
        w.pack()
        self.active_stuff.append(w)
        
        
        w = tkinter.Button(self.root, text="continue", command=self.done)
        w.pack()
        self.active_stuff.append(w)

    def done(self):
        value = self.active_var.get()
        answer = self.core.get_save_answer(value)
        
        #this deletes the UI elements for the current question
        for x in self.active_stuff:
            x.pack_forget()
        self.load_next_question()

    def load_next_question(self):
        q=self.core.load_next_question()
        if q!=None:
            self.build_question_window(q)
        else:
            w = tkinter.Label(self.root, text="all done")
            w.pack()
            self.active_stuff.append(w)
            

if __name__ == "__main__":
    M = myApp("test_question.txt")
    M.run()
