import tkinter as tk
import tensorflow as tf
import calendar

def Say_hello(cnt) :
    for i in range(cnt):
        print("Say hello")



s = "Life is short/n Use Pytohn"

root = tk.Tk()
t = tk.Text(root, height=2,width=len("Life is short"))
t.insert(tk.END, s)
t.pack()
tk.mainloop()