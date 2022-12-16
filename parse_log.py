import datetime
import requests
import time
import re
import os.path 

start_time_file = "/home/kazay/start_time"
log_file = "/opt/DemonX_scripts/logs/errors_moisklad_to_fulllog.log"

def sendMessage(message):
    TOKEN = "5989022565:AAHO5SOwdlpdMdAFXWXtJxdli4WXy8XyYW8"
    chat_id = "-1001604614259"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json()) # this sends the message


def write_start_script_time(file_location=start_time_file):
    with open(start_time_file, mode='w') as file:
        file.write('last start at %s.' %(datetime.datetime.now() + datetime.timedelta(hours=3)))


def parse_time_from_line(line):
    date_extract_pattern = "(?:\\d{4})-(?:\\d{2})-(?:\\d{2}).(?:\\d{2}):(?:\\d{2}):(?:\\d{2})" #(?:\\.\\d*)?)(?:(?:-(?:\\d{2}):(?:\\d{2}))?
    time = re.findall(date_extract_pattern,line)
    if len(time) != 0:
        return time[0]


def compare_date(start_time, end_time):
    if end_time != None:
        if time.strptime(start_time, '%Y-%m-%d %H:%M:%S') <= time.strptime(end_time, '%Y-%m-%d %H:%M:%S'):
            return True
        else:
            return False


def get_start_time():
    with open(start_time_file) as f_obj:
        contents = f_obj.read()
    return parse_time_from_line(contents)


def open_log(start_time):
    with open(log_file) as f_obj:
        lines = f_obj.readlines()
    for line in lines:
        if compare_date(start_time, parse_time_from_line(line)) == True:
            sendMessage(line)
            time.sleep(5)


if os.path.exists(start_time_file):
    start_time = get_start_time()
    open_log(start_time)

write_start_script_time()
print(get_start_time())
