import datetime
import requests
import time
import re
import os.path 
import glob
import sys


current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Take current day preffix
file_lst = glob.glob(( str(sys.argv[1]) + current_date + '*.log' ))  # Forming list with files names
start_time_file = str(sys.argv[2])
date_format = '%Y-%m-%d %H:%M:%S'


#  List with unsorted lines from all logs
unsorted_lines= []

#  Send message to telegram
def sendMessage(message):
    TOKEN = "5989022565:AAHO5SOwdlpdMdAFXWXtJxdli4WXy8XyYW8"
    chat_id = "-1001604614259"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json())  # this sends the message to tlg


# Write start time of the script
def write_start_script_time(file_location=start_time_file):
    with open(start_time_file, mode='w') as file:
        file.write('last start at %s.' %(datetime.datetime.now() + datetime.timedelta(hours = 3)))


# Return only time from log line if there is no time format in line return current time
def parse_time_from_line(line):
    date_extract_pattern = "(?:\\d{4})-(?:\\d{2})-(?:\\d{2}).(?:\\d{2}):(?:\\d{2}):(?:\\d{2})" 
    time = re.findall(date_extract_pattern,line)
    if len(time) != 0:
        return time[0]
    else:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# Compare dates start_time and end_time and if end_time >= start_time return True
def compare_date(start_time, end_time):
    if end_time is not None:
        if time.strptime(start_time, '%Y-%m-%d %H:%M:%S') <= time.strptime(end_time, '%Y-%m-%d %H:%M:%S'):
            return True
        else:
            return False


# Get start time from file
def get_start_time():
    with open(start_time_file) as f_obj:
        contents = f_obj.read()
    return parse_time_from_line(contents)


# open log file and compare last line with start_time and if line time >= start time then add line to unsorted list                                  
def open_log(start_time, file):
    with open(file) as f_obj:
         lines = f_obj.readlines()
    for line in reversed(lines):
        if compare_date(start_time, parse_time_from_line(line)) == True:
            if "type=error" in line:
                unsorted_lines.append(line)
                print(line)
        else:
            break


# start parsing file from file list 
for file in file_lst:
    if os.path.exists(file):
        start_time = get_start_time()
        if start_time is not None:
           open_log(start_time, file)  
        else:
            write_start_script_time()


# sort unsorted_lines by time
sorted_line_list = sorted(unsorted_lines, key=lambda x: datetime.datetime.strptime(parse_time_from_line(x), date_format))


# Send messages to telegramm from sorted_line_list
for line in sorted_line_list:
    line.replace('type=error msg=', '')
    line.replace('time=', '')
    sendMessage(line)
    time.sleep(3)

#  Write and print date and time to start_time file
write_start_script_time()
print(get_start_time())
