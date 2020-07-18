import tkinter as tk
import tkinter.ttk as ttk

class FindWindow(tk.Toplevel):
	def __init__(self, master, **kwargs):
		super().__init__(**kwargs)
		self.master = master
		self.geometry("350x100")
		self.title("Find and Replace")
		self.text_to_find = tk.StringVar()
		self.text_to_replace_with = tk.StringVar()

		top_frame = tk.Frame(self)
		middle_frame = tk.Frame(self)
		bottom_frame = tk.Frame(self)

		find_entry_label = tk.Label(top_frame, text = "Find: ")
		self.find_entry = ttk.Entry(top_frame,width=25, textvar=self.text_to_find)
		replace_entry_label = tk.Label(middle_frame, text="Replace with: ")
		self.replace_entry=ttk.Entry(middle_frame,width=25, textvar=self.text_to_replace_with)

		self.find_button = ttk.Button(bottom_frame, text="Find", command=self.on_find)
		self.replace = ttk.Button(bottom_frame, text="Replace", command=self.on_replace)
		self.cancel_button = ttk.Button(bottom_frame, text="Cancel", command=self.on_cancel)

		top_frame.pack(padx=20, fill=tk.X, pady=10)
		find_entry_label.pack(side=tk.LEFT)
		self.find_entry.pack(side=tk.RIGHT)

		middle_frame.pack(padx=20, fill=tk.X, pady=5)
		replace_entry_label.pack(side=tk.LEFT)
		self.replace_entry.pack(side=tk.RIGHT)

		bottom_frame.pack(padx=20, fill=tk.X, pady=10)
		self.find_button.pack(side=tk.LEFT, padx=10)
		self.replace.pack(side=tk.LEFT,padx=10)
		self.cancel_button.pack(side=tk.LEFT, padx=10)

	def on_find(self):
		self.master.find(self.text_to_find.get())

	def on_replace(self):
		self.master.replace_text(self.text_to_find.get(), self.text_to_replace_with.get())

	def on_cancel(self):
		self.master.cancel_find_window()
		self.destroy()

#if __name__ == "__main__":
#	mw = tk.Tk()
#	fw = FindWindow(mw)
#	mw.mainloop()
