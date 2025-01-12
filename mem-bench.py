#!/usr/bin/python

import pexpect
from pexpect import pxssh
import threading
import time
import os
import datetime

data_dir = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.mkdir(data_dir)
all_logfile = open(f"{data_dir}/all-log.txt", "w+")

start_ts = time.time()


def ts():
    return int((time.time() - start_ts) * 1000000)


def login(log_filename):
    ssh = pxssh.pxssh(
        options={"StrictHostKeyChecking": "no", "UserKnownHostsFile": "/dev/null"},
        echo=True,
        timeout=10000,
        encoding="utf-8",
    )
    ssh.logfile = open(f"{data_dir}/{log_filename}", "w+")
    ssh.login(server="localhost", username="root", password="root", port=7722)
    return ssh


def run_vm(vm_id):
    ssh = login(f"vm-{vm_id}-log.txt")
    ssh.sendline(
        "./lkvm-static run -c1 --console virtio --cove-vm -p 'earlycon=sbi console=hvc1 nokaslr' -k ./Image --virtio-transport=pci"
    )
    ssh.expect("/ # ")
    all_logfile.write(f"{ts()} [VM-{vm_id}] VM has finished booting\n")
    time.sleep(30)
    all_logfile.write(f"{ts()} [VM-{vm_id}] Starting a program\n")
    # ssh.sendline("/host/root/gtest")
    ssh.sendline("python")

    while True:
        all_logfile.write(f"{ts()} [VM-{vm_id}] {ssh.readline()}")
        all_logfile.flush()


def run_observer_vm():
    ssh = login("vm-observer-log.txt")
    ssh.sendline("./mem_usage")
    while True:
        all_logfile.write(f"{ts()} [VM-Observer] {ssh.readline()}")
        all_logfile.flush()


host = pexpect.spawn("./build run", encoding="utf-8", timeout=10000)
host.logfile = open(f"{data_dir}/host-log.txt", "w+")
host.expect("buildroot login: ")

for vm_id in range(2):
    threading.Thread(target=run_vm, args=(vm_id,)).start()

threading.Thread(target=run_observer_vm, args=()).start()

while True:
    all_logfile.write(f"{ts()} [Host] {host.readline()}")
    all_logfile.flush()
