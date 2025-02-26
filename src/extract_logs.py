import sys
import os
import time
import mmap
import datetime
from datetime import datetime as dt
from pathlib import Path
import multiprocessing as mp
from typing import List, Tuple

#Validate my input date to check whether the format is obeyed or not
def validate_date_format(date_str):
    print("Collecting data...")
    try:
        dt.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Incorrect date format: '{date_str}'. Expected format: YYYY-MM-DD")

def find_date_boundaries(mm: mmap.mmap, file_size: int) -> Tuple[str, str]:
    mm.seek(0)
    first_line = mm.readline().decode('utf-8', errors='ignore').strip()
    first_date = first_line[:10] if len(first_line) >= 10 else "0000-00-00"
    
    pos = max(0, file_size - 100000)  
    mm.seek(pos)
    mm.readline() 
    last_date = "9999-99-99"
    for _ in range(100):
        line = mm.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            break
        if len(line) >= 10 and line[4] == '-' and line[7] == '-':
            last_date = line[:10]
    return first_date, last_date

def find_lines_for_date(chunk: Tuple[int, int], file_path: str, target_date: str) -> List[str]:
    results = []
    start, end = chunk
    with open(file_path, 'rb') as f:
        f.seek(start)
        if start > 0:
            f.readline()
        current_pos = f.tell()
        while current_pos < end:
            try:
                line = f.readline().decode('utf-8', errors='ignore').strip()
                current_pos = f.tell()
                if line.startswith(target_date):
                    results.append(line)
            except Exception:
                current_pos = f.tell()
    return results


#Function to extract logs from the log file
def extract_logs(date_str, input_file_path, output_file_path,
                              num_processes: int = 4):
    file_size = os.path.getsize(input_file_path)
    with open(input_file_path, 'rb') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        min_date, max_date = find_date_boundaries(mm, file_size)
        mm.close()
    
    # Spliting the file into nearly equal chunks.
    chunk_size = file_size // num_processes
    chunks = []
    for i in range(num_processes):
        start = i * chunk_size
        end = file_size if i == num_processes - 1 else (i + 1) * chunk_size
        chunks.append((start, end))
    
    pool = mp.Pool(processes=num_processes)
    results = pool.starmap(find_lines_for_date, [(chunk, input_file_path, date_str) for chunk in chunks])
    pool.close()
    pool.join()
    
    # Flattening and sorting the results.
    extracted_lines = [line for sublist in results for line in sublist]
    extracted_lines.sort()
    
    os.makedirs(os.path.dirname(output_file_path) or ".", exist_ok=True)
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in extracted_lines:
            outfile.write(line + "\n")

def main():
    #Checking if we are running the file in command line or not
    if len(sys.argv) != 2:
        print("Usage: python extract_logs.py YYYY-MM-DD")
        sys.exit(1)
    
    date_str = sys.argv[1]
    
    try:
        validate_date_format(date_str)
    except ValueError as ve:
        print(ve)
        sys.exit(1)
    
    input_file_path = '../logs_2024.log'  
    output_file_path = f"../output/output_{date_str}.txt"
    
    start_time = time.time()
    
    try:
        extract_logs(date_str, input_file_path, output_file_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
    total_time = time.time() - start_time
    
    #Printing the time taken to run the log seach script
    print(f"Log entries for {date_str} have been written to {output_file_path}")
    print(f"Total running time: {total_time:.2f} seconds")

if __name__ == '__main__':
    main()
