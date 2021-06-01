
def compile_results(results, job, delete_mode=False):
    files_scanned = 0
    files_unchanged = 0
    files_updated = 0
    files_created = 0
    files_skipped = []
    files_not_found = []

    for el in results:
        files_scanned += el[0]
        files_unchanged += el[1]
        files_updated += el[2]
        files_created += el[3]
        files_skipped.extend(el[4])
        files_not_found.extend(el[5])
    print(f"{files_scanned} files scanned.")
    if delete_mode:
        print(f"{files_created} files deleted.")
    else:
        print(f"{files_created} files created.")
    print(f"{files_updated} files updated.")
    print(f"{files_unchanged} files unchanged.")
    total_skipped = len(files_skipped)
    if total_skipped > 0:
        print(f"{total_skipped} files skipped for lack of permissions.")
    total_not_found = len(files_not_found)
    if total_not_found > 0:
        print(f"{total_not_found} files failed (error).")

    file = open(f'skipped-{job}.log', 'w')
    for skipped in files_skipped:
        file.write(skipped)
        file.write('\n')

    file = open(f'error-{job}.log', 'w')
    for error in files_not_found:
        file.write(error)
        file.write('\n')
