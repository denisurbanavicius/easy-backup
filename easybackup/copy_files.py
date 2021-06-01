import os
import filecmp

from shutil import copy2


def copy_files(root, files, origin, target):
    files_scanned = 0
    files_unchanged = 0
    files_updated = 0
    files_created = 0
    files_skipped = []
    files_not_found = []

    current_path = root.replace(origin, '').lstrip(os.sep)
    for file in files:
        file_path = os.path.join(root, file)
        target_folder = os.path.join(target, current_path)
        target_path = os.path.join(target_folder, file)
        files_scanned += 1
        if os.path.exists(target_path):
            try:
                if filecmp.cmp(file_path, target_path):
                    files_unchanged += 1
                else:
                    copy2(file_path, target_path)
                    files_updated += 1
            except PermissionError:
                files_skipped.append(file_path)
            except FileNotFoundError:
                files_not_found.append(file_path)
            except OSError:
                files_skipped.append(file_path)
        else:
            try:
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                copy2(file_path, target_path)
                files_created += 1
            except PermissionError:
                files_skipped.append(file_path)
            except FileNotFoundError:
                files_not_found.append(file_path)
            except OSError:
                files_skipped.append(file_path)
        # end if
    # end for
    return [files_scanned, files_unchanged, files_updated, files_created, files_skipped, files_not_found]