import datetime
import requests
import time
import re
import os.path 
import glob
import sys



file_lst = glob.glob(str(sys.argv[1]))
start_time_file = str(sys.argv[2])
date_format = '%Y-%m-%d %H:%M:%S'

#  List with unsorted lines from all logs
unsorted_lines= []

#  Send message to telegram
def sendMessage(message):
    TOKEN = "5989022565:AAHO5SOwdlpdMdAFXWXtJxdli4WXy8XyYW8"
    chat_id = "-1001604614259"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json())  # this sends the message


def write_start_script_time(file_location=start_time_file):
    with open(start_time_file, mode='w') as file:
        file.write('last start at %s.' %(datetime.datetime.now() + datetime.timedelta(hours = 0)))


def parse_time_from_line(line):
    date_extract_pattern = "(?:\\d{4})-(?:\\d{2})-(?:\\d{2}).(?:\\d{2}):(?:\\d{2}):(?:\\d{2})" 
    time = re.findall(date_extract_pattern,line)
    if len(time) != 0:
        return time[0]


def compare_date(start_time, end_time):
    if end_time is not None:
        if time.strptime(start_time, '%Y-%m-%d %H:%M:%S') <= time.strptime(end_time, '%Y-%m-%d %H:%M:%S'):
            return True
        else:
            return False


def get_start_time():
    with open(start_time_file) as f_obj:
        contents = f_obj.read()
    return parse_time_from_line(contents)

# open log file and compare last line with start_time and if line time >= start time then add line to 
def open_log(start_time, file):
    with open(file) as f_obj:
        lines = f_obj.readlines()
    # for line in lines:
    #     if compare_date(start_time, parse_time_from_line(line)) == True:
    #         sendMessage(line)
    #         print(line)
    #         time.sleep(5)
    for line in reversed(list(open(file))):
        if compare_date(start_time, parse_time_from_line(line)) == True:
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

# sort inputDateList by time
sorted_line_list = sorted(unsorted_lines, key=lambda x: datetime.datetime.strptime(parse_time_from_line(x), date_format))

for line in sorted_line_list:
    sendMessage(line)

#  Write date and time to start_time file
write_start_script_time()
print(get_start_time())
