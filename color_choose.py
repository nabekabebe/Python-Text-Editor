import tkinter as tk
import tkinter.ttk as ttk
from tkinter.colorchooser import  askcolor
import json

class ChooseColor(tk.Toplevel):
	def __init__(self, master, **kwargs):
		super().__init__(**kwargs)
		self.master = master
		self.transient(self.master)
		self.geometry('400x300')
		self.title('Color Scheme')
		self.configure(bg=self.master.background)
		self.configure_ttk_elements()

		self.chosen_bg_color = tk.StringVar()
		self.chosen_fg_color = tk.StringVar()
		self.chosen_text_bg_color = tk.StringVar()
		self.chosen_text_fg_color = tk.StringVar()

		self.chosen_bg_color.set(self.master.background)
		self.chosen_fg_color.set(self.master.foreground)
		self.chosen_text_bg_color.set(self.master.text_background)
		self.chosen_text_fg_color.set(self.master.text_foreground)

		window_frame = tk.Frame(self, bg=self.master.background)
		window_fg_frame = tk.Frame(window_frame, bg=self.master.background)
		window_bg_frame = tk.Frame(window_frame, bg=self.master.background)

		window_label = ttk.Label(window_frame, text="Window:", anchor=tk.W, style="editor.TLabel")
		fg_label = ttk.Label(window_fg_frame, text="Foreground:", anchor=tk.E, style="editor.TLabel")
		bg_label = ttk.Label(window_bg_frame, text="Background:", anchor=tk.E, style="editor.TLabel")

		fg_color_chooser = ttk.Button(window_fg_frame, text="  Change FG color   ", style="editor.TButton", command= lambda c=self.chosen_fg_color: self.set_color(c))
		bg_color_chooser = ttk.Button(window_bg_frame, text="  Change BG color   ", style="editor.TButton", command= lambda c=self.chosen_bg_color: self.set_color(c))

		fg_color_preview = ttk.Label(window_fg_frame, textvar=self.chosen_fg_color)
		bg_color_preview = ttk.Label(window_bg_frame, textvar=self.chosen_bg_color)

		window_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
		window_label.pack(side=tk.TOP, fill=tk.X)
		window_fg_frame.pack(side=tk.TOP, fill=tk.X, expand=1, pady=8)
		window_bg_frame.pack(side=tk.TOP, fill=tk.X, expand=1, pady=8)

		fg_label.pack(side=tk.LEFT,fill=tk.X,padx=(20,20))
		fg_color_chooser.pack(side=tk.LEFT, padx = (15,0))
		fg_color_preview.pack(side=tk.RIGHT, fill=tk.X,expand=1, padx=(15, 5))
		bg_label.pack(side=tk.LEFT, fill=tk.X, padx=(20,20))
		bg_color_chooser.pack(side=tk.LEFT, padx=(15,0))
		bg_color_preview.pack(side=tk.RIGHT, fill=tk.X,expand=1, padx=(15, 5))

		text_frame = tk.Frame(self, bg=self.master.background)
		text_fg_frame = tk.Frame(text_frame, bg=self.master.background)
		text_bg_frame = tk.Frame(text_frame, bg=self.master.background)

		text_label = ttk.Label(text_frame, text="Editor:", anchor=tk.W, style="editor.TLabel")
		text_fg_label = ttk.Label(text_fg_frame, text="Foreground:", anchor=tk.E, style="editor.TLabel")
		text_bg_label = ttk.Label(text_bg_frame, text="Background:", anchor=tk.E, style="editor.TLabel")

		text_fg_color_chooser = ttk.Button(text_fg_frame, text="Change Text FG color", style="editor.TButton", command= lambda c=self.chosen_text_fg_color: self.set_color(c))
		text_bg_color_chooser = ttk.Button(text_bg_frame, text="Change Text BG color", style="editor.TButton", command= lambda c=self.chosen_text_bg_color: self.set_color(c))

		text_fg_color_preview = ttk.Label(text_fg_frame, textvar=self.chosen_text_fg_color)
		text_bg_color_preview = ttk.Label(text_bg_frame, textvar=self.chosen_text_bg_color)

		text_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
		text_label.pack(side=tk.TOP, fill=tk.X)
		text_fg_frame.pack(side=tk.TOP, fill=tk.X, expand=1, pady=8)
		text_bg_frame.pack(side=tk.TOP, fill=tk.X, expand=1, pady=8)

		text_fg_label.pack(side=tk.LEFT,fill=tk.X,padx=(20,20))
		text_fg_color_chooser.pack(side=tk.LEFT, padx=(15,0))
		text_fg_color_preview.pack(side=tk.RIGHT, expand=1, fill=tk.X, padx=(15, 5))
		text_bg_label.pack(side=tk.LEFT, fill=tk.X, padx=(20, 20))
		text_bg_color_chooser.pack(side=tk.LEFT, padx=(15,0))
		text_bg_color_preview.pack(side=tk.RIGHT, expand=1, fill=tk.X, padx=(15, 5))

		save_button = ttk.Button(self, text="save", command=self.save, style="editor.TButton")
		save_button.pack(side=tk.BOTTOM, pady=(0, 20))

		self.all_frames = [window_frame, window_fg_frame, window_bg_frame, text_frame, text_fg_frame, text_bg_frame]

	def save(self):
		scheme_color = {
		"fg":self.chosen_fg_color.get(),
		"bg":self.chosen_bg_color.get(),
		"tfg":self.chosen_text_fg_color.get(),
		"tbg":self.chosen_text_bg_color.get()
		}
		with open('scheme_color.json', 'w') as scheme:
			scheme.write(json.dumps(scheme_color))

		self.master.apply_color_scheme(self.chosen_fg_color.get(),
		self.chosen_bg_color.get(),
		self.chosen_text_fg_color.get(),
		self.chosen_text_bg_color.get())

		for frame in self.all_frames:
			frame.configure(bg=self.chosen_bg_color.get())
		self.configure(bg=self.chosen_bg_color.get())
		self.configure_ttk_elements()

	def configure_ttk_elements(self):
		style = ttk.Style()
		style.configure('editor.TLabel', foreground=self.master.foreground, background=self.master.background)
		style.configure('editor.TButton', foreground=self.master.foreground, background=self.master.background)



	def set_color(self, sv):
		choice_color = askcolor()[1]
		sv.set(choice_color)


"""
if __name__ == "__main__":
	w = tk.Tk()
	w.background = "grey"
	w.foreground="red"
	w.text_background="grey"
	w.text_foreground="black"
	c = ChooseColor(w)
	w.mainloop()
"""
