import os
import hashlib
import shutil
import re
from collections import defaultdict
from difflib import SequenceMatcher

def calculate_file_hash(file_path, method='sha256'):
    """Calculate file hash using the specified method."""
    hash_func = hashlib.sha256() if method == 'sha256' else hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except (OSError, IOError) as e:
        print(f"Error reading {file_path}: {e}")
        return None

def normalize_filename(filename):
    """Remove numbers and special characters from filenames for better comparison."""
    name, ext = os.path.splitext(filename)
    name = re.sub(r'\d+$', '', name).strip()  # Remove trailing numbers
    return name.lower() + ext.lower()

def move_to_trash(file, trash_folder):
    """Move a file to the Trash folder, renaming it if necessary."""
    if not os.path.exists(file):
        print(f"Warning: File not found, skipping move: {file}")
        return
    
    base_name = os.path.basename(file)
    dest_path = os.path.join(trash_folder, base_name)
    
    counter = 1
    while os.path.exists(dest_path):
        name, ext = os.path.splitext(base_name)
        new_name = f"{name}_{counter}{ext}"
        dest_path = os.path.join(trash_folder, new_name)
        counter += 1
    
    try:
        shutil.move(file, dest_path)
        print(f"Moved to Trash: {dest_path}")
    except FileNotFoundError:
        print(f"Error: File not found while moving: {file}")
    except Exception as e:
        print(f"Unexpected error while moving {file}: {e}")

def similar_name(file1, file2, threshold=0.85):
    """Determine if two filenames are similar using fuzzy matching after normalization."""
    return SequenceMatcher(None, normalize_filename(file1), normalize_filename(file2)).ratio() >= threshold

def find_duplicate_files(folder_path):
    """Find duplicate files using multiple approaches: hash, rolling hash, and fuzzy matching."""
    size_dict = defaultdict(list)
    hash_dict = defaultdict(list)
    name_dict = defaultdict(list)
    duplicates = []
    
    # First, group files by size and name similarity
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    size_dict[file_size].append(file_path)
                    name_dict[normalize_filename(file)].append(file_path)
            except OSError as e:
                print(f"Error getting size of {file_path}: {e}")
    
    # Identify potential duplicates by normalized filename similarity
    for file_list in name_dict.values():
        if len(file_list) > 1:
            for i in range(len(file_list)):
                for j in range(i + 1, len(file_list)):
                    if similar_name(os.path.basename(file_list[i]), os.path.basename(file_list[j])):
                        duplicates.append([file_list[i], file_list[j]])
    
    # Compare file hashes within same-size groups
    for file_list in size_dict.values():
        if len(file_list) > 1:
            for file in file_list:
                if os.path.exists(file):
                    file_hash = calculate_file_hash(file, method='sha256')
                    if file_hash:
                        hash_dict[file_hash].append(file)
    
    # Collect duplicates from hash comparisons
    for file_list in hash_dict.values():
        if len(file_list) > 1 and file_list not in duplicates:
            duplicates.append(file_list)
    
    # Handle duplicates after gathering all
    if duplicates:
        print("Duplicate files found:")
        for i, file_list in enumerate(duplicates, 1):
            print(f"Set {i}:")
            for file in file_list:
                print(f" - {file}")
            print("\n")
        
        print("Choose an action:")
        print("1 - Delete duplicates (keep one)")
        print("2 - Move duplicates to Trash (keep one)")
        print("3 - Keep all duplicates")
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == "1":
            for file_list in duplicates:
                for file in file_list[1:]:  # Keep one, delete the rest
                    if os.path.exists(file):
                        os.remove(file)
                        print(f"Deleted: {file}")
                    else:
                        print(f"Warning: File not found, skipping deletion: {file}")
        elif choice == "2":
            trash_folder = os.path.join(folder_path, "Trash")
            os.makedirs(trash_folder, exist_ok=True)
            for file_list in duplicates:
                for file in file_list[1:]:
                    move_to_trash(file, trash_folder)
        elif choice == "3":
            print("Keeping all duplicates.")
        else:
            print("Invalid option. No action taken.")
    else:
        print("No duplicate files found.")

if __name__ == "__main__":
    folder_path = r"C:\\Users\\fabio\\Downloads\\Zotero"
    if os.path.exists(folder_path):
        find_duplicate_files(folder_path)
    else:
        print(f"Folder '{folder_path}' does not exist.")
