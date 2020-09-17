# What kind of standardized header comments do we want to include?
#

import space_gui as gui

APP_NAME	= "SpACE"
APP_VERSION	= "0.0.1"

def main():
	print("This is %s version %s." % (APP_NAME, APP_VERSION))
	gui.launch_gui()


if __name__ == '__main__':
    main()