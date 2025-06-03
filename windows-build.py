import PyInstaller.__main__
import os
import sys
import shutil
import time

def clean_build_dirs():
    """Clean build and dist directories with retry logic"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
            except PermissionError:
                print(f"Waiting for {dir_name} directory to be released...")
                time.sleep(2)  # Wait 2 seconds
                try:
                    shutil.rmtree(dir_name)
                except PermissionError:
                    print(f"Could not remove {dir_name} directory. Please close any applications using it and try again.")
                    sys.exit(1)

def build_app():
    # Clean build directories first
    clean_build_dirs()
    
    # Get the absolute path to the main script
    main_script = os.path.abspath('src/main.py')
    
    # Get the absolute path to assets directory
    assets_dir = os.path.abspath('src/assets')
    
    # Get the absolute path to styles.qss
    styles_path = os.path.abspath('src/styles.qss')
    
    # Verify files exist
    if not os.path.exists(styles_path):
        print(f"Error: styles.qss not found at {styles_path}")
        sys.exit(1)
    
    print(f"Using styles.qss from: {styles_path}")
    
    # Get the absolute path to the icon file
    icon_path = os.path.abspath('src/assets/icons/icon.ico')
    
    # Define PyInstaller arguments
    args = [
        main_script,
        '--name=LiblouisTableEditor',
        '--windowed',  # For GUI applications
        '--clean',     # Clean PyInstaller cache
        '--noconfirm',  # Replace existing build without asking
        '--distpath=dist',  # Output directory
        '--workpath=build',  # Working directory
        '--specpath=build',  # Spec file directory
        '--hidden-import=PyQt5',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=subprocess',  # Add subprocess for testing window
        '--hidden-import=sys',
        '--hidden-import=os',
        f'--add-data={assets_dir};assets',  # Include assets directory
        f'--add-data={styles_path};.',  # Include styles.qss in root directory
        '--noconsole',  # Prevent console window from appearing
        f'--icon={icon_path}',  # Set the application icon using absolute path
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    # Verify the build
    dist_dir = os.path.join('dist', 'LiblouisTableEditor')
    styles_dest = os.path.join(dist_dir, 'styles.qss')
    
    # Check if styles.qss exists in the build
    if os.path.exists(styles_dest):
        print(f"Success: styles.qss was copied to {styles_dest}")
    else:
        print(f"Warning: styles.qss was not found in the build at {styles_dest}")
        # List contents of dist directory to help debug
        print("\nContents of dist directory:")
        for root, dirs, files in os.walk(dist_dir):
            print(f"\nDirectory: {root}")
            for file in files:
                print(f"  - {file}")

if __name__ == '__main__':
    build_app() 