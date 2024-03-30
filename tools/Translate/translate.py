import tkinter as tk
import shutil
import sys
import os

window = tk.Tk()
window.title("Markdown 与 Html 转译")
window.geometry('800x600')

frame1 = tk.Frame(window)
frame1.grid(row=1, column=0, sticky='w')
tk.Label(frame1, text = '输入文件').pack(side='left')

frame0 = tk.Frame(window)
frame0.grid(row=0, column=0, sticky='w')
tk.Label(frame0, text = '文件名称').pack(side='left')
filename = tk.Text(frame0, width=20, height=1)
filename.pack()
filename.window_create("insert")

frame2 = tk.Frame(window)
frame2.grid(row=2, column=0, sticky='w')
tk.Label(frame2, text = '').pack(side='left')
inputfile = tk.Text(frame2, width=40, height=40)
inputfile.pack()
inputfile.window_create("insert")

def clear():
	cur = os.path.dirname(__file__)
	inputPath = os.path.join(cur, 'input')
	outputPath = os.path.join(cur, 'output')
	shutil.rmtree(inputPath)
	os.mkdir(inputPath)
	shutil.rmtree(outputPath)
	os.mkdir(outputPath)

def writeIn():
	# 把内容写入文件
	fname = filename.get("1.0", "end")
	code = inputfile.get("1.0", "end")
	fnameWithoutLast = fname[0: len(fname) - 1]
	cur = os.path.dirname(__file__)
	inputPath = os.path.join(cur, 'input')
	Cfile = open(os.path.join(inputPath, fnameWithoutLast), "w", encoding='utf-8')
	Cfile.write(code)

def translate():
	os.system('python3 AddProblem.py')

frame3 = tk.Frame(window)
frame3.grid(row=0, column=1, sticky='w')
tk.Label(frame3, text = '转译').pack(side='left')
tk.Button(frame3, text="清空", command=clear).pack(side='left')
tk.Button(frame3, text="写入", command=writeIn).pack(side='left')
tk.Button(frame3, text="翻译", command=translate).pack(side='left')
window.mainloop()