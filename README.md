# liblouis-table-editor

A graphical editor for Liblouis translation tables. This application provides a user-friendly interface for creating and editing Liblouis braille translation tables.

## Prerequisites

Before installing the Liblouis Table Editor, you must have Liblouis installed on your system.

For detailed installation instructions, see [Liblouis Installation Guide](Prerequisite%20-%20Liblouis%20Installation%20Guide.md).

## Installation

1. Download the latest release of Liblouis Table Editor release.
2. Install to your desired location
3. Run `LiblouisTableEditor.exe` (Windows) or the appropriate executable for your platform

## "Open With" Functionality

The Liblouis Table Editor now supports full "Open With" integration, allowing you to open `.cti`, `.ctb`, and `.utb` files directly from your file manager.

### Features:
- **Command Line Support**: Open files directly from command line
  ```bash
  # Open a single file
  LiblouisTableEditor.exe "path/to/file.cti"
  
  # Open multiple files
  LiblouisTableEditor.exe "file1.cti" "file2.ctb" "file3.utb"
  
  # Show help
  LiblouisTableEditor.exe --help
  ```

- **File Association**: 
  - **Windows**: Right-click any `.cti`, `.ctb`, or `.utb` file and select "Open with Liblouis Table Editor"
  - **Linux**: Files are automatically associated with the application when installed via the `.deb` package

- **Drag and Drop**: Drag table files directly onto the application window to open them

- **Multiple File Support**: Open multiple files simultaneously from command line or file manager

### Supported File Types:
- `.cti` - Liblouis CTI Table files
- `.ctb` - Liblouis CTB Table files  
- `.utb` - Liblouis UTB Table files

## Building from Source

If you want to build the application from source:

1. Install Python 3.8 or later
2. Clone the repository:
   ```
   git clone https://github.com/zendalona/liblouis-table-editor
   cd Liblouis-Table-Editor
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
#### For Windows
4. Run the build script:
   ```
   python windows-build.py
   ```
5. The built application will be in the `dist/LiblouisTableEditor` directory

#### For Linux
   
6. Run the Setup script:
   ```
   sudo python3 setup.py install --install-data=/usr
   ```

## Troubleshooting

If you encounter any issues:

### Liblouis Installation Issues
- **Linux**: If tables or executables are missing, check:
  - `/usr/share/liblouis/tables`
  - `/usr/local/share/liblouis/tables`
  - Run `sudo apt-get install liblouis-bin` if `lou_translate` is not found

- **Windows**: 
  - Ensure Liblouis is properly installed in `C:\Program Files\liblouis`
  - Verify the bin directory is in your system PATH
  - Check that all required files are present

## Usage

After launching the application, you'll be presented with a user-friendly interface where you can:

- Create new Liblouis translation tables
- Edit existing tables
- Test translation rules in real-time
- Export tables in the proper format for use with Liblouis

The editor provides various tools and options to help you define translation rules, test them, and ensure they work as intended.

## License

[MIT License](LICENSE)
