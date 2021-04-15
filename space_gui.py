# -*- coding: utf-8 -*-
# 
# Spectral Analysis Clustering Explorer (SpACE)
# Missouri State University
# CSC450 Fall 2020 - Dr. Razib Iqbal
#
# Team 2 (FTIR/ECOSTRESS/SpACE team):
# Austin Alvidrez
# Brad Meyer
# Collin Tinen
# Kegan Moore
# Sam Nack
#
# Copyright 2020 Austin Alvidrez, Brad Meyer, Collin Tinen,
# Kegan Moore, Sam Nack
#
# Spectral Analysis Clustering Explorer (SpACE) is free software:
# you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Spectral Analysis Clustering Explorer (SpACE) is distributed in
# the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with Spectral Analysis Clustering Explorer (SpACE).
# If not, see <https://www.gnu.org/licenses/>.

# space_gui.py
# This is the graphical user interface for the SpACE application.

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
import tkinter.filedialog as tkfd
from time import sleep
import os.path
import space_file_ops as fileops
import space_data_ops as dataops
import space_kmeans as km
import space_dbscan as db
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


# entire file is linked to External Interface Requirements #1 - product must be encapsulated into a Graphical User
# Interface
# entire file is linked to Non-functional requirement #1 - GUI responds in 2 seconds or less
def launch_gui(cnf):
    root = tk.Tk()
    app = SpaceApp(master=root, app_config=cnf)
    app.mainloop()


