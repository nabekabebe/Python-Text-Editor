import tkinter as tk

class LineNumbers(tk.Text):
	def __init__(self, master, text_widget,**kwargs):
		super().__init__(master, **kwargs)

		self.text_widget = text_widget


		self.insert(1.0, '1')
		self.configure(state='disabled', font=(master.font_family, master.font_size))

		self.text_widget.bind('<Control-v>', self.get_cursor_index)
		self.text_widget.bind('<KeyPress>', self.on_key_press)
		self.on_key_press()

	def get_cursor_index(self, event=None):
		index = str(self.text_widget.index(tk.INSERT)).split('.')[0]
		return index

	def on_key_press(self, event=None):
		final_index = str(self.text_widget.index(tk.END))
		line_num = final_index.split('.')[0]
		if int( self.get_cursor_index(event=None)) > int(line_num):
			line_numbers = self.get_cursor_index(event=None)
		line_numbers = '\n'.join( str(no + 1) for no in range(int(line_num)))

		line_width = len(str(line_num))
		self.configure(state="normal", width=line_width)
		self.delete(1.0, tk.END)
		self.insert(1.0, line_numbers)
		self.configure(state = "disabled")
		self.see(str(self.text_widget.index(tk.INSERT)))

	def force_update(self):
		self.on_key_press()
		self.configure(bg=self.master.background, fg=self.master.foreground)


#if __name__ == "__main__":
#	w = tk.Tk()
#	t = tk.Text(w)
#	l = LineNumbers(w,t,width=1)
#	l.pack(side=tk.LEFT)
#	t.pack(side=tk.LEFT, expand=1,fill=tk.BOTH)
#	w.mainloop()
