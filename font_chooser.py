import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import  families

class FontChooser(tk.Toplevel):
	def __init__(self, master, **kwargs):
		super().__init__(**kwargs)
		self.master = master

		self.transient(self.master)
		self.geometry("500x200")
		self.title("Font")

		self.configure(bg=self.master.background)

		self.font_list = tk.Listbox(self, exportselection=False)
		self.available_fonts = sorted(families())
		self.master.font_family = self.available_fonts[0]
		for family in self.available_fonts:
			self.font_list.insert(tk.END, family)
		current_selection_index = self.available_fonts.index(self.master.font_family)
		if current_selection_index:
			self.font_list.select_set(current_selection_index)
			self.font_list.see(current_selection_index)

		self.size_input = tk.Spinbox(self, from_=5, to=99, value=self.master.font_size)

		self.save_button = ttk.Button(self, text="Save", command= self.save, style="editor.TButton")
		self.cancel_button = ttk.Button(self, text="Cancel", command=self.destroy, style="editor.TButton")

		self.cancel_button.pack(side = tk.BOTTOM, fill=tk.X, expand=1, padx=50)
		self.save_button.pack(side=tk.BOTTOM, fill=tk.X, expand=1,  padx=50)
		self.font_list.pack(side=tk.LEFT, fill=tk.Y, expand=1)
		self.size_input.pack(side=tk.RIGHT, fill=tk.X, expand=1, padx=50)


	def save(self):
		font_family = self.font_list.get(self.font_list.curselection()[0])
		font_size = self.size_input.get()
		with open('font.txt', 'w') as file:
			file.write("")
		with open('font.txt', 'a') as file:
			for c,f in ["family",font_family],["size",font_size]:
				file.write(c+":"+f+"\n")
		self.master.update_font()

