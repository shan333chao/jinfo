import os
import time
import sys
import subprocess
import psutil

# pid = 20521
pid = sys.argv[-1]
jstack_temp_folder = "/root/jstack_temp"
if os.path.exists(jstack_temp_folder):
    os.popen(f"rm -rf {jstack_temp_folder}/jstack.{pid}_*.txt")
    print("clear old file")
else:
    os.popen("mkdir /root/jstack_temp")


for th in range(0, 100):
    stack = os.popen(
        f"jstack {pid}>{jstack_temp_folder}/jstack.{pid}_{th}.txt")
    time.sleep(0.5)
    print(th)

cat_all = os.popen(
    f"cat {jstack_temp_folder}/jstack.{pid}_*.txt >/root/jstack_{pid}.txt")
print(f"/root/jstack_{pid}.txt    dump complated!\n\n")
print(f"cat   /root/jstack_{pid}.txt |grep -C 15 'com.alpha'")
