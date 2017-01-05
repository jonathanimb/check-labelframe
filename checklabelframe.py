#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

try:
	import ttk
	import Tkinter as tk
except:
	import tkinter as tk
	from tkinter import ttk

class CheckLabelFrame(ttk.LabelFrame):
	"""A tkinter LabelFrame that includes a checkbutton to enable or disable
	the entire frame"""
	def __init__(self, master=None, text="", *args, **kwargs):
		self.enabled = tk.IntVar(master, True)
		self.enabled.trace('w', lambda *args: self.update_enable(self))
		cb = ttk.Checkbutton(master, variable=self.enabled, text=text)
		ttk.LabelFrame.__init__(self, master, labelwidget=cb, *args, **kwargs)

	def update_enable(self, target):
		for child in target.children.values():
			try:
				if self.enabled.get():
					# when enableing, check if child is in another CheckLabelFrame
					if isinstance(child.master, CheckLabelFrame):
					#~ if hasattr(child.master, 'enabled'):
						if child.master.enabled.get():
							child.config(state=tk.NORMAL)
					else:
						child.config(state=tk.NORMAL)
				else:
					child.config(state=tk.DISABLED)
			except tk.TclError:
				#probably because the child is a Frame, so try to change it's children too
				if hasattr(child, 'children'):
					self.update_enable(target=child)


def main():
	# an example

	root = tk.Tk()

	win = CheckLabelFrame(root, text='Frame1')
	ttk.Button(win, text='test').pack()
	ttk.Checkbutton(win, text="another option").pack()
	ttk.Label(win, text='important data label').pack()
	ttk.Button(win, text='test').pack()

	h = tk.Frame(win)
	ttk.Label(h, text='subframe label').pack()
	ttk.Button(h, text='sbuframe btn').pack()
	h.pack()

	l = CheckLabelFrame(win, text='nested')
	ttk.Button(l, text='test').grid(row=0, column=0)
	ttk.Button(l, text='test').grid(row=0, column=1)
	l.pack()
	win.pack(expand=True, fill=tk.BOTH)
	def disable(*args):
		win.enabled.set(False)
	def enable(*args):
		win.enabled.set(True)
	def toggle(*args):
		win.enabled.set(not win.enabled.get())

	win2 = CheckLabelFrame(root, text='Frame2')
	ttk.Button(win2, text='Disable Frame1', command=disable).pack()
	ttk.Button(win2, text='Enable Frame1', command=enable).pack()
	ttk.Button(win2, text='Toggle Frame1', command=toggle).pack()
	win2.pack(expand=True, fill=tk.BOTH)

	root.mainloop()

if __name__ == '__main__':
	main()
