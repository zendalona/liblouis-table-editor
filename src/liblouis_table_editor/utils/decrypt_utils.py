def decrypt_file_to_string(file_path):
  
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        # Removed error print to reduce console spam - file reading errors handled gracefully
        return "" 
