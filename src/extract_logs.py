import sys
import os
import time
from datetime import datetime

#Validate my input date to check whether the format is obeyed or not
def validate_date_format(date_str):
    print("Collecting data...")
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Incorrect date format: '{date_str}'. Expected format: YYYY-MM-DD")

#Function to extract logs from th log file
def extract_logs(date_str, input_file_path, output_file_path):
    os.makedirs(os.path.dirname(output_file_path) or ".", exist_ok=True) 
    
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        matched_lines = [line for line in infile if line.startswith(date_str)]
        outfile.writelines(matched_lines)  

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
