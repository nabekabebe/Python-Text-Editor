import tkinter as tk
import tkinter.ttk as ttk

from textarea import TextArea

class MainWindow(tk.Tk):
	def __init__(self):
		super().__init__()
		self.text_area = TextArea(self,bg="white",fg="black",undo=True)
		self.scrollbar = ttk.Scrollbar(orient="vertical",command=self.scroll_text)
		self.text_area.configure(yscrollcommand = self.scrollbar.set)

		self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
		self.text_area.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1 )

	def scroll_text(self, *args):
		self.text_area.yview_moveto(args[1])

if __name__ == '__main__':
	MainWindow().mainloop()
