#!/usr/bin/python3
import os, sys
from pathlib import Path

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3
STATE_DEPENDENT = 4
BENACHRICHTIGEN = False

def find_path(filename):
    for root, dirs, files in os.walk('/'):
        for name in files:
            if name == filename:
                path = os.path.abspath(os.path.join(root, name))
                return path


def find_auth():
    filename = "auth.log"
    var = find_path(filename)
    return var


def words_of_file():
    f_path = find_auth()
    f_time_path = "/srv/checkAuthTime.txt"
    if not Path(f_time_path).is_file():
        f=open(f_time_path, "w+")
        f.write("0 0 0")
        f.close()
    with open(f_time_path, "r") as my_time_file:
        for time_line in my_time_file:
            time_list = time_line.split(" ", 2)
            file_hour, file_minute, file_second = time_list[0], time_list[1], time_list[2]
    with open(f_path, "r") as my_file:
        for line in my_file:
            my_str = line.split(" ", 3)
            month, day, time, others = my_str[0], my_str[1], my_str[2], my_str[3]
            new_time_list = time.split(":", 2)
            my_hour, my_minute, my_second = new_time_list[0], new_time_list[1], new_time_list[2]
            if (my_hour>file_hour) or ((my_hour == file_hour) and (my_minute>file_minute)) or (((my_hour== file_hour) and (my_time_file == file_minute)) and my_second>file_second):
                other_list = others.split(" ", 3)
                rbg, sshd, accept_key, rubbish = other_list[0], other_list[1], other_list[2], other_list[3]
                if accept_key == "Accepted":
                    rubbish_list = rubbish.split(" ", 3)
                    public_word, for_word, name, leftover = rubbish_list[0], rubbish_list[1], rubbish_list[2], rubbish_list[3]
                    if name != "appicing":
                        print(name)
                        global BENACHRICHTIGEN
                        BENACHRICHTIGEN = True
    my_hour = str(my_hour)
    my_minute = str(my_minute)
    my_second = str(my_second)
    t_file = open(f_time_path, "w")
    t_file.seek(0)
    t_file.write(str(my_hour) + " " + str(my_minute) + " " + str(my_second))
    t_file.close()




def main():
    find_path('auth.log')
    words_of_file()
    if BENACHRICHTIGEN:
        sys.exit(STATE_WARNING)
    else:
        sys.exit(STATE_OK)
    

main()

