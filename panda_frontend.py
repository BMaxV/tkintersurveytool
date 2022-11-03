# this requires panda.
# also optionally, my UI helper package.

import sys

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from panda3d.core import LVecBase4f

from panda_interface_glue import panda_interface_glue

import surveytypes

class Wrapper:    
    def __init__(self):
        # Showbase is required for panda
        self.b = ShowBase()
        self.elements=[]
        
        self.core = surveytypes.App("test_question.txt")
        q=self.core.load_next_question()
        self.build_question_window(q)
    
    def clear(self):
        # deletes panda elemets. You could also change the values,
        # but I already have a build function and it's pretty quick anyway.
        for x in self.elements:
            x.removeNode()
        
    
    def load_next_question(self,*args):
        value=self.current_answer
        answer = self.core.get_save_answer(value)
        q=self.core.load_next_question()
        
        self.clear()
        self.build_question_window(q)
        
            
    def set_radio_option(self,index,args):
        
        # maybe set that one to a color or something.
        self.current_answer=index
        for aindex in self.radio_options:
            self.radio_options[aindex].setColor(LVecBase4f(0.8,0.8,0.8,1))
        self.radio_options[index].setColor(LVecBase4f(0.6,0.6,0.8,1))
    
    def quit(self,*args):
        sys.exit()
    
    def build_question_window(self,question):
        op_dict={}
        op_dict["scale"]=0.05
        diffx=0.3
        #done_button=panda_interface_glue.create_button("set"(2*diffx,0,0.2),op_dict["scale"],print,("this",))
        dy=0
        index=0
        
        if question==None:
            q_text=panda_interface_glue.create_textline("all done",(0,0,0.2))
            done_button=panda_interface_glue.create_button("quit",(0,0,0.1-dy*(index)),op_dict["scale"],self.quit,(1,))
        
        else:
            q_text=panda_interface_glue.create_textline(question.question_text,(0,0,0.2))
            
            #question text
            self.elements.append(q_text)
            self.radio_options={}
            
            for option in question.option_list:
                #build my radiobutton
                option_button=panda_interface_glue.create_button("set",(2*diffx,0,0.1-dy*(index)),op_dict["scale"],self.set_radio_option,(index,))
                option_text=panda_interface_glue.create_textline(option,(0,0,0.1-dy*(index)))
                self.radio_options[index]=option_text
                self.elements.append(option_button)
                self.elements.append(option_text)
                
                dy+=0.1
                index+=1
                a=1
        
            done_button=panda_interface_glue.create_button("done",(0,0,0.1-dy*(index)),op_dict["scale"],self.load_next_question,(1,))
            self.elements.append(done_button)
            

def main():
    W = Wrapper()
    while True:
        W.b.taskMgr.step()
        
    
if __name__ == "__main__":
    main()

