# asset_utils.py


from .ApplyStyles import get_asset_path, get_all_icon_paths, get_all_image_paths

def get_icon_path(icon_name):
   
    path = get_asset_path(f'icons/{icon_name}')
    if path:
        return path
    
    return get_asset_path('icons/about.png')  

def get_image_path(image_name):
   
    path = get_asset_path(f'images/{image_name}')
    if path:
        return path
    
    return None

def get_app_icon_path():
 
    icon_names = [
        'liblouis-table-editor.ico',
        'liblouis-table-editor-64-0.png',
        'liblouis-table-editor-48-0.png',
        'liblouis-table-editor-32-0.png',
        'about.png' 
    ]
    
    for icon_name in icon_names:
        path = get_icon_path(icon_name)
        if path:
            return path
    
    return None

def get_common_icons():
    
    return {
        'success': 'tick.png',
        'error': 'tick.png',  
        'info': 'about.png',  
        'warning': 'about.png',  
        'new': 'new.png',
        'open': 'open.png',
        'save': 'save.png',
        'save_as': 'save_as.png',
        'undo': 'undo.png',
        'redo': 'redo.png',
        'find': 'find.png',
        'find_replace': 'find_replace.png',
        'go_to_entry': 'go_to_entry.png',
        'increase_font': 'increase_font.png',
        'decrease_font': 'decrease_font.png',
        'about': 'about.png',
        'user_guide': 'user_guide.png',
        'report_bug': 'report_bug.png',
    }

def get_icon_for_toast(icon_type):
    
    common_icons = get_common_icons()
    icon_name = common_icons.get(icon_type, 'about.png')
    return get_icon_path(icon_name)

def get_zendalona_logo_path():
    """Return the path to the zendalona.png logo if available."""
    return get_image_path('zendalona.png')

__all__ = [
    'get_icon_path', 
    'get_image_path', 
    'get_app_icon_path', 
    'get_common_icons', 
    'get_icon_for_toast',
    'get_zendalona_logo_path',
] 
