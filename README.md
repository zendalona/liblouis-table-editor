# Liblouis Table Editor

A graphical editor for Liblouis translation tables. This application provides a user-friendly interface for creating and editing Liblouis braille translation tables.

## Prerequisites

Before installing the Liblouis Table Editor, you must have Liblouis installed on your system.

For detailed installation instructions, see [Liblouis Installation Guide](Prerequisite%20-%20Liblouis%20Installation%20Guide.md).

## Installation

1. Download the latest release of Liblouis Table Editor release.
2. Install to your desired location
3. Run `LiblouisTableEditor.exe` (Windows) or the appropriate executable for your platform

## Building from Source

If you want to build the application from source:

1. Install Python 3.8 or later
2. Clone the repository:
   ```
   git clone https://github.com/yourusername/Liblouis-Table-Editor.git
   cd Liblouis-Table-Editor
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the build script:
   ```
   python build.py
   ```
5. The built application will be in the `dist/LiblouisTableEditor` directory

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

