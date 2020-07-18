import tkinter as tk
from highlight_config import lang_config

class Highlighter:
	def __init__(self, text_widget):
		self.text_widget = text_widget
		self.config = lang_config
		self.categories = self.config['category']
		self.numbers_color = self.config['numbers']['color']
		self.strings_color = self.config['strings']['color']
		self.configure_tags()
		#self.keywords = ["True","False","def","for","while","import","if","elif","else"]
		self.disallowed_previous_chars = ["_","-","."]

		#self.tag_configure('keyword', foreground=self.keywords_color)
		#self.tag_configure('number', foreground=self.numbers_color)
		self.text_widget.bind('<KeyRelease>',self.on_key_release)
		#self.text_widget.pack(fill=tk.BOTH,expand=1)

	def on_key_release(self, event=None):
		self.highlight()

	def highlight_regex(self, regexp, tag):
		length = tk.IntVar()
		start = 1.0
		idx = self.text_widget.search(regexp, start,tk.END, regexp=1, count=length)
		while idx:
			end = f"{idx}+{length.get()}c"
			self.text_widget.tag_add(tag, idx, end)
			start = end
			idx = self.text_widget.search(regexp,start,tk.END,regexp=1,count=length)

	def configure_tags(self):
		for category in self.categories.keys():
			color = self.categories[category]['color']
			self.text_widget.tag_configure(category, foreground=color)
		self.text_widget.tag_configure("number", foreground=self.numbers_color)
		self.text_widget.tag_configure("string", foreground=self.strings_color)
		self.text_widget.tag_configure("parenthesis", foreground=self.config['parenthesis']['color'])
	def highlight(self, event=None):
		length = tk.IntVar()
		for category in self.categories:
			matches = self.categories[category]['matches']
			for keyword in matches:
				start = 1.0
				keyword = keyword + "[^A-Za-z_-]"
				idx = self.text_widget.search(keyword, start, tk.END, count=length, regexp = 1)
				while idx:
					char_match_found = int(str(idx).split('.')[1])
					line_match_found = int(str(idx).split('.')[0])
					if char_match_found > 0:
						previous_char_index = str(line_match_found) + '.' + str(char_match_found - 1)
						previous_char = self.text_widget.get(previous_char_index, previous_char_index + "+1c")
						if previous_char.isalnum() or previous_char in self.disallowed_previous_chars:
							end = f"{idx}+{length.get()-1}c"
							start = end
							idx = self.text_widget.search(keyword, start, tk.END, regexp=1)
						else:
							end = f"{idx}+{length.get() - 1}c"
							self.text_widget.tag_add(category, idx, end)
							start = end
							idx =  self.text_widget.search(keyword, start, tk.END, regexp=1)
					else:
						end = f"{idx}+{length.get() - 1}c"
						self.text_widget.tag_add(category, idx, end)
						start = end
						idx = self.text_widget.search(keyword, start, tk.END, regexp=1)
				self.highlight_regex(r"(\d)+[.]?(\d)*", "number")
				self.highlight_regex(r"[\'][^\']*[\']", "string")
				self.highlight_regex(r"[\"][^\']*[\"]", "string")
				self.highlight_regex(r"\(.*\)", "parenthesis")

	def force_highlight(self):
		self.highlight()
#if __name__ == "__main__":
#	w = tk.Tk()
#	h = Highlighter(tk.Text(w))
#	w.mainloop()
