#
# Graphical user interface for SpACE
#

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
import tkinter.filedialog as tkfd
from time import sleep
import space_file_ops as fileops
import space_data_ops as dataops
import space_kmeans as km
import space_dbscan as db
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

def launch_gui(cnf):
    root = tk.Tk()
    app = SpaceApp(master=root, app_config=cnf)
    app.mainloop()


class SpaceApp(tk.Frame):
    """A tkinter GUI-based app for SpACE."""

    def __init__(self, master, app_config={}):
        """Set up the root window and instantiate the main frame."""
        super().__init__(master)
        self.master = master
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.app_config = app_config
        if app_config != {}:
            self.master.title("%s v. %s" %
                              (self.app_config.get("APP_NAME", 'Application'),
                               self.app_config.get("APP_VERSION", 'Unknown')))
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)

        # attach handler for exiting the program
        self.master.protocol("WM_DELETE_WINDOW", self._on_close)

        self._create_widgets()
        if app_config != {}:
            self._set_defaults()
        self.log("SpACE graphical user interface startup")

        # data objects holding pandas dataframes
        self._data_objs = []

    def _create_widgets(self):
        """Create and configure all the widgets in the main frame."""
        self.grid_columnconfigure(index=0, weight=0)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_rowconfigure(index=0, weight=1)

        # OPTIONS FRAME, left column
        self._Frame_options = ttk.Frame(self)

        # - DATA widgets -
        self._LabelFrame_data = ttk.LabelFrame(self._Frame_options, text="Data")
        # -- input sub-frame --
        self._Frame_input = ttk.Frame(self._LabelFrame_data)
        self._Label_data_text = ttk.Label(self._Frame_input, text="Input from folder:")
        self._Var_folder = tk.StringVar()
        self._Entry_folder = ttk.Entry(self._Frame_input, width=30, textvariable=self._Var_folder)
        self._Button_browse = ttk.Button(self._Frame_input, text="Browse...", command=self._on_browse)
        self._Label_data_text.grid(row=0, column=0, padx=(0, 0), sticky=tk.W)
        self._Entry_folder.grid(row=1, column=0, padx=(5, 0), sticky=tk.W)
        self._Button_browse.grid(row=1, column=1, padx=5)
        self._Frame_input.grid(row=0, sticky=tk.W)
        # -- normalize sub-frame --
        Frame_normalize = ttk.Frame(self._LabelFrame_data)
        Label_normalize = ttk.Label(Frame_normalize, text="Normalization:")
        self._Var_normalize = tk.StringVar()
        Combobox_normalize = ttk.Combobox(Frame_normalize, width=10, justify="center",
                                      state="readonly", textvariable=self._Var_normalize,
                                      values=list(dataops.NORMALIZATION_TYPES.keys()))
        Combobox_normalize.current(0)
        Label_normalize.grid(row=0, column=0, sticky=tk.W)
        Combobox_normalize.grid(row=0, column=1, sticky=tk.W)
        Frame_normalize.grid(row=1, pady=5, sticky=tk.W)
        # -- pca sub-frame --
        self._Frame_pca = ttk.Frame(self._LabelFrame_data)
        self._Var_pca = tk.BooleanVar()
        self._Var_pca_dimensions = tk.IntVar()
        self._Checkbutton_pca = ttk.Checkbutton(self._Frame_pca, text="Perform PCA", variable=self._Var_pca)
        self._Label_pca_text = ttk.Label(self._Frame_pca, text="Number of dimensions:")
        self._Entry_pca = ttk.Entry(self._Frame_pca, width=5, justify="center", textvariable=self._Var_pca_dimensions)
        self._Checkbutton_pca.grid(row=0, sticky=tk.W)
        self._Label_pca_text.grid(row=1, column=0, sticky=tk.W)
        self._Entry_pca.grid(row=1, column=1)
        self._Frame_pca.grid(row=2, pady=(0, 5), sticky=tk.W)
        # - DATA widgets grid -
        self._LabelFrame_data.grid(row=0, column=0, padx=(10, 0), pady=(5, 0))

        # - KMEANS widgets -
        self._LabelFrame_kmeans = ttk.LabelFrame(self._Frame_options, text="K-means algorithm")
        self._Var_kmeans = tk.BooleanVar()
        self._Var_kmeans_clusters = tk.IntVar()
        self._Checkbutton_kmeans = ttk.Checkbutton(self._LabelFrame_kmeans, text="Perform K-means",
                                                   variable=self._Var_kmeans)
        self._Checkbutton_kmeans.grid(row=0, sticky=tk.W)
        self._Label_k = ttk.Label(self._LabelFrame_kmeans, text="Number of clusters (k):")
        self._Entry_k = ttk.Entry(self._LabelFrame_kmeans, width=5, justify="center",
                                  textvariable=self._Var_kmeans_clusters)
        self._Label_k.grid(row=1, column=0, pady=(0, 5), sticky=tk.W)
        self._Entry_k.grid(row=1, column=1, pady=(0, 5))
        # - KMEANS widgets grid -
        self._LabelFrame_kmeans.grid(row=1, column=0, padx=(10, 0), pady=(30, 0), sticky=tk.EW)

        # - DBSCAN widgets -
        self._LabelFrame_dbscan = ttk.LabelFrame(self._Frame_options, text="DBSCAN algorithm")
        self._Var_dbscan = tk.BooleanVar()
        self._Checkbutton_dbscan = ttk.Checkbutton(self._LabelFrame_dbscan, text="Perform DBSCAN",
                                                   variable=self._Var_dbscan)
        self._Checkbutton_dbscan.grid(row=0, sticky=tk.W)
        # -- dbscan parameters sub-frame --
        self._Frame_dbscan_parameters = ttk.Frame(self._LabelFrame_dbscan)
        self._Var_eps = tk.DoubleVar()
        self._Var_minpts = tk.IntVar()
        self._Label_eps = ttk.Label(self._Frame_dbscan_parameters, text="epsilon:")
        self._Entry_eps = ttk.Entry(self._Frame_dbscan_parameters, width=5, justify="center",
                                    textvariable=self._Var_eps)
        self._Label_eps.grid(row=0, column=0, sticky=tk.E)
        self._Entry_eps.grid(row=0, column=1, sticky=tk.W)
        self._Label_minpts = ttk.Label(self._Frame_dbscan_parameters, text="MinPts:")
        self._Entry_minpts = ttk.Entry(self._Frame_dbscan_parameters, width=5, justify="center",
                                       textvariable=self._Var_minpts)
        self._Label_minpts.grid(row=1, column=0, sticky=tk.E)
        self._Entry_minpts.grid(row=1, column=1, sticky=tk.W)
        self._Frame_dbscan_parameters.grid(row=1, pady=(0, 5), sticky=tk.W)
        # - DBSCAN grid -
        self._LabelFrame_dbscan.grid(row=2, column=0, padx=(10, 0), pady=(5, 0), sticky=tk.EW)

        # - BUTTONS for actions -
        self._Frame_action_buttons = ttk.Frame(self._Frame_options)
        self._Button_go = ttk.Button(self._Frame_action_buttons, text="Go", width=15, command=self._on_go)
        self._Button_save = ttk.Button(self._Frame_action_buttons, text="Save", width=15, command=self._on_save,
                                       state="disabled")
        self._Button_go.grid(pady=10)
        self._Button_save.grid(pady=10)
        # - BUTTONS for actions grid -
        self._Frame_action_buttons.grid(row=3, column=0, pady=30)

        # end setup of OPTIONS FRAME, left column
        self._Frame_options.grid(row=0, column=0, sticky=tk.N)

        # NOTEBOOK (tabs), right column
        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=(10, 5))
        Notebook_controller = ttk.Notebook(self)
        # the tabs
        self._Tab_log = ttk.Frame(Notebook_controller)
        self._Tab_kmeans = ttk.Frame(Notebook_controller)
        self._Tab_dbscan = ttk.Frame(Notebook_controller)
        # rezise setup
        for tab in (self._Tab_log, self._Tab_kmeans, self._Tab_dbscan):
            tab.grid_columnconfigure(index=0, weight=1)
            tab.grid_rowconfigure(index=0, weight=1)
        Notebook_controller.add(self._Tab_log, text="Log")
        Notebook_controller.add(self._Tab_kmeans, text="K-means plot")
        Notebook_controller.add(self._Tab_dbscan, text="DBSCAN plot")
        # log text box and scrollbars
        self._Scroll_H = ttk.Scrollbar(self._Tab_log, orient=tk.HORIZONTAL)
        self._Scroll_V = ttk.Scrollbar(self._Tab_log, orient=tk.VERTICAL)
        self._Text_log = tk.Text(self._Tab_log, wrap=tk.NONE, width=78, height=32,
                                 xscrollcommand=self._Scroll_H.set,
                                 yscrollcommand=self._Scroll_V.set,
                                 bg="black", fg="gray")
        self._Scroll_H["command"] = self._Text_log.xview
        self._Scroll_V["command"] = self._Text_log.yview
        self._Text_log.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self._Scroll_H.grid(row=1, column=0, sticky=tk.E + tk.W)
        self._Scroll_V.grid(row=0, column=1, sticky=tk.N + tk.S)
        Button_clear_log = ttk.Button(self._Tab_log, text="Clear Log", width=15, command=self._on_clear_log)
        Button_clear_log.grid(row=2, columnspan=2, pady=5)
        # kmeans panel
        self._kmeans_viz_panel = VisualizationPanel(self._Tab_kmeans, self._on_generate_plot_kmeans)
        self._kmeans_viz_panel.get_frame_handle().grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self._kmeans_viz_panel.disable_widgets()
        # dbscan panel
        self._dbscan_viz_panel = VisualizationPanel(self._Tab_dbscan, self._on_generate_plot_dbscan)
        self._dbscan_viz_panel.get_frame_handle().grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self._dbscan_viz_panel.disable_widgets()

        # end setup of NOTEBOOK (tabs), right column
        Notebook_controller.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

    def _set_defaults(self):
        self._Var_folder.set(self.app_config["DEFAULT_INPUT_PATH"])
        self._Var_pca.set(self.app_config["PCA_BY_DEFAULT"])
        self._Var_pca_dimensions.set(self.app_config["DEFAULT_PCA_DIMENSIONS"])
        self._Var_kmeans_clusters.set(self.app_config["DEFAULT_KMEANS_K"])
        self._Var_eps.set(self.app_config["DEFAULT_DBSCAN_EPS"])
        self._Var_minpts.set(self.app_config["DEFAULT_DBSCAN_MINPTS"])

    def log(self, text):
        """A simple logging facility for status messages
        during program execution."""
        # Right now this just logs to the console.
        # Future expansion options:
        # a) simply turn this off prior to project submission
        # b) or perhaps save to a file
        # c) or perhaps output to a logging window that the user can
        #    see/hide as desired so they know what's going on
        self._Text_log.insert(tk.END, "%s\n" % text)
        self.master.update()

    def _quick_message_box(self, text):
        """A quick and dirty messagebox for showing simple output for debugging."""
        tkmb.showinfo("Message", text)

    def _validate_user_input(self):
        """Check for valid input from user in the following controls:
        - input folder entry
        - kmeans number of clusters k
        - dbscan epsilon
        - dbscan minpts
        Gives error message to user if anything is wrong.
        Returns True if no errors, false if any error."""
        self.log("-- Begin input validation --")
        # verify we have a good path in the input folder widget
        if not fileops.path_exists(self._Var_folder.get()):
            # a nonexistent path is a fatal error
            self.log("Invalid path: %s" % self._Var_folder.get())
            self._quick_message_box("Invalid path:\n%s" % self._Var_folder.get())
            return False
        # verify kmeans number of clusters
        if self._Var_kmeans.get():
            if self._Var_kmeans_clusters.get() < 2:
                # bad number of clusters is a fatal error
                self.log("Number of clusters for K-means must be at least 2.")
                self._quick_message_box("Number of clusters for K-means must be at least 2.")
                return False
        # verify dbscan epsilon and minpts
        if self._Var_dbscan.get():
            if self._Var_eps.get() < 0:
                # bad epsilon is a fatal error
                self.log("DBSCAN epsilon must be greater than zero.")
                self._quick_message_box("DBSCAN epsilon must be greater than zero.")
                return False
            if self._Var_minpts.get() < 3:
                # bad minpts is a fatal error
                self.log("DBSCAN MinPts must be at least 3.")
                self._quick_message_box("DBSCAN MinPts must be at least 3.")
                return False
        self.log("All user input OK.")
        self.log("-- End input validation --")
        return True

    def _on_browse(self):
        dir = tkfd.askdirectory(initialdir=self._Var_folder.get())
        # askdirectory returns '' if the user clicked cancel
        # so only update the folder path if the user actually selected something
        if dir != '':
            self.log("user: changed input folder to %s" % dir)
            self._Var_folder.set(dir)

    def _on_clear_log(self):
        self._Text_log.delete(1.0, tk.END)

    def _do_import_data(self):
        # reset everything, in case we are running multiple times
        self._data_objs = []
        self.log("-- Begin data import and pre-processing --")
        # search for all files in input folder and subfolder
        file_list = fileops.collect_all_filenames(self._Var_folder.get())
        self.log("Found %s files and folders in %s" % (len(file_list), self._Var_folder.get()))
        # filter by filename
        filtered_file_list = fileops.filter_filenames(file_list)
        self.log("Found %s files matching the filename filter criteria" % len(filtered_file_list))
        if len(filtered_file_list) == 0:
            # a empty path is a fatal error
            # log to console and pop up a messagebox
            self.log("No files found path: %s" % self._Var_folder.get())
            self._quick_message_box("No files found:\n%s" % self._Var_folder.get())
            return
        # parse
        self.log("Loading into data objects...")
        self._data_objs = dataops.file_to_data_object(filtered_file_list)
        self.log("Loaded %s data objects" % len(self._data_objs))
        # re-index the pairs dataframes
        self.log("Re-indexing pairs dataframes...")
        dataops.reindex(self._data_objs)
        # range check
        self.log("Calculating common range...")
        min, max = dataops.find_common_range(self._data_objs)
        if (min, max) == (None, None):
            # lack of a common range across files is a fatal error
            # log to console and pop up a messagebox
            self.log("No range in common!")
            self._quick_message_box("No range in common!")
            self._data_objs = []
            return
        else:
            self.log("All files have this wavelength range in common: %s to %s" % (min, max))
        # truncate to common range
        self.log("Truncating data to range %s to %s..." % (min, max))
        dataops.truncate(self._data_objs, min, max)
        # finds the index of the file with the highest resolution
        self.log("Finding highest resolution file...")
        max_res_index = dataops.find_max_res(self._data_objs)
        # align the pairs dataframes to dataframe with highest resolution
        self.log("Aligning the data...")
        dataops.align(self._data_objs, max_res_index)

        fileops.save_data_files(self._Var_folder.get(), "/align/", self._data_objs)

        # Normalization
        self.log("Normalizing data with method: %s" % self._Var_normalize.get())
        self._data_objs = dataops.NORMALIZATION_TYPES[self._Var_normalize.get()](self._data_objs)
        fileops.save_data_files(self._Var_folder.get(), "/normalized/", self._data_objs)

        # final, pre-processed dataset
        self._dataset = dataops.combine(self._data_objs)

        # PCA
        if self._Var_pca.get():
            self.log('Performing PCA to ' + str(self._Var_pca_dimensions.get()) + ' dimensions')
            self._dataset = dataops.pca(self._dataset, self._Var_pca_dimensions.get())
            self.log('PCA applied')

        self.log("-- End data import and pre-processing --")

    def _do_kmeans_clustering(self):
        self.log("-- Begin K-means clustering --")
        self.log("Clustering...")
        self._k_clusters = km.do_Kmeans(self._Var_kmeans_clusters.get(), self._dataset)
        self.log("Calculating cluster compositions...")
        composition = km.calculate_composition(self._k_clusters, self._Var_kmeans_clusters.get(), self._data_objs)
        self.log("(..temporary file save..)")
        fileops.save_kmeans_cluster_files(self._Var_folder.get(), "/kmeans_clustering/", self._k_clusters, composition)
        self.log("-- End K-means clustering --")
        # TODO: check the kmeans clustering succeeded before enabling plot widgets
        self._kmeans_viz_panel.enable_widgets()

    def _do_dbscan_clustering(self):
        # epsilon: self._Var_eps.get()
        # minpts: self._Var_minpts.get()
        self.log("-- Begin DBSCAN clustering --")
        self.log("Clustering...")
        self._db_clusters = db.do_dbscan(self._Var_eps.get(), self._Var_minpts.get(), self._dataset)
        self.log("Calculating cluster compositions...")
        
        self.log("-- End DBSCAN clustering --")
        # TODO: check the DBSSCAN clustering succeeded before enabling plot widgets
        self._dbscan_viz_panel.enable_widgets()

    def _on_go(self):
        # this might take a while, so disable the Go button and busy the cursor
        # while we do work
        self._Button_go.config(state="disabled")
        self.update()
        self.master.config(cursor="watch")
        sleep(.5)  # cursor is sometimes not updating without this delay
        self.master.update_idletasks()
        self.log("user: pressed Go button")

        # destroy any existing visualization and
        # disable visualization until we have new data
        for viz_panel in [self._kmeans_viz_panel, self._dbscan_viz_panel]:
            viz_panel.destroy_canvas()
            viz_panel.disable_widgets()
        if self._validate_user_input():
            # all input checks passed
            self._do_import_data()
            if self._Var_kmeans.get() and self._data_objs != []:
                self._do_kmeans_clustering()
            if self._Var_dbscan.get() and self._data_objs != []:
                self._do_dbscan_clustering()
            # re-enable the save button
            self._Button_save["state"] = "normal"
        else:
            # at least one input check failed
            pass  # this is here for possible future expansion

        # re-enable Go button and un-busy the cursor now that we're done
        self.master.config(cursor="")
        self._Button_go.config(state="normal")
        self.master.update()

    def _on_save(self):
        self._quick_message_box(
            "Congrats, you clicked the Save button.  This actuall does nothing now, but eventually might!")

    def _on_close(self):
        self.master.quit()
        self.master.destroy()

    def _on_generate_plot_kmeans(self):
        self.log("user: pressed Generate Plot button (K-means)")
        dimensions = self._kmeans_viz_panel.get_dimensions()
        self.log("-- Begin K-means plotting in %sD --" % dimensions)
        plot = km.plot2D if dimensions == 2 else km.plot3D
        self.log("PCA reducing cluster data to %s dimensions..." % dimensions)
        self._reduced_set = dataops.pca(self._dataset, dimensions)
        self.log("Plotting...")
        figure = plot(self._reduced_set, self._k_clusters, embedded=True)
        self._kmeans_viz_panel.display_figure(figure)
        self.log("-- End K-means plotting --")

    def _on_generate_plot_dbscan(self):
        self.log("user: pressed Generate Plot button (dbscan)")
        dimensions = self._dbscan_viz_panel.get_dimensions()
        self.log("Plotting in %s dimensions" % self._dbscan_viz_panel.get_dimensions())
        plot = db.plot2D if dimensions == 2 else db.plot3D
        self.log("PCA reducing cluster data to %s dimensions..." % dimensions)
        self._reduced_set = dataops.pca(self._dataset, dimensions)
        self.log("Plotting...")
        figure = plot(self._db_clusters, self._reduced_set)
        self._dbscan_viz_panel.display_figure(figure)
        self.log("-- End DBSCAN plotting --")

