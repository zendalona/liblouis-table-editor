# Liblouis Table Editor

<<<<<<< HEAD
Liblouis Table Editor is an intuitive, accessible, and user-friendly tool designed to simplify the creation, editing, and management of translation tables used by the Liblouis Braille translation system. This project was developed as part of the Google Summer of Code (GSoC) 2024 by [Riya Jain](https://github.com/jriyyya) under the Mentorship of [Nalin Sathyan](https://github.com/nalin-x-linux), [Samuel Thibault](https://github.com/sthibaul) and K Sathaseelan initiative with the aim of providing both novice and experienced users with a more straightforward way to interact with and manage Liblouis tables.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [User Interface Overview](#user-interface-overview)
- [Implementation Details](#implementation-details)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

Liblouis is a library that provides braille translation and back-translation. It is used by various screen readers and braille translation tools. However, creating and managing the translation tables used by Liblouis can be a complex and error-prone process. The Liblouis Table Editor aims to simplify this process by offering an intuitive graphical interface that allows users to create, modify, and test translation tables without needing to manually edit text files.

This project was developed during the Google Summer of Code 2024 by [Riya Jain](https://github.com/jriyyya) under the Mentorship of [Nalin Sathyan](https://github.com/nalin-x-linux), [Samuel Thibault](https://github.com/sthibaul) and K Sathaseelan, and it addresses the need for a more accessible and user-friendly way to interact with Liblouis translation tables.

## Features

- **Graphical User Interface (GUI):** An easy-to-use GUI for creating and editing Liblouis translation tables.
- **Accessibility:** The editor is designed to be accessible, ensuring that users with different abilities can effectively use the tool.
- **Real-Time Editing and Validation:** The tool provides real-time feedback and validation, helping users avoid common errors in table creation.
- **Multi-Version Support:** The editor can handle multiple versions of Liblouis, ensuring compatibility with different environments.
- **Testing Environment:** Users can test their tables within the editor to ensure correct functionality before deploying them.
- **Tab-Based Interface:** Work on multiple tables simultaneously using a tabbed interface. Each table opens in its own tab, allowing you to easily switch between them.
- **Session Persistence:** The editor automatically saves your work. If you close the program and reopen it, the editor will restore your session, allowing you to continue from where you left off.

## Installation

### Prerequisites

- **Python 3.x**: The editor is developed in Python, so you'll need Python installed on your system.
- **PyQt5**: The GUI is built using PyQt5, which you can install using pip:

```bash
pip3 install PyQt5
```

### Cloning the Repository
Clone the repository from GitHub: 
```bash
git clone https://github.com/zendalona/liblouis-table-editor.git
cd liblouis-table-editor
```

### Running the Application


#### Running in Windows
To start the application, run
```bash
mingw32-make
```
command, which is a build tool commonly used in development environments that rely on the MinGW (Minimalist GNU for Windows) toolchain


#### For running it in Linux/WSL

1. To start the application run
```bash
make run
```


## Usage

After launching the application, you'll be presented with a user-friendly interface where you can start creating or editing Liblouis tables. The editor provides various tools and options to help you define translation rules, test them, and ensure they work as intended.

### Creating a New Table

1. Click on `File > New` to create a new translation table.
2. Use the interface to define characters, rules, and exceptions.
3. Test your table using the built-in testing tools.

### Editing an Existing Table

1. Click on `File > Open` to open an existing Liblouis table.
2. Modify the table as needed using the provided tools.
3. Save your changes using `File > Save`.

## User Interface Overview

The user interface is divided into several sections:

- **Menu Bar:** Provides options to create, open, save, and close files, as well as access help and settings.
- **Table Editor:** The main area where you can define and edit translation rules.
- **Table Preview:** A existing table is loaded into the table preview, where each entry can has the following command - Edit, Duplicate, Delete.
- **Testing Panel:** A panel where you can input text and see the corresponding braille output based on the currently loaded table.
- **Output Window:** Displays messages, errors, and logs to help you debug and refine your table.

## Implementation Details

The Liblouis Table Editor is implemented primarily in Python using the PyQt5 library for the graphical interface. The application is designed to be modular, making it easy to extend and maintain.

Key components include:

- **Main Application Window:** Handles the overall layout and interactions within the application.
- **Table Editor Module:** Manages the creation, editing, and validation of translation tables.
- **Testing Environment:** Provides a real-time interface for testing tables against sample inputs.

### Future Enhancements

- **Localization:** Adding support for multiple languages to make the editor accessible to a broader audience.
- **Advanced Testing Features:** Implementing more sophisticated testing scenarios to handle complex translation rules.
- **Plugin Support:** Allowing users to extend the editor with custom plugins for additional functionality.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue on GitHub. If you would like to contribute code, please fork the repository and submit a pull request.

### Guidelines

- Ensure that your code adheres to the project's coding standards.
- Write clear, concise commit messages.
- Include comments and documentation for new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

This project was developed as part of the Google Summer of Code 2024. Special thanks to the Zendalona and the Liblouis community for their support and feedback throughout the development process.
=======
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
>>>>>>> liblouis/main

