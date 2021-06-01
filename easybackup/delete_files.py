import os


def delete_files(root, files, origin, target):
    """
    Here we invert the origin and target on the file logic so we can reverse the sync and delete the extra files
    """
    files_scanned = 0
    files_unchanged = 0
    files_updated = 0
    files_deleted = 0
    files_skipped = []
    files_not_found = []

    current_path = root.replace(target, '').lstrip(os.sep)
    for file in files:
        target_path = os.path.join(root, file)
        origin_folder = os.path.join(origin, current_path)
        origin_path = os.path.join(origin_folder, file)
        files_scanned += 1
        # We delete the file if it doesn't exists on the origin

        if os.path.exists(origin_path):
            # Do nothing
            pass
        else:
            # print(f'File marked for deletion: {target_path}')
            try:
                os.remove(target_path)
                files_deleted += 1
            except PermissionError:
                files_skipped.append(target_path)
            except FileNotFoundError:
                files_not_found.append(target_path)
            except OSError:
                files_skipped.append(target_path)
        # end if
    # end for
    return [files_scanned, files_unchanged, files_updated, files_deleted, files_skipped, files_not_found]


def delete_empty_folders(target):
    print('Deleting empty folders...')
    for root, dirs, files in os.walk(target):
        for folder in dirs:
            full_path = os.path.join(root, folder)
            # Remove folder if empty
            try:
                if not os.listdir(full_path):
                    os.removedirs(full_path)
            except PermissionError:
                print(f'PermissionError on deleting folder: {full_path}')
            except FileNotFoundError:
                print(f'FileNotFoundError on deleting folder: {full_path}')
            except OSError:
                print(f'OSError on deleting folder: {full_path}')
            # end if
        # end for
    # end for
    print('Done.')
