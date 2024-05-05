# Define the application name variable
APP_NAME = YouTube Summariser App

# Default target
all: build zip

# Build the application using PyInstaller
build:
	pyinstaller --onefile --windowed --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' "$(APP_NAME).py"

# Zip the application in the dist directory
zip:
	cd dist && zip -r "$(APP_NAME).zip" "$(APP_NAME).app"

# Clean build artifacts
clean:
	rm -rf build dist $(APP_NAME).spec

.PHONY: all build zip clean
