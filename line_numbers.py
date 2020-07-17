import tkinter as tk

class LineNumbers(tk.Text):
	def __init__(self, master, text_widget,**kwargs):
		super().__init__(master, **kwargs)

		self.text_widget = text_widget
		self.text_widget.bind('<KeyPress>', self.on_key_press)

		self.insert(1.0, '1')
		self.configure(state='disabled')

	def on_key_press(self, event=None):
		final_index = str(self.text_widget.index(tk.END))
		line_num = final_index.split('.')[0]
		line_numbers = '\n'.join( str(no + 1) for no in range(int(line_num)))

		line_width = len(str(line_num))
		self.configure(state="normal", width=line_width)
		self.delete(1.0, tk.END)
		self.insert(1.0, line_numbers)
		self.configure(state = "disabled")


#if __name__ == "__main__":
#	w = tk.Tk()
#	t = tk.Text(w)
#	l = LineNumbers(w,t,width=1)
#	l.pack(side=tk.LEFT)
#	t.pack(side=tk.LEFT, expand=1,fill=tk.BOTH)
#	w.mainloop()
