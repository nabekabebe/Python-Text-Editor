import tkinter as tk

class TextArea(tk.Text):
	def __init__(self, master, **kwargs):
		super().__init__(**kwargs)
		self.bind_events()
		self.master = master
		self.config(wrap=tk.WORD)
	def bind_events(self):
		self.bind("<Control-a>",self.select_all)
		self.bind("<Control-c>", self.copy)
		self.bind("<Control-v>", self.paste)
		self.bind("<Control-x>", self.cut)
		self.bind("<Control-y>", self.redo)
		self.bind("<Control-z>", self.undo)

	def copy(self, event=None):
		self.event_generate("<<Control-c>>")
	def paste(self, event=None):
		self.event_generate("<<Control-v>>")
	def cut(self, event=None):
		self.event_generate("<<Control-x>>")
	def redo(self, event=None):
		self.event_generate("<<Control-y>>")
		return "break"
	def undo(self, event=None):
		self.event_generate("<<Control-z>>")
		return "break"
	def select_all(self, event=None):
		self.tag_add("sel", 1.0, tk.END)
		return "break"

