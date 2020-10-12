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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import space_kmeans
import space_random_data
import space_plot_kmeans
import normalization


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
        self.app_config = app_config
        if app_config != {}:
            self.master.title("%s v. %s" %
                              (self.app_config.get("APP_NAME", 'Application'),
                               self.app_config.get("APP_VERSION", 'Unknown')))
        self.grid()

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
        # -- normalize is by itself, no sub-frame --
        self._Var_normalize = tk.BooleanVar()
        self._Checkbutton_normalize = ttk.Checkbutton(self._LabelFrame_data, text="Normalize data during import",
                                                     variable=self._Var_normalize)
        self._Checkbutton_normalize.grid(row=1, sticky=tk.W)
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
        self._Entry_eps = ttk.Entry(self._Frame_dbscan_parameters, width=5, justify="center", textvariable=self._Var_eps)
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
        self._Notebook_controller = ttk.Notebook(self)
        # the tabs
        self._Tab_log = ttk.Frame(self._Notebook_controller)
        self._Tab_kmeans = ttk.Frame(self._Notebook_controller)
        self._Tab_dbscan = ttk.Frame(self._Notebook_controller)
        # rezise setup
        for tab in (self._Tab_log, self._Tab_kmeans, self._Tab_dbscan):
            tab.grid_columnconfigure(index=0, weight=1)
            tab.grid_rowconfigure(index=0, weight=1)
        self._Notebook_controller.add(self._Tab_log, text="Log")
        self._Notebook_controller.add(self._Tab_kmeans, text="K-means plot")
        self._Notebook_controller.add(self._Tab_dbscan, text="DBSCAN plot")
        # log text box and scrollbars
        self._Scroll_H = ttk.Scrollbar(self._Tab_log, orient = tk.HORIZONTAL)
        self._Scroll_V = ttk.Scrollbar(self._Tab_log, orient = tk.VERTICAL)
        self._Text_log = tk.Text(self._Tab_log, wrap = tk.NONE, width=72, height=36,
                                xscrollcommand = self._Scroll_H.set,
                                yscrollcommand = self._Scroll_V.set,
                                bg="black", fg="gray")
        self._Scroll_H["command"] = self._Text_log.xview
        self._Scroll_V["command"] = self._Text_log.yview
        self._Text_log.grid(row=0, column=0)
        self._Scroll_H.grid(row=1, column=0, sticky=tk.E+tk.W)
        self._Scroll_V.grid(row=0, column=1, sticky=tk.N+tk.S)
        # kmeans panel
        self._kmeans_viz_panel = VisualizationPanel(self._Tab_kmeans, self)
        self._kmeans_viz_panel.get_frame_handle().grid()
        self._kmeans_viz_panel.disable_widgets()
        # dbscan panel
        self._dbscan_viz_panel = VisualizationPanel(self._Tab_dbscan, self)
        self._dbscan_viz_panel.get_frame_handle().grid()
        self._dbscan_viz_panel.disable_widgets()

        # end setup of NOTEBOOK (tabs), right column
        self._Notebook_controller.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)


    def _set_defaults(self):
        self._Var_folder.set(self.app_config["DEFAULT_INPUT_PATH"])
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

    def _on_browse(self):
        dir = tkfd.askdirectory(initialdir=self._Var_folder.get())
        # askdirectory returns '' if the user clicked cancel
        # so only update the folder path if the user actually selected something
        if dir != '':
            self.log("user: changed input folder to %s" % dir)
            self._Var_folder.set(dir)

    def _do_import_data(self):
        # reset everything, in case we are running multiple times
        self._data_objs = []
        # verify we have a good path in the input folder widget
        if not fileops.path_exists(self._Var_folder.get()):
            # a nonexistent path is a fatal error
            # log to console and pop up a messagebox
            self.log("Invalid path: %s" % self._Var_folder.get())
            self._quick_message_box("Invalid path:\n%s" % self._Var_folder.get())
            return
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

        fileops.save_files(self._Var_folder.get(), "/align/", self._data_objs)
        
        #PCA
        if self._Var_pca.get():
            self.log('Performing PCA to ' + str(self._Var_pca_dimensions.get()) + ' dimensions')
            normalization.PCAnormalize(self._data_objs, self._Var_pca_dimensions.get())
            self.log('PCA applied')

        # final, pre-processed dataset
        self.log("Done importing and pre-processing data files")
        self._dataset = dataops.combine(self._data_objs)
        
        # alignment
   

    def _on_go(self):
        # this might take a while, so disable the Go button and busy the cursor
        # while we do work
        self._Button_go.config(state="disabled")
        self.update()
        self.master.config(cursor="watch")
        sleep(.5)   # cursor is sometimes not updating without this delay
        self.master.update()
        self.log("user: pressed Go button")
        self._do_import_data()

        #This re-enables the save button
        self._Button_save["state"] = "normal"
        # TODO: normalization

        
        # kmeans
        if self._Var_kmeans.get() and self._data_objs != []:
            self.log("Performing K-means...")
            k_clusters = space_kmeans.do_Kmeans(self._Var_kmeans_clusters.get(), self._dataset)
            self.log("...done.")
            composition = space_kmeans.calculate_composition(k_clusters, self._Var_kmeans_clusters.get(), self._data_objs)
            # TODO: check the kmeans clustering succeeded before enabling plot widgets
            self._kmeans_viz_panel.enable_widgets()
            # plotting broke, disable for now
            #space_plot_kmeans.plot(self._dataset, k_clusters)
        # TODO: dbscan
        # re-enable Go button and un-busy the cursor now that we're done
        self.master.config(cursor="")
        self._Button_go.config(state="normal")
        self.master.update()

    def _on_save(self):
        self._quick_message_box("Congrats, you clicked the Save button.  This actuall does nothing now, but eventually might!")

    def _on_close(self):
        self.master.destroy()

class VisualizationPanel(object):
    """A panel with tkinter widgets for the K-means and DBSCAN
    visualization plots."""

    def __init__(self, parent, controller):
        """Set up frame and widgets."""
        self._Frame = ttk.Frame(parent)
        self._Frame.grid()
        self._Var_dimensions = tk.StringVar()
        self._Combobox = ttk.Combobox(self._Frame, width=5, justify="center",
                                        state="readonly", textvariable=self._Var_dimensions,
                                        values=['2D', '3D'])
        self._Combobox.current(0)
        self._Combobox.grid(pady=10)
        self._Button = ttk.Button(self._Frame, width=15, text="Generate Plot")
        self._Button.grid()

    def get_frame_handle(self):
        return self._Frame

    def disable_widgets(self):
        self._Combobox.config(state="disabled")
        self._Button.config(state="disabled")

    def enable_widgets(self):
        self._Combobox.config(state="readonly")
        self._Button.config(state="normal")