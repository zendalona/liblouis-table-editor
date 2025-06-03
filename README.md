# Liblouis Table Editor

A graphical editor for Liblouis translation tables.

## Prerequisites

Before installing the Liblouis Table Editor, you must have Liblouis installed on your system:

1. Download and install Liblouis from the official website
2. Install it to the default location: `C:\Program Files\liblouis`
3. Make sure the installation includes:
   - `bin/lou_translate.exe`
   - `share/liblouis/tables` directory

## Installation

1. Download the latest release of Liblouis Table Editor
2. Extract the ZIP file to your desired location
3. Run `LiblouisTableEditor.exe` from the extracted folder

## Building from Source

If you want to build the application from source:

1. Install Python 3.8 or later
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the build script:
   ```
   python build.py
   ```
4. The built application will be in the `dist/LiblouisTableEditor` directory

## Troubleshooting

If you encounter any issues:

1. Make sure Liblouis is properly installed in `C:\Program Files\liblouis`
2. Verify that the Liblouis installation includes all required files
3. Check that you have the correct version of Python installed

## Usage

After launching the application, you'll be presented with a user-friendly interface where you can start creating or editing Liblouis tables. The editor provides various tools and options to help you define translation rules, test them, and ensure they work as intended.
