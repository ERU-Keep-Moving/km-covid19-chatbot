import agirlikTest
import time
import sys
from tkinter import *


def send(a):
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)
    print(msg)
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "\nYou: " + msg + '\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 10))

        res = agirlikTest.chat(msg)
        ChatLog.insert(END, "Bot: " + res + '\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

        EntryBox.mark_set("insert", "1.1")

    if agirlikTest.cikisDurumu(agirlikTest.cevapListesi) or msg.lower() == "kapat":
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "\n\n\nUygulamayı kullandığınız için teşekkürler!")
        ChatLog.config(state=DISABLED)
        EntryBox.config(state=DISABLED)


def startPos():
    agirlikTest.reset()
    ChatLog.config(state=NORMAL)
    ChatLog.delete(0.0,END)
    ChatLog.insert(END,
                   "Chatbot ile konuşmaya başlayabilirsiniz ('kapat' yazarak çıkabilir ve sonucunuzu öğrenebilirsiniz.)!"'\n\n')
    ChatLog.insert(END,
                   "Şikayetiniz(varsa) sırayla yazabilirsiniz. Vermiş olduğunuz bilgilere göre covid19 risk durumunuz hesaplanacaktır."'\n\n')
    ChatLog.config(foreground="#442265", font=("Verdana", 10))
    ChatLog.config(state=DISABLED)
    EntryBox.config(state=NORMAL)
    

base = Tk()
base.title("Keep Moving")
base.geometry("510x520")
base.resizable(width=FALSE, height=FALSE)
base.configure(background='lightgray')
base.iconphoto(False, PhotoImage(file='images/logo.png'))

ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial", )
ChatLog.config(state=DISABLED)

scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

EntryBox = Text(base, bd=2, bg="white", width="29", height="5", font="Arial")
EntryBox.bind("<Return>", send)

var = StringVar()
var.set("Mesajınızı yazdıktan sonra ENTER tuşuna basınız!\nYeniden başlamak için buraya tıklayabilirsiniz.")
Label = Label(base, textvariable=var, relief=RAISED)
Label.bind("<Button-1>",lambda e,startPos=startPos:startPos())


scrollbar.place(x=476, y=6, height=356)
ChatLog.place(x=6, y=6, height=356, width=470)
EntryBox.place(x=6, y=370, height=80, width=487)
Label.place(x=6, y=460, height=50, width=487)


startPos()

base.mainloop()
