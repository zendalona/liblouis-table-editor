# style_utils.py

from PyQt5.QtCore import QFile, QTextStream
import os
import sys

def get_asset_path(relative_path):
  
    if getattr(sys, 'frozen', False):

        if hasattr(sys, '_MEIPASS'):

            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(sys.executable)
        
        possible_paths = [

            os.path.join(base_dir, "assets", relative_path),
            os.path.join(base_dir, "_internal", "assets", relative_path),
            os.path.join(base_dir, "liblouis_table_editor", "assets", relative_path),
            os.path.join(base_dir, "_internal", "liblouis_table_editor", "assets", relative_path),

            os.path.join(os.path.dirname(sys.executable), "assets", relative_path),
            os.path.join(os.path.dirname(sys.executable), "_internal", "assets", relative_path),
            os.path.join(os.path.dirname(sys.executable), "liblouis_table_editor", "assets", relative_path),
            os.path.join(os.path.dirname(sys.executable), "_internal", "liblouis_table_editor", "assets", relative_path),
        ]
    else:

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        possible_paths = [
            os.path.join(base_dir, "assets", relative_path),
            os.path.join(os.path.dirname(base_dir), "assets", relative_path),
            os.path.join(base_dir, "src", "liblouis_table_editor", "assets", relative_path),
        ]
    
    found_path = None
    for path in possible_paths:
        if os.path.exists(path):
            found_path = path.replace("\\", "/")  # Normalize path separators
            break
    
    if not found_path:
        # Only print error for missing critical assets, not for debug logging
        return None
    
    return found_path

def get_all_icon_paths():
   
    icon_files = [
        'down-arrow.png',
        'new.png',
        'open.png',
        'save.png',
        'save_as.png',
        'undo.png',
        'redo.png',
        'go_to_entry.png',
        'find.png',
        'find_replace.png',
        'increase_font.png',
        'decrease_font.png',
        'about.png',
        'user_guide.png',
        'report_bug.png',
        'tick.png',
        'liblouis-table-editor-16-0.png',
        'liblouis-table-editor-32-0.png',
        'liblouis-table-editor-48-0.png',
        'liblouis-table-editor-64-0.png',
        'liblouis-table-editor-128-0.png',
        'liblouis-table-editor-256-0.png',
        'liblouis-table-editor.ico',
    ]
    
    icon_paths = {}
    for icon_file in icon_files:
        path = get_asset_path(f'icons/{icon_file}')
        if path:
            icon_paths[icon_file] = path
        # Removed warning print for missing icons
    
    return icon_paths

def get_all_image_paths():
  
    image_files = [
        'background.png',
        'welcome.bmp',
        'wizardsmallicon.bmp',
        'zendalona.png',
    ]
    
    image_paths = {}
    for image_file in image_files:
        path = get_asset_path(f'images/{image_file}')
        if path:
            image_paths[image_file] = path
        # Removed warning print for missing images
    
    return image_paths

def apply_styles(widget):
   
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(sys.executable)
        
        possible_paths = [
            os.path.join(base_dir, "styles.qss"),  
            os.path.join(base_dir, "_internal", "styles.qss"),  
            os.path.join(os.path.dirname(sys.executable), "styles.qss"),  
            os.path.join(os.path.dirname(sys.executable), "_internal", "styles.qss"), 
        ]
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        possible_paths = [
            os.path.join(base_dir, "styles.qss"), 
            os.path.join(base_dir, "src", "styles.qss"), 
        ]
    
    stylesheet_path = None
    for path in possible_paths:
        if os.path.exists(path):
            stylesheet_path = path
            break
    
    if not stylesheet_path:
        print("Error: styles.qss not found in any of the expected locations")
        return False
    
    style_file = QFile(stylesheet_path)
    if not style_file.open(QFile.ReadOnly | QFile.Text):
        print(f"Error: Could not open stylesheet at {stylesheet_path}")
        return False
    
    style_stream = QTextStream(style_file)
    style_sheet = style_stream.readAll()
    style_file.close()
    
    icon_paths = get_all_icon_paths()
    
    replacements_made = 0
    for icon_name, icon_path in icon_paths.items():

        old_patterns = [
            f"url(./liblouis_table_editor/assets/icons/{icon_name})",
            f"url(./src/assets/icons/{icon_name})",
            f"url(assets/icons/{icon_name})",
            f"url(icons/{icon_name})",
            f"./liblouis_table_editor/assets/icons/{icon_name}",
            f"./src/assets/icons/{icon_name}",
            f"assets/icons/{icon_name}",
            f"icons/{icon_name}"
        ]
        
        for old_pattern in old_patterns:
            if old_pattern in style_sheet:
                if old_pattern.startswith("url("):

                    new_pattern = f"url({icon_path})"
                else:

                    new_pattern = icon_path
                style_sheet = style_sheet.replace(old_pattern, new_pattern)
                replacements_made += 1
    
    down_arrow_path = icon_paths.get('down-arrow.png')
    if down_arrow_path:

        down_arrow_patterns = [
            "image: url(./liblouis_table_editor/assets/icons/down-arrow.png);",
            "image: url(./liblouis_table_editor/assets/icons/down-arrow.png)",
            "url(./liblouis_table_editor/assets/icons/down-arrow.png)",
            "./liblouis_table_editor/assets/icons/down-arrow.png"
        ]
        
        replaced = False
        for pattern in down_arrow_patterns:
            if pattern in style_sheet:
                if pattern.startswith("image: url(") and pattern.endswith(");"):

                    new_pattern = f"image: url({down_arrow_path});"
                elif pattern.startswith("image: url("):

                    new_pattern = f"image: url({down_arrow_path})"
                elif pattern.startswith("url("):

                    new_pattern = f"url({down_arrow_path})"
                else:

                    new_pattern = down_arrow_path
                
                style_sheet = style_sheet.replace(pattern, new_pattern)
                replaced = True
                break
        
        if not replaced:
            # Look for down-arrow manually and replace if found
            if "down-arrow" in style_sheet:
                lines = style_sheet.split('\n')
                for i, line in enumerate(lines):
                    if 'down-arrow' in line and "image: url(" in line and "down-arrow.png" in line:
                        old_line = line.strip()
                        new_line = f"  image: url({down_arrow_path});"
                        style_sheet = style_sheet.replace(old_line, new_line)
                        replaced = True
                        break
    
    widget.setStyleSheet(style_sheet)
    
    return True

__all__ = ['apply_styles', 'get_asset_path', 'get_all_icon_paths', 'get_all_image_paths']


