import chardet, os

def get_datetime_file_formatted(datetime):
    return datetime.strftime("%Y-%m-%d_%H%M%S")

def get_files_from_location(location_path):
    if os.path.isfile(location_path):
        return [location_path]
    elif os.path.isdir(location_path):
        return [os.path.join(location_path, f) for f in os.listdir(location_path) if os.path.isfile(os.path.join(location_path, f))]
    else:
        return []
    
def remove_non_alphanumeric_to_file(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    with open(file_path, 'r', encoding=result['encoding']) as f:
        text = f.read()
        cleaned_text = ''.join(char for char in text if char.isalnum() or char.isspace())
    with open(file_path, 'w', encoding=result['encoding']) as f:
        f.write(cleaned_text)

        f.truncate()
