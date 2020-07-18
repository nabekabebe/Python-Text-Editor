import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

from text_highlighter import Highlighter
from textarea import TextArea
from line_numbers import LineNumbers
from findwindow import FindWindow

class MainWindow(tk.Tk):
	def __init__(self):
		super().__init__()
		self.text_area = TextArea(self,bg="white",fg="black",undo=True)
		self.scrollbar = ttk.Scrollbar(orient="vertical",command=self.scroll_text)
		self.text_area.configure(yscrollcommand = self.scrollbar.set)

		self.menu = tk.Menu(self, bg="lightgrey", fg="black")
		submenu_items = ["file", "edit", "tools", "help"]
		self.generate_sub_menus(submenu_items)
		self.configure(menu=self.menu)

		self.right_click_menu = tk.Menu(self, bg="lightgrey", fg="black", tearoff=0)
		self.right_click_menu.add_command(label='Cut', command=self.edit_cut)
		self.right_click_menu.add_command(label='Copy', command=self.edit_copy)
		self.right_click_menu.add_command(label='Paste', command=self.edit_paste)

		self.line_numbers = LineNumbers(self, self.text_area, width=1, bg="black", fg="cyan")
		#self.line_numbers = tk.Text(self, bg="black", fg="white")
		#first_100_numbers = [str(n) for n in range(1,101)]
		#self.line_numbers.insert(1.0,"\n".join(first_100_numbers))
		#self.line_numbers.configure(state="disabled", width=3,yscrollcommand=self.scrollbar.set)

		self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
		self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
		self.text_area.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1 )
		self.bind_events()
		self.highlight = Highlighter(self.text_area)

	def generate_sub_menus(self, submenu_items):
		window_methods = [ method_name for method_name in dir(self) if callable(getattr(self, method_name))]
		tkinter_methods = [ method_name for method_name in dir(tk.Tk) if callable(getattr(tk.Tk, method_name))]

		my_methods = [method for method in set(window_methods) - set(tkinter_methods)]
		my_methods = sorted(my_methods)

		for item in submenu_items:
			sub_menu = tk.Menu(self.menu, tearoff=0, bg="lightgrey", fg="black")
			matching_methods = []
			for method in my_methods:
				if method.startswith(item):
					matching_methods.append(method)
			for match in matching_methods:
				actual_method = getattr(self, match)
				method_shortcut = actual_method.__doc__
				friendly_name = ' '.join(match.split('_')[1:])
				sub_menu.add_command(label=friendly_name.title(), command=actual_method, accelerator=method_shortcut)
			self.menu.add_cascade(label=item.title(), menu=sub_menu)

	def scroll_text(self, *args):
		if len(args) > 1:
			self.text_area.yview_moveto(args[1])
			self.line_numbers.yview_moveto(args[1])
		else:
			event = args[0]
			if event.delta:
				move = -1 * (event.delta / 120)
			else:
				if event.num == 5:
					move=1
				else:
					move=-1
			self.text_area.yview_scroll(int(move), "units")
			self.line_numbers.yview_scroll(int(move), "units")

	def bind_events(self):
		self.text_area.bind("<MouseWheel>", self.scroll_text)
		self.text_area.bind("<Button-4>", self.scroll_text)
		self.text_area.bind("<Button-5>", self.scroll_text)

		self.line_numbers.bind("<MouseWheel>", lambda e: "break")
		self.line_numbers.bind("<Button-4>", lambda e: "break")
		self.line_numbers.bind("<Button-5>", lambda e: "break")
		self.bind('<Control-f>', self.show_find_window)

		self.text_area.bind('<Button-3>', self.show_right_click_menu)

	def edit_cut(self, event=None):
		#ctrl + x
		self.text_area.event_generate("<Control-x>")
		self.line_numbers.force_update()

	def edit_paste(self, event=None):
		"""Ctrl+V"""
		self.text_area.event_generate("<Control-v>")
		self.line_numbers.force_update()
		self.highlight.force_highlight()
	def edit_copy(self, event=None):
		"""Ctrl+C"""
		self.text_area.event_generate("<Control-c>")

	def show_right_click_menu(self, event=None):
		x = self.winfo_x() +  event.x
		y = self.winfo_y() +  event.y

		self.right_click_menu.post(x,y)

	def show_find_window(self, event = None):
		FindWindow(self.text_area)

if __name__ == '__main__':
	MainWindow().mainloop()