class SpaceApp(tk.Frame):
    """A tkinter GUI-based app for SpACE."""

    # linked to functional requirement #13 - pre-populate parameters for k-means and DBSCAN with default values
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

        # data objects holding pandas dataframes (empty for now)
        self._data_objs = []
        # combined dataframe (none for now)
        self._dataset = None

    def _create_widgets(self):
        """Create and configure all the widgets in the main frame."""
        self.grid_columnconfigure(index=0, weight=0)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_rowconfigure(index=0, weight=1)

        # OPTIONS FRAME, left column
        self._Frame_options = ttk.Frame(self)

        # - DATA widgets -
        self._LabelFrame_data = tk.LabelFrame(self._Frame_options, text="Data")

        # -- input sub-frame --
        self._Frame_input = ttk.Frame(self._LabelFrame_data)
        self._Label_data_text = ttk.Label(self._Frame_input, text="Input from folder:")
        self._Var_folder = tk.StringVar()
        self._Entry_folder = ttk.Entry(self._Frame_input, width=30, textvariable=self._Var_folder)
        self._Button_browse = ttk.Button(self._Frame_input, text="Browse...", command=self._on_browse)
        self._Label_data_text.grid(row=0, column=0, sticky=tk.W)
        self._Entry_folder.grid(row=1, column=0, sticky=tk.W)
        self._Button_browse.grid(row=1, column=1, padx=(5, 0))
        self._Frame_input.grid(row=0, padx=5, pady=(5, 0), sticky=tk.W)

        # -- align sub-frame --
        self._Frame_align = ttk.Frame(self._LabelFrame_data)
        self._Var_align = tk.BooleanVar()
        self._Checkbutton_align = ttk.Checkbutton(self._Frame_align, text= "Use aligned data", variable=self._Var_align)
        self._Checkbutton_align.grid(row=0,sticky=tk.W)
        self._Frame_align.grid(row=1,padx=5,pady=(10,0),sticky=tk.W)

        # -- normalize sub-frame --
        Frame_normalize = ttk.Frame(self._LabelFrame_data)
        Label_normalize = ttk.Label(Frame_normalize, text="Normalization:")
        self._Var_normalize = tk.StringVar()
        Combobox_normalize = ttk.Combobox(Frame_normalize, width=10, justify="center",
                                          state="readonly", textvariable=self._Var_normalize,
                                          values=list(dataops.NORMALIZATION_TYPES.keys()))
        Combobox_normalize.current(0)
        Label_normalize.grid(row=0, column=0, sticky=tk.W)
        Combobox_normalize.grid(row=0, column=1, padx=(5, 0), sticky=tk.W)
        Frame_normalize.grid(row=2, padx=5, pady=(10, 0), sticky=tk.W)

        # -- pca sub-frame --
        self._Frame_pca = ttk.Frame(self._LabelFrame_data)
        self._Var_pca = tk.BooleanVar()
        self._Var_pca_dimensions = tk.IntVar()
        self._Checkbutton_pca = ttk.Checkbutton(self._Frame_pca, text="Perform PCA", variable=self._Var_pca)
        self._Label_pca_text = ttk.Label(self._Frame_pca, text="Number of dimensions:")
        self._Entry_pca = ttk.Entry(self._Frame_pca, width=5, justify="center", textvariable=self._Var_pca_dimensions)
        self._Checkbutton_pca.grid(row=0, sticky=tk.W)
        self._Label_pca_text.grid(row=1, column=0, sticky=tk.W)
        self._Entry_pca.grid(row=1, column=1, padx=5)
        self._Frame_pca.grid(row=3, padx=5, pady=(10, 0), sticky=tk.W)

        # -- save after processing steps --
        self._Var_save_after_modify = tk.BooleanVar()
        Checkbutton_save_after_modify = ttk.Checkbutton(self._LabelFrame_data, text="Save after each data modification",
                                                        variable=self._Var_save_after_modify)
        Checkbutton_save_after_modify.grid(row=4, padx=5, pady=10, sticky=tk.W)

        # - DATA widgets grid -
        self._LabelFrame_data.grid(row=0, column=0, padx=(10, 0), pady=(5, 0))

        # - KMEANS widgets -
        self._Var_kmeans = tk.BooleanVar()
        self._Var_kmeans_clusters = tk.IntVar()
        w = ttk.Checkbutton(self._Frame_options, text="K-means algorithm", variable=self._Var_kmeans)
        Labelframe = tk.LabelFrame(self._Frame_options, labelwidget=w)
        w = ttk.Label(Labelframe, text="Number of clusters (k):")
        w.grid(row=0, column=0, padx=5, pady=(5, 10), sticky=tk.W)
        w = ttk.Entry(Labelframe, width=5, justify="center", textvariable=self._Var_kmeans_clusters)
        w.grid(row=0, column=1, pady=(5, 10))
        # - KMEANS widgets grid -
        Labelframe.grid(row=1, column=0, padx=(10, 0), pady=(40, 5), sticky=tk.EW)

        # - DBSCAN widgets -
        self._Var_dbscan = tk.BooleanVar()
        w = ttk.Checkbutton(self._Frame_options, text="DBSCAN algorithm", variable=self._Var_dbscan)
        Labelframe = tk.LabelFrame(self._Frame_options, labelwidget=w)
        self._Var_eps = tk.DoubleVar()
        self._Var_minpts = tk.IntVar()
        w = ttk.Label(Labelframe, text="Epsilon:")
        w.grid(row=0, column=0, padx=5, pady=(10, 5), sticky=tk.E)
        w = ttk.Entry(Labelframe, width=5, justify="center", textvariable=self._Var_eps)
        w.grid(row=0, column=1, pady=(10, 5), sticky=tk.W)
        w = ttk.Label(Labelframe, text="MinPts:")
        w.grid(row=1, column=0, padx=5, pady=(0, 10), sticky=tk.E)
        w = ttk.Entry(Labelframe, width=5, justify="center", textvariable=self._Var_minpts)
        w.grid(row=1, column=1, pady=(0, 10), sticky=tk.W)
        # - DBSCAN grid -
        Labelframe.grid(row=2, column=0, padx=(10, 0), pady=(5, 0), sticky=tk.EW)

        # - BUTTONS for actions -
        self._Frame_action_buttons = ttk.Frame(self._Frame_options)
        self._Button_go = ttk.Button(self._Frame_action_buttons, text="Go", width=15, command=self._on_go)
        self._Button_save = ttk.Button(self._Frame_action_buttons, text="Save", width=15, command=self._on_save)
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
        # resize setup
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
        self._Var_save_after_modify.set(self.app_config["SAVE_AFTER_DATA_MODIFICATION_BY_DEFAULT"])
        self._Var_kmeans_clusters.set(self.app_config["DEFAULT_KMEANS_K"])
        self._Var_eps.set(self.app_config["DEFAULT_DBSCAN_EPS"])
        self._Var_minpts.set(self.app_config["DEFAULT_DBSCAN_MINPTS"])
        self._Button_save["state"] = "disabled"
        self.saving_params = {"kmeans": self.app_config["KMEANS_SAVING"],
                              "dbscan": self.app_config["DBSCAN_SAVING"],
                              "folder": self.app_config["DEFAULT_INPUT_PATH"]}

    def _reset_default_save_path(self):
        """Reset the default save path for cluster compositions to
        subfolder /cluster_composition/ under the input folder.
        e.g. if selected input folder is D:/INPUT
        the default save path with be D:/INPUT/cluster_composition/"""
        self.saving_params["folder"] = os.path.join(self._Var_folder.get(),
                                                    "cluster_composition")

    def log(self, text):
        """A simple logging facility for status messages
        during program execution."""
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

    # linked to functional requirement #5 - accept input from data files
    # linked to functional requirement #10 - accept subset of data folders
    def _on_browse(self):
        dir = tkfd.askdirectory(initialdir=self._Var_folder.get())
        # askdirectory returns '' if the user clicked cancel
        # so only update the folder path if the user actually selected something
        if dir != '':
            self.log("user: changed input folder to %s" % dir)
            self._Var_folder.set(dir)

    def _on_clear_log(self):
        self._Text_log.delete(1.0, tk.END)

    # linked to functional requirement #6 - normalize data
    # linked to functional requirement #3 - preprocess data files
    # linked to functional requirement #7 - PCA
    def _do_import_data(self):
        # reset everything, in case we are running multiple times
        self._data_objs = []
        self._dataset = None
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
        if not self._Var_align:
            #This means we are working with the raw Ecostress files,
            #if false, we are working with already aligned files, and we can skip this step
            self.log("Loading into data objects...")
            self._data_objs, return_msg = dataops.file_to_data_object(filtered_file_list)
            if not self._data_objs:
                self.log(return_msg)
                self._quick_message_box(return_msg)
                return
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
            if self._Var_save_after_modify.get():
                self.log("Saving aligned data...")
                fileops.save_data_files(self._Var_folder.get(), "aligned", self._data_objs)
        else:
            #Working with already aligned files
            self.log("Loading aligned files into data objects...")
            self._data_objs = dataops.aligned_file_to_data_object(filtered_file_list)
            self.log("Loaded %s data objects" % len(self._data_objs))

        # Normalization
        self.log("Normalizing data with method: %s" % self._Var_normalize.get())
        self._data_objs = dataops.NORMALIZATION_TYPES[self._Var_normalize.get()](self._data_objs)
        if self._Var_save_after_modify.get():
            self.log("Saving normalized data...")
            fileops.save_data_files(self._Var_folder.get(), "normalized", self._data_objs)
        # final, pre-processed dataset
        self._dataset = dataops.combine(self._data_objs)
        if self._Var_save_after_modify.get():
            self.log("Saving final combined dataframe...")
            fileops.save_block_data(self._Var_folder.get(), "block", self._dataset)
        # PCA
        if self._Var_pca.get():
            self.log('Performing PCA to ' + str(self._Var_pca_dimensions.get()) + ' dimensions...')
            self._dataset = dataops.pca(self._dataset, self._Var_pca_dimensions.get())
            self.log('PCA applied')
            if self._Var_save_after_modify.get():
                self.log("Saving PCA-reduced data...")
                # the folder suffix here is a nested subfolder path like:
                # \block\PCA-<number of dimensions> so the individual
                # path components are passed as a tuple
                fileops.save_block_data(self._Var_folder.get(), ("block", "PCA-" + self._Entry_pca.get()),
                                        self._dataset)

        self.log("-- End data import and pre-processing --")

    # linked to functional requirement #1 - kmeans clustering algorithm
    def _do_kmeans_clustering(self):
        self.log("-- Begin K-means clustering --")
        self.log("Clustering...")
        self._k_clusters = km.do_Kmeans(self._Var_kmeans_clusters.get(), self._dataset)
        self.log("-- End K-means clustering --")
        self._kmeans_viz_panel.enable_widgets()

    # linked to functional requirement #2 - dbscan clustering algorithm
    def _do_dbscan_clustering(self):
        # epsilon: self._Var_eps.get()
        # minpts: self._Var_minpts.get()
        self.log("-- Begin DBSCAN clustering --")
        self.log("Clustering...")
        self._db_clusters = db.do_dbscan(self._Var_eps.get(), self._Var_minpts.get(), self._dataset)
        self.log("-- End DBSCAN clustering --")
        self._dbscan_viz_panel.enable_widgets()

    # linked to functional requirement #8 - save data after modification
    # linked to functional requirement #9 - save clustered data
    # linked to non-functional requirement #4 - save as .csv files
    # linked to non-functional requirement #5 - save files in a tree format
    def _do_save_cluster_composition(self):
        """This function is the button handler for the Save button in the save dialog box."""
        self.log("user: pressed Save button in save dialog")
        if self.saving_params["kmeans"]["save"]:
            self.log("Calculating K-Means cluster compositions...")
            if self.saving_params["kmeans"]["by_type"]:
                composition_by_type = km.calculate_composition(self._k_clusters, self._Var_kmeans_clusters.get(),
                                                               self._data_objs, 1)
                fileops.save_composition(self.saving_params["folder"], "kmeans", "by_type", composition_by_type)
            if self.saving_params["kmeans"]["by_class"]:
                composition_by_class = km.calculate_composition(self._k_clusters, self._Var_kmeans_clusters.get(),
                                                                self._data_objs, 2)
                fileops.save_composition(self.saving_params["folder"], "kmeans", "by_class", composition_by_class)
            if self.saving_params["kmeans"]["by_subclass"]:
                composition_by_subclass = km.calculate_composition(self._k_clusters, self._Var_kmeans_clusters.get(),
                                                                   self._data_objs, 3)
                fileops.save_composition(self.saving_params["folder"], "kmeans", "by_subclass", composition_by_subclass)
            self.log("Finished K-Means cluster compositions...")
        if self.saving_params["dbscan"]["save"]:
            self.log("Calculating DBSCAN cluster compositions...")
            if self.saving_params["dbscan"]["by_type"]:
                composition_by_type = db.db_comp(self._db_clusters, self._data_objs, 1)
                fileops.save_composition(self.saving_params["folder"], "dbscan", "by_type", composition_by_type)
            if self.saving_params["dbscan"]["by_class"]:
                composition_by_class = db.db_comp(self._db_clusters, self._data_objs, 2)
                fileops.save_composition(self.saving_params["folder"], "dbscan", "by_class", composition_by_class)
            if self.saving_params["dbscan"]["by_subclass"]:
                composition_by_subclass = db.db_comp(self._db_clusters, self._data_objs, 3)
                fileops.save_composition(self.saving_params["folder"], "dbscan", "by_subclass", composition_by_subclass)
            self.log("Finished DBSCAN cluster compositions...")

    def _on_go(self):
        # this might take a while, so disable the buttons and busy the cursor
        # while we do work
        self._Button_go.config(state="disabled")
        self._Button_save.config(state="disabled")
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
        # reset default cluster save location in case user is using
        # new input data from a new path
        self._reset_default_save_path()
        if self._validate_user_input():
            # all input checks passed
            self._do_import_data()
            if self._Var_kmeans.get() and self._data_objs != []:
                self._do_kmeans_clustering()
            if self._Var_dbscan.get() and self._data_objs != []:
                self._do_dbscan_clustering()
            # re-enable the save button if at least one algorithm was selected
            if self._Var_kmeans.get() or self._Var_dbscan.get():
                self._Button_save["state"] = "normal"

        # re-enable Go button and un-busy the cursor now that we're done
        self.master.config(cursor="")
        self._Button_go.config(state="normal")
        self.master.update()

    def _on_save(self):
        # reset default folder for saving to be the same folder as input
        # SaveDialog will append the /cluster_composition (or whatever
        # the user selects)
        SaveDialog(self.master, params=self.saving_params,
                   handler=self._do_save_cluster_composition,
                   title="Save Cluster Composition",
                   kmeans=self._Var_kmeans.get(), dbscan=self._Var_dbscan.get())

    def _on_close(self):
        self.master.quit()
        self.master.destroy()

    # linked to non-functional requirement #2 - perform 2D and 3D visualization in 5 minutes or less
    # linked to functional requirement #11 - visualize clustered data
    def _on_generate_plot_kmeans(self):
        self.log("user: pressed Generate Plot button (K-means)")
        plot_dataset = None
        dimensions = self._kmeans_viz_panel.get_dimensions()
        self.log("-- Begin K-means plotting in %sD --" % dimensions)
        plot = km.plot2D if dimensions == 2 else km.plot3D
        if self._dataset.shape[1] == dimensions:
            self.log("Skipping PCA because data set is already %s dimensions" % dimensions)
            plot_dataset = self._dataset
        elif self._dataset.shape[1] < dimensions:
            self.log(
                "Cannot plot in %sD because input data is only in %s dimensions" % (dimensions, self._dataset.shape[1]))
            self._quick_message_box(
                "Cannot plot in %sD because input data is only in %s dimensions.\nPlotting in 2D instead."
                % (dimensions, self._dataset.shape[1]))
            plot_dataset = self._dataset
            plot = km.plot2D
        else:
            self.log("PCA reducing data to %s dimensions..." % dimensions)
            plot_dataset = dataops.pca(self._dataset, dimensions)
        self.log("Plotting...")
        canvas = plot(plot_dataset, self._k_clusters, embedded=True,
                      master=self._kmeans_viz_panel.get_canvas_frame_handle())
        self._kmeans_viz_panel.display_plot(canvas)
        self.log("-- End K-means plotting --")

    # linked to non-functional requirement #2 - perform 2D and 3D visualization in 5 minutes or less
    # linked to functional requirement #11 - visualize clustered data
    def _on_generate_plot_dbscan(self):
        self.log("user: pressed Generate Plot button (dbscan)")
        plot_dataset = None
        dimensions = self._dbscan_viz_panel.get_dimensions()
        self.log("-- Begin DBSCAN plotting in %sD --" % dimensions)
        plot = db.plot2D if dimensions == 2 else db.plot3D
        if self._dataset.shape[1] == dimensions:
            self.log("Skipping PCA because data set is already %s dimensions" % dimensions)
            plot_dataset = self._dataset
        elif self._dataset.shape[1] < dimensions:
            self.log(
                "Cannot plot in %sD because input data is only in %s dimensions" % (dimensions, self._dataset.shape[1]))
            self._quick_message_box(
                "Cannot plot in %sD because input data is only in %s dimensions.\nPlotting in 2D instead."
                % (dimensions, self._dataset.shape[1]))
            plot_dataset = self._dataset
            plot = db.plot2D
        else:
            self.log("PCA reducing data to %s dimensions..." % dimensions)
            plot_dataset = dataops.pca(self._dataset, dimensions)
        self.log("Plotting...")
        canvas = plot(plot_dataset, self._db_clusters, embedded=True,
                      master=self._dbscan_viz_panel.get_canvas_frame_handle())
        self._dbscan_viz_panel.display_plot(canvas)
        self.log("-- End DBSCAN plotting --")