class VisualizationPanel(object):
    """A panel with tkinter widgets for the K-means and DBSCAN
    visualization plots."""

    def __init__(self, parent, button_handler):
        """Set up frame and widgets."""
        # this is the 'main' frame
        # either the 'controls' frame or the 'canvas' frame
        # will be gridded into this 'main' frame
        self._Frame = ttk.Frame(parent)
        self._Frame.grid_columnconfigure(0, weight=1)
        self._Frame.grid_rowconfigure(0, weight=1)
        # this is the 'canvas' frame
        # it's empty at instantiation
        self._Frame_canvas = ttk.Frame(self._Frame)
        self._Frame_canvas.grid_columnconfigure(0, weight=1)
        self._Frame_canvas.grid_rowconfigure(0, weight=1)
        self._Frame_canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        # this is the 'controls' frame
        self._Frame_controls = ttk.Frame(self._Frame)
        self._Var_dimensions = tk.StringVar()
        self._Combobox = ttk.Combobox(self._Frame_controls, width=5, justify="center",
                                      state="readonly", textvariable=self._Var_dimensions,
                                      values=['2D', '3D'])
        self._Combobox.current(0)
        self._Combobox.grid(pady=10)
        self._Button = ttk.Button(self._Frame_controls, width=15, text="Generate Plot",
                                  command=button_handler)
        self._Button.grid()
        self._Frame_controls.grid(row=0, column=0)

    def get_frame_handle(self):
        """Return handle to the 'main' frame so it can be gridded
        into the calling application."""
        return self._Frame

    def get_dimensions(self):
        """Return the number of dimensions selected by the combobox."""
        return 2 if self._Var_dimensions.get() == '2D' else 3

    def disable_widgets(self):
        """Disable the dimensions combobox and Generate Plot button
        so that user can't try to plot before clusters data is available."""
        self._Combobox.config(state="disabled")
        self._Button.config(state="disabled")

    def enable_widgets(self):
        """Enable the dimensions combobox and Generate Plot button."""
        self._Combobox.config(state="readonly")
        self._Button.config(state="normal")

    def display_figure(self, figure):
        """Set up a canvas, display a matplotlib figure on it, and
        set up the plot toolbar."""
        self._Frame_controls.lower() # hide 'controls' frame
        canvas = FigureCanvasTkAgg(figure, master=self._Frame_canvas)
        canvas.draw()
        # NOTE: must use pack geometry manager instead of grid here.
        # FigureCanvasTkAgg and NavigationToolbar2Tk appear to be using
        # pack internally and mixing it with grid is causing problems.
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self._Frame_canvas)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def destroy_canvas(self):
        """Remove any existing canvas plot and then hide the
        'canvas' frame so the 'controls' frame becomes visible
        again and the user can plot again with new data."""
        for widget in self._Frame_canvas.winfo_children():
            widget.destroy()
        self._Frame_canvas.lower() # hide 'canvas' frame
