import tkinter as tk
import tkinter.messagebox as tkmb
import space_kmeans
import space_random_data

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
		self._Frame_options = tk.Frame(self)
		# data widgets
		self._LabelFrame_data = tk.LabelFrame(self._Frame_options, text = "Data")
		# -- input sub-frame --
		self._Frame_input = tk.Frame(self._LabelFrame_data)
		self._Label_data_text = tk.Label(self._Frame_input, text = "Input folder:")
		self._Entry_folder = tk.Entry(self._Frame_input, width = 30)
		self._Button_browse = tk.Button(self._Frame_input, text = "Browse...", command = self._on_browse)
		self._Label_data_text.grid(row = 0, column = 0, padx = (0,0), sticky = tk.W)
		self._Entry_folder.grid(row = 1, column = 0, padx = (5,0), sticky = tk.W)
		self._Button_browse.grid(row = 1, column = 1, padx = 5)
		self._Frame_input.grid(row = 0, sticky = tk.W)
		# -- normalize is by itself, no sub-frame --
		self._Var_normalize = tk.IntVar()
		self._Checkbutton_normalize = tk.Checkbutton(self._LabelFrame_data, text = "Normalize data during import", variable = self._Var_normalize)
		self._Checkbutton_normalize.grid(row = 1, sticky = tk.W)
		# -- pca sub-frame --
		self._Frame_pca = tk.Frame(self._LabelFrame_data)
		self._Var_pca = tk.IntVar()
		self._Checkbutton_pca = tk.Checkbutton(self._Frame_pca, text = "Perform PCA", variable = self._Var_pca)
		self._Label_pca_text = tk.Label(self._Frame_pca, text = "Number of dimensions:")
		self._Entry_pca = tk.Entry(self._Frame_pca, width = 5)
		self._Checkbutton_pca.grid(row = 0, sticky = tk.W)
		self._Label_pca_text.grid(row = 1, column = 0, sticky = tk.W)
		self._Entry_pca.grid(row = 1, column = 1)
		self._Frame_pca.grid(row = 2, pady = (0,5), sticky = tk.W)
		# data widgets grid
		self._LabelFrame_data.grid(row = 0, column = 0, padx = (10,0), pady = (5,0))

		# kmeans widgets
		self._LabelFrame_kmeans = tk.LabelFrame(self._Frame_options, text = "K-means algorithm")
		self._Var_kmeans = tk.BooleanVar()
		self._Var_kmeans_clusters = tk.IntVar()
		self._Checkbutton_kmeans = tk.Checkbutton(self._LabelFrame_kmeans, text = "Perform K-means", variable = self._Var_kmeans)
		self._Checkbutton_kmeans.grid(row = 0, sticky = tk.W)
		self._Label_k = tk.Label(self._LabelFrame_kmeans, text = "Number of clusters (k):")
		self._Entry_k = tk.Entry(self._LabelFrame_kmeans, width = 5, textvariable = self._Var_kmeans_clusters)
		self._Label_k.grid(row = 1, column = 0, pady = (0,5), sticky = tk.W)
		self._Entry_k.grid(row = 1, column = 1, pady = (0,5))
		# kmeans grid
		self._LabelFrame_kmeans.grid(row = 1, column = 0, padx = (10,0), pady = (30,0), sticky = tk.EW)

		# dbscan widgets
		self._LabelFrame_dbscan = tk.LabelFrame(self._Frame_options, text = "DBSCAN algorithm")
		self._Var_dbscan = tk.IntVar()
		self._Checkbutton_dbscan = tk.Checkbutton(self._LabelFrame_dbscan, text = "Perform DBSCAN", variable = self._Var_dbscan)
		self._Checkbutton_dbscan.grid(row = 0, sticky = tk.W)
		# -- dbscan parameters sub-frame --
		self._Frame_dbscan_parameters = tk.Frame(self._LabelFrame_dbscan)
		self._Label_eps = tk.Label(self._Frame_dbscan_parameters, text = "epsilon:")
		self._Entry_eps = tk.Entry(self._Frame_dbscan_parameters, width = 5)
		self._Label_eps.grid(row = 0, column = 0, sticky = tk.E)
		self._Entry_eps.grid(row = 0, column = 1, sticky = tk.W)
		self._Label_minpts = tk.Label(self._Frame_dbscan_parameters, text = "MinPts:")
		self._Entry_minpts = tk.Entry(self._Frame_dbscan_parameters, width = 5)
		self._Label_minpts.grid(row = 1, column = 0, sticky = tk.E)
		self._Entry_minpts.grid(row = 1, column = 1, sticky = tk.W)
		self._Frame_dbscan_parameters.grid(row = 1, pady = (0, 5), sticky = tk.W)
		# dbscan grid
		self._LabelFrame_dbscan.grid(row = 2, column = 0, padx = (10,0), pady = (5,0), sticky = tk.EW)

		# action buttons
		self._Frame_action_buttons = tk.Frame(self._Frame_options)
		self._Button_go = tk.Button(self._Frame_action_buttons, text = "Go", width = 15, command = self._on_go)
		self._Button_save = tk.Button(self._Frame_action_buttons, text = "Save", width = 15, command = self._on_save, state = "disabled")
		self._Button_go.grid(pady = 10)
		self._Button_save.grid(pady = 10)
		self._Frame_action_buttons.grid(row = 3, column = 0, pady = 30)

		self._Frame_options.grid(row = 0, column = 0, sticky = tk.N)

		# canvas is a placeholder for visualization
		self._Frame_canvas = tk.Frame(self)
		self._Canvas_visualization = tk.Canvas(self._Frame_canvas, width = 600, height = 600, bg = "blue")
		self._Canvas_visualization.grid()
		self._Frame_canvas.grid(row = 0, column = 1, padx = 10, pady = 10)

	def _quick_message_box(self, text):
		"""A quick and dirty messagebox for showing simple output for debugging."""
		tkmb.showinfo("Message", text)

	def _on_browse(self):
		self._quick_message_box("Congrats, you clicked the Browse button.")

	def _on_go(self):
		self._quick_message_box("Congrats, you clicked the Go button.")
		if self._Var_kmeans.get():
			space_kmeans.do_Kmeans(self._Var_kmeans_clusters.get(), space_random_data.generateRandomData(1000))
	
	def _on_save(self):
		self._quick_message_box("Congrats, you clicked the Save button.")

	def _on_close(self):
		self.master.destroy()