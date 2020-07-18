import tkinter as tk
import tkinter.messagebox as msgbox

class TextArea(tk.Text):
	def __init__(self, master, **kwargs):
		super().__init__(**kwargs)
		self.bind_events()
		self.master = master
		self.config(wrap=tk.WORD)

		self.tag_configure('find_match', background="yellow")
		self.find_match_index = None
		self.find_search_starting_index = 1.0

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
		return "break"
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

	def find(self, text_to_find):
		length = tk.IntVar()
		idx = self.search(text_to_find, self.find_search_starting_index, tk.END, count=length)
		if idx:
			self.tag_remove('find_match', 1.0, tk.END)
			end = f"{idx}+{length.get()}c"
			self.tag_add('find_match',idx,end)
			self.see(idx)

			self.find_search_starting_index = end
			self.find_match_index = idx
		else:
			if self.find_match_index != 1.0:
				if msgbox.askyesno("No More result","No further matches, Repeat from beginning?"):
					self.find_search_starting_index = 1.0
					self.find_match_index = None
					return self.find(text_to_find)
				else:
					self.find_search_starting_index = 1.0
					self.find_match_index = None
					self.tag_remove('find_match', 1.0, tk.END)
			else:
				msgbox.showinfo("No Matches","There is no result.")

	def replace_text(self, target, replacement):
		if self.find_match_index:
			end = f"{self.find_match_index}+{len(target)}c"
			self.replace(self.find_match_index, end, replacement)

			self.find_search_starting_index = f"{self.find_match_index}linestart"
			self.find_match_index = None

	def cancel_find_window(self):
		self.find_search_starting_index = 1.0
		self.find_match_index = None
		self.tag_remove('find_match', 1.0, tk.END)
