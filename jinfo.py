import os
import time
import sys
import subprocess
pid = sys.argv[-1]
stack = os.popen(f"jstack {pid} >/root/{pid}.txt")
while 1:
    if os.path.exists(f"/root/{pid}.txt"):
        print(f"jstack {pid}.txt dump success")
        time.sleep(1)
        break

top_info = subprocess.Popen(
    [f"top", "-Hp", f"{pid}", "n", "3"], stdout=subprocess.PIPE)
out, err = top_info.communicate()

out_info = out.decode('unicode-escape')

lines = out_info.splitlines()
top_arr = []
for i in range(7, len(lines)):
    fix_items = []
    items = lines[i].replace(
        "\x1b(B\x1b[m", "").replace("\x1b[1m", "").split(" ")
    for idx in range(0, len(items)-1):
        res = items[idx].strip()
        if len(res) == 0:
            continue
        fix_items.append(res)
    if len(fix_items) > 0:
        try:
            int(fix_items[0])
        except Exception as ex:
            continue
        top_arr.append(fix_items)


process = os.popen(f"ps -ef |grep '{pid}'")
process_infos = process.readlines()
for line in process_infos:
    print(line)

process_dic = {}
for item in top_arr:
    hex_thread_id = hex(int(item[0]))
    if hex_thread_id in process_dic.keys():
        continue
    if item[8]=="0.0":
        continue
    process_dic[hex_thread_id] = item[0]
    stack = os.popen(f"grep '{hex_thread_id}' /root/{pid}.txt ")
    log = stack.readline()
    print(f"{item[0]} ,{item[8]} {hex_thread_id},{log}")


remove = os.popen(f"rm -rf /root/{pid}.txt")
remove.read()
