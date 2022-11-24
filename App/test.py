from tkinter import *
root = Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
canv = Canvas(root, width=600, height=400, bg='#f0f0c0')
canv.grid(row=0, column=0, sticky=N+S+E+W)
root.mainloop()
