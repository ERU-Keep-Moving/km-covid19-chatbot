import agirlikTest
import time
import sys

#Creating GUI with tkinter
from tkinter import *

isQuit=False

   
def send(a):
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    print(msg)
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "\nYou: " + msg + '\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 10 ))
    
        res = agirlikTest.chat(msg)
        ChatLog.insert(END, "Bot: " + res + '\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        
        EntryBox.mark_set("insert", "1.1")
           
        
def startPos():
    ChatLog.config(state=NORMAL)
    ChatLog.insert(END, "Chatbot ile konuşmaya başlayabilirsiniz (quit yazarak çıkabilir ve sonucunuzu öğrenebilirsiniz.)!"'\n\n')
    ChatLog.insert(END, "Şikayetiniz(varsa) sırayla yazabilirsiniz. Vermiş olduğunuz bilgilere göre covid19 risk durumunuz hesaplanacaktır."'\n\n')
    ChatLog.config(foreground="#442265", font=("Verdana", 10 ))
    ChatLog.config(state=DISABLED)


base = Tk()
base.title("Keep Moving")
base.geometry("500x500")
base.resizable(width=FALSE, height=FALSE)


ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)

scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

EntryBox = Text(base, bd=2, bg="white",width="29", height="5", font="Arial")
EntryBox.bind("<Return>", send)

var=StringVar()
var.set("Mesajınızı yazdıktan sonra ENTER tuşuna basınız!")
Label=Label( base, textvariable=var, relief=RAISED )

scrollbar.place(x=476,y=6, height=356)
ChatLog.place(x=6,y=6, height=356, width=470)
EntryBox.place(x=6, y=370, height=80, width=470)
Label.place(x=6,y=450,height=50,width=470)

startPos()


base.mainloop()


