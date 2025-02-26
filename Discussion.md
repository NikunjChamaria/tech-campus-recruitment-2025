# Log Extraction Script Documentation

**Author:** Nikunj Chamaria  
**Student ID:** 2021UCH1896  

## Solutions Considered

### 1. Using Regex for Date Matching
- Initially, I considered using regular expressions to match log entries based on the date format.
- However, regex can be complex and may not handle invalid date formats effectively.

### 2. Using `strptime` for Date Validation and String Matching
- I opted for `datetime.strptime` to validate date formats before processing the logs.
- This ensures that only correctly formatted dates proceed to the extraction step.
- The approach is simpler and more reliable compared to regex validation.

## Final Solution Summary

I chose to use `datetime.strptime` for validating the date format and a list comprehension to filter log entries based on the given date. This approach ensures:
- Proper input validation before processing.
- Efficient filtering using string matching.
- Clear and maintainable code structure.

## Steps to Run

### Prerequisites
- Ensure you have Python installed (version 3.x recommended).
- The log file (`logs_2024.log`) should be available in the same directory as the script.

### Execution Steps
1. Open a terminal or command prompt.
2. Navigate to the directory containing the script.
3. Run the script with the required date parameter:
   ```sh
   python extract_logs.py YYYY-MM-DD
   ```
   Replace `YYYY-MM-DD` with the desired date.
4. The script will create an output file in the `output/` directory, containing all log entries from the specified date.
5. Check the console output for the processing time and the output file path.

### Example Run
```sh
python extract_logs.py 2024-02-26
```
**Expected Output:**
```
Collecting data...
Log entries for 2024-02-26 have been written to output/output_2024-02-26.txt
Total running time: 0.03 seconds
```

### Error Handling
- If an incorrect date format is provided, the script will print an error message and exit.
- If any other issue occurs (e.g., missing log file), an error message will be displayed.
