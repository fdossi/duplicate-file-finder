import os
import hashlib
import shutil
import re
from collections import defaultdict
from difflib import SequenceMatcher
from multiprocessing import Pool, cpu_count

def calculate_file_hash(file_path, method='sha256'):
    """Calculate file hash using the specified method."""
    if not os.path.exists(file_path) or os.path.islink(file_path):
        return None
    
    hash_func = hashlib.sha256() if method == 'sha256' else hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except (OSError, IOError, PermissionError) as e:
        print(f"Error reading {file_path}: {e}")
        return None

def normalize_filename(filename):
    """Remove numbers and special characters from filenames for better comparison."""
    name, ext = os.path.splitext(filename)
    name = re.sub(r'\d+$', '', name).strip()
    return name.lower() + ext.lower()

def similar_name(file1, file2, threshold=0.85):
    """Determine if two filenames are similar using fuzzy matching after normalization."""
    return SequenceMatcher(None, normalize_filename(file1), normalize_filename(file2)).ratio() >= threshold

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
    except PermissionError:
        print(f"Error: Permission denied while trying to move {file}.")
    except Exception as e:
        print(f"Unexpected error while moving {file}: {e}")

def find_duplicate_files(folder_path):
    """Find duplicate files by size, then by hash."""
    size_dict = defaultdict(list)
    duplicates = []
    
    print("Scanning for files...")
    # Group files by size
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.islink(file_path):
                try:
                    file_size = os.path.getsize(file_path)
                    size_dict[file_size].append(file_path)
                except OSError as e:
                    print(f"Error getting size of {file_path}: {e}")
    
    # Check for exact duplicates using hash
    potential_duplicates = [files for files in size_dict.values() if len(files) > 1]
    
    print("Comparing file hashes...")
    with Pool(cpu_count()) as p:
        for file_list in potential_duplicates:
            hashes = p.map(calculate_file_hash, file_list)
            hash_dict = defaultdict(list)
            for i, h in enumerate(hashes):
                if h:
                    hash_dict[h].append(file_list[i])
            
            for file_group in hash_dict.values():
                if len(file_group) > 1:
                    duplicates.append(file_group)
    
    return duplicates

def find_similar_names(folder_path, existing_duplicates):
    """Find files with similar names using fuzzy matching, excluding already found exact duplicates."""
    name_dict = defaultdict(list)
    similar_names = []
    existing_dup_files = {f for sublist in existing_duplicates for f in sublist}

    print("Checking for similar filenames...")
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path not in existing_dup_files:
                name_dict[normalize_filename(file)].append(file_path)

    for file_list in name_dict.values():
        if len(file_list) > 1:
            # Simple pairwise comparison for now
            for i in range(len(file_list)):
                for j in range(i + 1, len(file_list)):
                    if similar_name(os.path.basename(file_list[i]), os.path.basename(file_list[j])):
                        similar_names.append([file_list[i], file_list[j]])
    
    return similar_names

def handle_duplicates(duplicates, folder_path):
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
                for file in file_list[1:]:
                    if os.path.exists(file):
                        try:
                            os.remove(file)
                            print(f"Deleted: {file}")
                        except PermissionError:
                            print(f"Error: Permission denied while trying to delete {file}.")
                        except Exception as e:
                            print(f"Unexpected error while deleting {file}: {e}")
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

def main():
    while True:
        folder_path = input("Please enter the folder path to scan for duplicates (or 'exit' to quit): ").strip()
        if folder_path.lower() == 'exit':
            break

        if not os.path.exists(folder_path):
            print(f"Error: Folder '{folder_path}' does not exist. Please try again.")
            continue
        
        # Run duplicate detection logic
        exact_duplicates = find_duplicate_files(folder_path)
        similar_names_duplicates = find_similar_names(folder_path, exact_duplicates)
        
        # Combine the lists and handle duplicates
        all_duplicates = exact_duplicates + similar_names_duplicates
        
        handle_duplicates(all_duplicates, folder_path)
        
        break


if __name__ == "__main__":
    main()