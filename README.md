# Duplicate File Finder

## Overview
This script efficiently identifies and manages duplicate files within a specified directory using multiple approaches. It detects duplicate files based on filename similarity, file size, and cryptographic hash comparisons. The script provides users with three options for handling duplicates: delete, move to trash, or keep them.

## Features
- **Filename Normalization**: Detects minor differences such as trailing numbers in filenames.
- **Fuzzy Matching**: Uses similarity scoring to detect near-duplicate filenames.
- **File Hashing**: Compares file contents using SHA-256 hashing to confirm duplication.
- **Smart Handling of Missing Files**: Skips files that no longer exist to prevent errors.
- **User Options**: Allows users to delete, move to a `Trash` folder, or keep duplicates.

## Installation
1. Clone or download this repository:
   ```sh
   git clone https://github.com/yourusername/duplicate-file-finder.git
   cd duplicate-file-finder
   ```
2. Install dependencies (if necessary):
   ```sh
   pip install --user
   ```

## Usage
Run the script with Python:
```sh
python find_duplicates.py
```

### User Prompt Options:
When duplicate files are found, you will be prompted with the following options:
- `1`: Delete duplicate files (keep one copy)
- `2`: Move duplicate files to a `Trash` folder
- `3`: Keep all duplicates

### Example Output:
```
Duplicate files found:
Set 1:
 - C:\\Users\\username\\path-to-folder\\file1.pdf
 - C:\\Users\\username\\path-to-folder\\file1_2.pdf

Choose an action:
1 - Delete duplicates (keep one)
2 - Move duplicates to Trash (keep one)
3 - Keep all duplicates
Enter your choice (1/2/3): 2
Moved to Trash: C:\\Users\\username\\path-to-folder\\file1_2.pdf
```

## How It Works
1. **Scans Directory**: The script walks through all files in the specified directory.
2. **Groups by File Size**: Files with identical sizes are considered for further comparison.
3. **Compares Hash Values**: Files with matching hashes are flagged as duplicates.
4. **Checks Filename Similarity**: Uses fuzzy matching to catch small variations.
5. **Handles User Choice**: Prompts the user to delete, move, or keep duplicates.

## Error Handling
- If a file is missing when attempting to move or delete, the script logs a warning and continues execution.
- If an unexpected error occurs, the script displays the error message instead of crashing.

## Future Improvements
- Add GUI support for easier interaction.
- Implement multi-threading for faster duplicate detection.
- Support cloud storage directories (Google Drive, Dropbox, etc.).

## License
This project is licensed under the MIT License. Feel free to modify and distribute it.

## Contributing
Contributions are welcome! If you have suggestions or improvements, create a pull request or open an issue on GitHub.

## Author
Developed by **Fabio Dossi**.

