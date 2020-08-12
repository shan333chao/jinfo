import os
import time
import sys
import subprocess
import psutil
import datetime

key = sys.argv[-1]
if len(key)==0:
    print("param key is empty!!!")
    exit()

process_jstack_folder = "/root/jstack_process"
if os.path.exists(process_jstack_folder):
    os.popen(f"rm -rf {process_jstack_folder}/jstack.*")
    print("clear old file")
else:
    os.popen(f"mkdir {process_jstack_folder}")


def get_pid(key):
    process_info = os.popen(f"ps -ef |grep '{key}' ")
    process_lines = process_info.readlines()
    monitor_process = ""
    pid = 0
    for l in process_lines:
        if "java" in l:
            monitor_process = l
            pid = int(monitor_process[4:14].strip())
            break
    return pid


pid = 0
pp = None
while 1:
    now_time= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    npid = get_pid(key)
    if not psutil.pid_exists(npid):
        print(f"{now_time} process {key} is not exist!")
        npid = 0
        time.sleep(30)
        continue
    
    if pid != npid:
        pp = psutil.Process(pid=npid)
        pid = npid
        print(f"{now_time} pid changed {npid}")

    process_cpu_percent = pp.cpu_percent()
    if process_cpu_percent > 100:
        mem = pp.memory_percent()
        current_timestap = int(time.time())
        stack = os.popen(
            f"jstack {npid}>{process_jstack_folder}/jstack.{npid}_{current_timestap}.txt")
        print(
            f"{now_time} cpu:{process_cpu_percent} mem:{round(mem,2)}% jstack {process_jstack_folder}/jstack.{npid}_{current_timestap}.txt")
    time.sleep(30)
