import os
import time
import threading

from copy_files import copy_files
from delete_files import delete_files, delete_empty_folders
from results import compile_results
from utils import load_config

from multiprocessing import Pool
from tqdm import tqdm

# TODO: Fix bug that rewrites skipped and error log files on each use
# TODO: Add log folder on config


def sync(origin, target, job, cpu_cores):
    walk_buffer = []

    print(f'\nLoading file list for {origin} -> {target}')
    for root, dirs, files in os.walk(origin):
        walk_buffer.append((root, files, origin, target))
    print('File list loaded.')

    print('Copying files...')
    pool = Pool(cpu_cores)
    results = pool.starmap(copy_files, tqdm(walk_buffer, total=len(walk_buffer)), chunksize=10)
    pool.close()
    pool.join()
    print("Done.")

    compile_results(results, job)


def delete_extras(origin, target, job, cpu_cores):
    walk_buffer = []

    print(f'\nLoading file deletion list for {origin} -> {target}')
    for root, dirs, files in os.walk(target):
        walk_buffer.append((root, files, origin, target))
    print('File list loaded.')

    print('Deleting files...')
    pool = Pool(cpu_cores)
    results = pool.starmap(delete_files, tqdm(walk_buffer, total=len(walk_buffer)), chunksize=10)
    pool.close()
    pool.join()
    print("Done.")

    compile_results(results, job, delete_mode=True)

    delete_empty_folders(target)


def run():
    start = time.time()

    config = load_config()
    sys_config = config['system']
    parallel_jobs = (sys_config['parallel_jobs'] == "True")
    full_sync = (sys_config['full_sync'] == "True")
    max_cpu_cores = int(sys_config['max_cpu_cores'])
    num_of_tasks = len(config.sections()) - 1

    if parallel_jobs:
        cpu_cores = max_cpu_cores // num_of_tasks
    else:
        cpu_cores = max_cpu_cores

    if parallel_jobs:
        thread_list = []
        for job in config.sections():
            if job == 'system':
                continue

            bkp_obj = config[job]
            job_thread = threading.Thread(target=sync, args=(bkp_obj['origin'], bkp_obj['target'], job, cpu_cores))
            thread_list.append(job_thread)
            if full_sync:
                delete_thread = threading.Thread(target=delete_extras, args=(bkp_obj['origin'], bkp_obj['target'], job, cpu_cores))
                thread_list.append(delete_thread)

        for job_thread in thread_list:
            job_thread.start()

        for job_thread in thread_list:
            job_thread.join()
    else:
        for job in config.sections():
            if job == 'system':
                continue

            bkp_obj = config[job]
            sync(**bkp_obj, job=job, cpu_cores=cpu_cores)
            if full_sync:
                delete_extras(**bkp_obj, job=job, cpu_cores=cpu_cores)

    end = time.time()
    minutes, seconds = divmod(end - start, 60)
    print("Total time: {:0>2}:{:05.2f}".format(int(minutes), seconds))


if __name__ == '__main__':
    run()
