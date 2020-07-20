import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as msgbox

from text_highlighter import Highlighter
from textarea import TextArea
from line_numbers import LineNumbers
from findwindow import FindWindow
from font_chooser import FontChooser
from color_choose import ChooseColor
import json

class MainWindow(tk.Tk):
	def __init__(self):
		super().__init__()

		self.background = "lightgrey"
		self.foreground = "black"
		self.text_background = "white"
		self.text_foreground = "black"
		self.update_scheme()

		self.text_area = TextArea(self,bg=self.text_background, fg=self.text_foreground, undo=True)
		self.scrollbar = ttk.Scrollbar(orient="vertical",command=self.scroll_text)
		self.text_area.configure(yscrollcommand = self.scrollbar.set)

		self.font_family = None
		self.font_size = 20
		self.update_font()

		self.menu = tk.Menu(self, bg=self.background, fg=self.foreground)
		submenu_items = ["file", "edit", "tools", "help"]

		self.right_click_menu = tk.Menu(self, bg=self.background, fg=self.foreground, tearoff=0)
		self.right_click_menu.add_command(label='Cut', command=self.edit_cut)
		self.right_click_menu.add_command(label='Copy', command=self.edit_copy)
		self.right_click_menu.add_command(label='Paste', command=self.edit_paste)

		self.line_numbers = LineNumbers(self, self.text_area, width=2, bg=self.background, fg=self.foreground)
		#self.line_numbers = tk.Text(self, bg="black", fg="white")
		#first_100_numbers = [str(n) for n in range(1,101)]
		#self.line_numbers.insert(1.0,"\n".join(first_100_numbers))
		#self.line_numbers.configure(state="disabled", width=3,yscrollcommand=self.scrollbar.set)

		self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
		self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
		self.text_area.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1 )
		self.bind_events()
		self.highlight = Highlighter(self.text_area, 'highlight_config.json')

		self.all_menus = [self.menu, self.right_click_menu]

		self.generate_sub_menus(submenu_items)
		self.configure(menu=self.menu)

		self.open_file = None

	def generate_sub_menus(self, submenu_items):
		window_methods = [ method_name for method_name in dir(self) if callable(getattr(self, method_name))]
		tkinter_methods = [ method_name for method_name in dir(tk.Tk) if callable(getattr(tk.Tk, method_name))]

		my_methods = [method for method in set(window_methods) - set(tkinter_methods)]
		my_methods = sorted(my_methods)

		for item in submenu_items:
			sub_menu = tk.Menu(self.menu, tearoff=0, bg=self.background, fg=self.foreground)
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
			self.all_menus.append(sub_menu)

	def apply_color_scheme(self,fgc,bgc,text_fgc,text_bgc):
		self.background = bgc
		self.foreground = fgc
		self.text_background = text_bgc
		self.text_foreground = text_fgc

		self.text_area.configure(bg=text_bgc, fg=text_fgc)

		for menu in self.all_menus:
			menu.configure(bg=self.background, fg=self.foreground)

		self.line_numbers.force_update()

	def configure_ttk_elements(self):
		style = ttk.Style()
		style.configure('editor.TLabel', foreground=self.foreground, background=self.background)
		style.configure('editor.TButton', foreground=self.foreground, background=self.background)

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

		self.bind('<Control-n>', self.file_new)
		self.bind('<Control-o>', self.file_open)
		self.bind('<Control-s>', self.file_save)
		self.bind('<Control-h>', self.help_about)
		#self.bind('<Control-m>', self.tools_change_syntax_highlighting)
		self.bind('<Control-g>', self.tools_change_color_scheme)
		self.bind('<Control-l>', self.tools_change_font)

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

	def edit_select_all(self, event=None):
		#ctrl +a
		self.text_area.event_generate("<Control-a>")

	def edit_find_and_replace(self, event=None):
		#ctrl + f
		self.show_find_window()

	def file_open(self, event=None):
		#ctrl+o
		file_to_open = filedialog.askopenfilename()
		if file_to_open:
			self.open_file = file_to_open
			self.text_area.display_file_contents(file_to_open)
			self.line_numbers.force_update()
			self.highlight.force_highlight()

	def file_save(self, event=None):
		#ctrl + s
		current_file = self.open_file if self.open_file else None
		if not current_file:
			current_file = filedialog.asksaveasfilename()
		if current_file:
			contents = self.text_area.get(1.0, tk.END)
			with open(current_file, 'w') as file:
				file.write(contents)

	def file_new(self, event=None):
		#ctrl + n
		self.text_area.delete(1.0, tk.END)
		self.open_file = None
		self.line_numbers.force_update()

	def show_find_window(self, event = None):
		FindWindow(self.text_area)

	def update_font(self):
		self.load_font_file('font.txt')
		self.text_area.configure(font = (self.font_family, self.font_size))

	def load_font_file(self, file_path):
		with open(file_path, 'r') as stream:
			try:
				font_family = stream.readline().split(':')[1].strip()
				font_size = stream.readline().split(':')[1].strip()
			except Exception as e:
				print(e)
				return

		self.font_family = font_family
		self.font_size = font_size
		if self.font_family is None:
			self.font_family = "clean"

	def update_scheme(self):
		with open('scheme_color.json', 'r') as stream:
			scheme = json.loads(stream.read())
			self.background = scheme['bg']
			self.foreground = scheme['fg']
			self.text_foreground = scheme['tfg']
			self.text_background = scheme['tbg']

	def change_font(self):
		FontChooser(self)

	def tools_change_font(self, event=None):
		#ctrl+l
		self.change_font()

	def tools_change_color_scheme(self, event=None):
		#ctrl + g
		self.change_color_scheme()
	def change_color_scheme(self):
		self.scheme_color = ChooseColor(self)

	def show_about_page(self):
		msgbox.showinfo("About", "Niko Text Editor: developed by Nabek Abebe, python 3 Tkinter")

	def help_about(self, event=None):
		#ctrl + h
		self.show_about_page()

if __name__ == '__main__':
	MainWindow().mainloop()
