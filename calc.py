import threading
import os
video_path = "./videos"
files = os.listdir(video_path)
thread_num = 1
i = 0
for i in range(thread_num):
    open("videos-%d.txt" % (i), "w").write('')
for file in files:
    if file.endswith('.mp4'):
        open("videos-%d.txt" % (i % thread_num), "a").write(file + '\n')
        i += 1
"""
threads = []


def run_main(id):
    os.system("python3 main.py videos-%d.txt > out-%d.txt" % (id, id))


for i in range(thread_num):
    thread = threading.Thread(target=run_main, args=(i,))
    thread.start()
    threads.append(thread)

for p in threads:
    p.join()
"""
