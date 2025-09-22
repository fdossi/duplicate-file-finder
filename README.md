# Duplicate File Finder

## Overview

This Python script efficiently identifies and manages duplicate files within a specified directory. It uses a comprehensive approach that combines content-based SHA-256 hashing for exact duplicates with advanced fuzzy filename matching for near-duplicates. The script is interactive, guiding you through a scan and presenting a consolidated list of duplicates. You can then choose to delete them, move them to a "Trash" folder, or keep them. It also includes a **dry-run mode** for safe previews of all actions.

-----

## Features

  * **Comprehensive Detection**: Combines content-based SHA-256 hashing for exact duplicates with an advanced fuzzy filename matching algorithm for near-duplicates.
  * **Performance Optimized**: Utilizes **multiprocessing** to calculate file hashes in parallel, significantly reducing scan time on large directories.
  * **Interactive Prompts**: Guides the user by asking for the folder path and run options directly in the terminal, eliminating the need to edit the code.
  * **Dry-Run Mode**: Allows you to run the scan and preview all actions (deleting or moving) without making any permanent changes to your files.
  * **Smart Handling**: Gracefully skips symbolic links and handles permission errors to prevent the script from crashing.
  * **User Options**: Provides clear choices to delete files, move them to a `Trash` folder, or leave them untouched.

-----

## How It Works

1.  **Path and Mode Input**: The script prompts the user to enter the directory path and to select whether to run in dry-run mode.
2.  **Initial Scan**: It walks through all files in the specified directory, initially grouping them by file size.
3.  **Hash Comparison**: For groups with multiple files, the script calculates the **SHA-256 hash** of each file's content using multiple processes. Files with identical hashes are flagged as exact duplicates.
4.  **Filename Matching**: It then performs a separate scan to identify files with similar normalized filenames using an improved fuzzy matching algorithm.
5.  **Consolidated Report**: The script combines the results from both the hash and name similarity checks into a single, comprehensive list.
6.  **User Action**: Finally, it prompts the user to select an action for handling the detected files. If in **dry-run mode**, the script will only display the actions it would take without executing them.

-----

## Installation

1.  Clone or download this repository:
    ```sh
    git clone https://github.com/yourusername/duplicate-file-finder.git
    cd duplicate-file-finder
    ```
2.  This script uses the standard Python library, but for improved name similarity detection, you can optionally install the `fuzzywuzzy` library.
    ```sh
    pip install fuzzywuzzy
    ```

-----

## Usage

Run the script with Python. It will prompt you for all the necessary information.

```sh
python find_duplicates.py
```

### Example Interaction

```
Please enter the folder path to scan for duplicates (or 'exit' to quit): C:\Users\username\path-to-folder
Run in dry-run mode to only preview actions? (yes/no): yes
Scanning for files...
Comparing file hashes...
Checking for similar filenames...

Duplicate files found:
Set 1:
 - C:\Users\username\path-to-folder\file1.pdf
 - C:\Users\username\path-to-folder\file1_2.pdf
 - C:\Users\username\path-to-folder\file1(copy).pdf

--- DRY-RUN MODE: No files will be deleted or moved. ---
```

-----

## Future Improvements

  * Add a graphical user interface (GUI) for a more intuitive user experience.
  * Provide more detailed reports or logs of the actions taken.
  * Support cloud storage directories (Google Drive, Dropbox, etc.).

-----

## License

This project is licensed under the MIT License. 

-----

## Contributing

Contributions are welcome\! If you have suggestions or improvements, please create a pull request or open an issue on GitHub.

-----

## Author

Developed by **Fabio Dossi**.