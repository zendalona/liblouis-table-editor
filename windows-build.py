import PyInstaller.__main__
import os
import sys
import shutil
import time

def clean_build_dirs():
    
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
    
    clean_build_dirs()
    
    main_script = os.path.abspath('src/liblouis_table_editor/__main__.py')
    
    assets_dir = os.path.abspath('src/liblouis_table_editor/assets')
    
    styles_path = os.path.abspath('src/liblouis_table_editor/styles.qss')
    
    if not os.path.exists(styles_path):
        print(f"Error: styles.qss not found at {styles_path}")
        sys.exit(1)
    
    print(f"Using styles.qss from: {styles_path}")
    
    icon_path = os.path.abspath('src/liblouis_table_editor/assets/icons/icon.ico')
    
    args = [
        main_script,
        '--name=LiblouisTableEditor',
        '--windowed',  
        '--clean',     
        '--noconfirm',  
        '--distpath=dist',  
        '--workpath=build',  
        '--specpath=build',  
        '--hidden-import=PyQt5',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=subprocess',  
        '--hidden-import=sys',
        '--hidden-import=os',
        f'--add-data={assets_dir};assets',  
        f'--add-data={styles_path};.',  
        '--noconsole',  
        f'--icon={icon_path}',  
    ]
    
    PyInstaller.__main__.run(args)
    
    dist_dir = os.path.join('dist', 'LiblouisTableEditor')
    styles_dest = os.path.join(dist_dir, 'styles.qss')
    
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
