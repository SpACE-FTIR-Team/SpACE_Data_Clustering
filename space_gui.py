import tkinter as tk
import tkinter.messagebox as tkmb

def launch_gui():
	root = tk.Tk()
	app = SpaceApp(master = root)
	app.mainloop()

class SpaceApp(tk.Frame):
	"""A tkinter GUI-based app for SpACE."""

	def __init__(self, master):
		"""Set up the root window and instantiate the main frame."""
		super().__init__(master)
		self.master = master
		self.master.title("SpACE v.0.0.1")
		self.grid()

		# attach handler for exiting the program
		self.master.protocol("WM_DELETE_WINDOW", self._on_close)

		self._create_widgets()

	def _create_widgets(self):
		"""Create and configure all the widgets in the main frame."""
		# data
		self._LabelFrame_data = tk.LabelFrame(self, text = "Data")
		self._Label_data_text = tk.Label(self._LabelFrame_data, text = "Input folder:")
		self._Entry_folder = tk.Entry(self._LabelFrame_data, width = 30)
		self._Button_browse = tk.Button(self._LabelFrame_data, text = "Browse...", command = self._on_browse)
		self._Label_data_text.grid(row = 0, column = 0, padx = (5,0), sticky = tk.W)
		self._Entry_folder.grid(row = 1, column = 0, padx = (5,0), sticky = tk.W)
		self._Button_browse.grid(row  = 1, column = 1, padx = 5)
		self._LabelFrame_data.grid(padx = (10,0), pady = (5,0))

	def _quick_message_box(self, text):
		"""A quick and dirty messagebox for showing simple output for debugging."""
		tkmb.showinfo("Message", text)

	def _on_browse(self):
		self._quick_message_box("Congrats, you clicked the Browse button.")

	def _on_close(self):
		self.master.destroy()