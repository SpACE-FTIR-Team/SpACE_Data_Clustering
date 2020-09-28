# What kind of standardized header comments do we want to include?
#

from os import getcwd
import space_gui as gui

CONFIG = {
	"APP_NAME": "SpACE",
	"APP_VERSION": "0.0.4",
	"DEFAULT_PCA_DIMENSIONS": 2,
	"DEFAULT_KMEANS_K": 8,
	"DEFAULT_DBSCAN_EPS": 1.0,
	"DEFAULT_DBSCAN_MINPTS": 3,
	"DEFAULT_INPUT_PATH": None,
}

def main():
	print("This is %s version %s." % (CONFIG["APP_NAME"], CONFIG["APP_VERSION"]))
	# add current directory to the config -- used for initial input folder path
	# might change this later
	CONFIG["DEFAULT_INPUT_PATH"] = getcwd()
	gui.launch_gui(CONFIG)

if __name__ == '__main__':
    main()