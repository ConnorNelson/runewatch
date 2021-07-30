#!/usr/bin/env python

import sys
import os
import re
import time
import datetime
import subprocess
import argparse

import pyshark


def notify(cmd, delay):
    global previous_time

    subprocess.run(
        cmd,
        shell=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    previous_time = time.time() + delay


def main():
    global previous_time

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", required=True, help="listen on network interface")
    parser.add_argument("-w", "--world", required=True, type=int, help="RuneScape world")
    parser.add_argument("-c", "--command", required=True, help="command to run when notifying")
    parser.add_argument("-n", "--notify", help="regex to detect notify")
    parser.add_argument("-s", "--success", help="regex to detect success")
    parser.add_argument("-t", "--timeout", type=int, help="notify if success not detected (seconds)")
    parser.add_argument("-d", "--delay", type=int, default=0, help="delay further notifications (seconds)")

    args = parser.parse_args()

    host = f"world{args.world}.runescape.com"
    capture = pyshark.LiveCapture(
        interface=args.interface, bpf_filter=f"tcp and host {host}"
    )

    start = time.time()
    previous_time = time.time()
    previous_success = time.time()
    success = 0

    for packet in capture.sniff_continuously():
        if not hasattr(packet.tcp, "payload"):
            continue
        payload = bytes.fromhex(packet.tcp.payload.replace(":", ""))

        stats = {
            "success": success,
            "success/hr": int(success / (previous_time - start) * 3600)
            if previous_time - start
            else 0,
            "time-since-success": str(
                datetime.timedelta(seconds=int(time.time() - previous_success))
            ),
            "total-time": str(datetime.timedelta(seconds=int(time.time() - start))),
        }
        stats = "  ".join(f"{attr}: {val}" for attr, val in stats.items())
        print("\r" + " " * 80 + "\r" + stats, end="", flush=True)

        if args.timeout and time.time() > previous_time + args.timeout:
            notify(args.command, args.delay)

        if args.notify:
            match = re.search(args.notify.encode(), payload)
            if match:
                notify(args.command, args.delay)

        if args.success:
            match = re.search(args.success.encode(), payload)
            if match:
                success += 1
                previous_time = time.time()
                previous_success = time.time()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.close()  # No way to cleanly exit pyshark