# linked to functional requirement #11 - visualize clustered data
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

    def get_canvas_frame_handle(self):
        """Return handle to the 'canvas' frame so the plot
        function can generate a canvas as a child of this frame."""
        return self._Frame_canvas

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

    def display_plot(self, canvas):
        """Display the canvas containing the plot and
        set up the plot toolbar."""
        self._Frame_controls.lower()  # hide 'controls' frame
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

        self._Frame_canvas.lower()  # hide 'canvas' frame


# linked to functional requirement #9 - save clustered data
class SaveDialog(tk.Toplevel):
    """A modal dialog for saving cluster composition."""

    # This is largely based on effbot's dialog box class at
    # https://effbot.org/tkinterbook/tkinter-dialog-windows.htm
    def __init__(self, parent, params, handler, title=None, kmeans=False, dbscan=False):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self._parameters = params
        self._save_handler = handler

        self._create_vars()
        self._create_widgets()
        if not kmeans:
            self._disable_widgets(self._kmeans_checkbuttons)
        if not dbscan:
            self._disable_widgets(self._dbscan_checkbuttons)

        self.grab_set()
        self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    def _create_vars(self):
        self._Var_folder = tk.StringVar()
        self._Var_folder.set(self._parameters["folder"])
        self._Var_kmeans = tk.BooleanVar()
        self._Var_kmeans.set(self._parameters["kmeans"]["save"])
        self._Var_kmeans_type = tk.BooleanVar()
        self._Var_kmeans_type.set(self._parameters["kmeans"]["by_type"])
        self._Var_kmeans_class = tk.BooleanVar()
        self._Var_kmeans_class.set(self._parameters["kmeans"]["by_class"])
        self._Var_kmeans_subclass = tk.BooleanVar()
        self._Var_kmeans_subclass.set(self._parameters["kmeans"]["by_subclass"])
        self._Var_dbscan = tk.BooleanVar()
        self._Var_dbscan.set(self._parameters["dbscan"]["save"])
        self._Var_dbscan_type = tk.BooleanVar()
        self._Var_dbscan_type.set(self._parameters["dbscan"]["by_type"])
        self._Var_dbscan_class = tk.BooleanVar()
        self._Var_dbscan_class.set(self._parameters["dbscan"]["by_class"])
        self._Var_dbscan_subclass = tk.BooleanVar()
        self._Var_dbscan_subclass.set(self._parameters["dbscan"]["by_subclass"])

    def _create_widgets(self):
        Frame = ttk.Frame(self)

        w = ttk.Label(Frame, text="Select what to save:")
        w.grid(row=0, columnspan=2, pady=(10, 5))

        Frame_checkbuttons = ttk.Frame(Frame)
        self._kmeans_checkbuttons = []
        self._dbscan_checkbuttons = []
        w = ttk.Checkbutton(Frame_checkbuttons, text="K-means", variable=self._Var_kmeans)
        self._kmeans_checkbuttons.append(w)
        Labelframe = tk.LabelFrame(Frame_checkbuttons, labelwidget=w)
        w = ttk.Checkbutton(Labelframe, text="By Type", variable=self._Var_kmeans_type)
        self._kmeans_checkbuttons.append(w)
        w.grid(padx=10, pady=(10, 0), sticky=tk.W)
        w = ttk.Checkbutton(Labelframe, text="By Class", variable=self._Var_kmeans_class)
        self._kmeans_checkbuttons.append(w)
        w.grid(padx=10, sticky=tk.W)
        w = ttk.Checkbutton(Labelframe, text="By Subclass", variable=self._Var_kmeans_subclass)
        self._kmeans_checkbuttons.append(w)
        w.grid(padx=10, pady=(0, 10), sticky=tk.W)
        Labelframe.grid(row=1, column=0, padx=5)

        w = ttk.Checkbutton(Frame_checkbuttons, text="DBSCAN", variable=self._Var_dbscan)
        self._dbscan_checkbuttons.append(w)
        Labelframe = tk.LabelFrame(Frame_checkbuttons, labelwidget=w)
        w = ttk.Checkbutton(Labelframe, text="By Type", variable=self._Var_dbscan_type)
        self._dbscan_checkbuttons.append(w)
        w.grid(padx=10, pady=(10, 0), sticky=tk.W)
        w = ttk.Checkbutton(Labelframe, text="By Class", variable=self._Var_dbscan_class)
        self._dbscan_checkbuttons.append(w)
        w.grid(padx=10, sticky=tk.W)
        w = ttk.Checkbutton(Labelframe, text="By Subclass", variable=self._Var_dbscan_subclass)
        self._dbscan_checkbuttons.append(w)
        w.grid(padx=10, pady=(0, 10), sticky=tk.W)
        Labelframe.grid(row=1, column=1, padx=5)
        Frame_checkbuttons.grid(padx=5)

        w = ttk.Label(Frame, text="Select a folder to save in:")
        w.grid(row=2, columnspan=2, pady=(10, 5))
        Frame_folder = ttk.Frame(Frame)
        w = ttk.Entry(Frame_folder, width=30, textvariable=self._Var_folder)
        w.grid(row=0, column=0, sticky=tk.E)
        w = ttk.Button(Frame_folder, text="Browse...", command=self._on_browse)
        w.grid(row=0, column=1, padx=(5, 0))
        Frame_folder.grid(padx=10)

        Frame_buttons = ttk.Frame(Frame)
        Button_save = ttk.Button(Frame_buttons, text="Save", width=15, command=self._on_save, default=tk.ACTIVE)
        Button_cancel = ttk.Button(Frame_buttons, text="Cancel", width=15, command=self._on_cancel)
        Button_save.grid(row=0, column=0, padx=(0, 5))
        Button_cancel.grid(row=0, column=1)

        self.bind("<Return>", self._on_save)
        self.bind("<Escape>", self._on_cancel)

        Frame_buttons.grid(pady=20)
        Frame.grid()

    def _disable_widgets(self, widgets):
        for w in widgets:
            # get tkVar associated with the widget
            tkvar = w["variable"]
            # set tkVar to False (uncheck the box)
            w.setvar(tkvar, False)
            # disable the widget (grays it out)
            w["state"] = "disabled"

    def _on_browse(self):
        dir = tkfd.askdirectory(initialdir=self._Var_folder.get())
        # askdirectory returns '' if the user clicked cancel
        # so only update the folder path if the user actually selected something
        if dir != '':
            self._Var_folder.set(dir)
            self._parameters["folder"] = dir

    def _on_save(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return
        self.withdraw()
        self.update_idletasks()

        self._parameters["kmeans"]["save"] = self._Var_kmeans.get()
        self._parameters["kmeans"]["by_type"] = self._Var_kmeans_type.get()
        self._parameters["kmeans"]["by_class"] = self._Var_kmeans_class.get()
        self._parameters["kmeans"]["by_subclass"] = self._Var_kmeans_subclass.get()
        self._parameters["dbscan"]["save"] = self._Var_dbscan.get()
        self._parameters["dbscan"]["by_type"] = self._Var_dbscan_type.get()
        self._parameters["dbscan"]["by_class"] = self._Var_dbscan_class.get()
        self._parameters["dbscan"]["by_subclass"] = self._Var_dbscan_subclass.get()

        self._save_handler()
        self._on_cancel()

    def _on_cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        return 1  # override
