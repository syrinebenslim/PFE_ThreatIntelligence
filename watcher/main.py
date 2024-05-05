# This is a sample Python script.
import os

import paramiko

from watcher.feed_watcher import FeedWatcher


# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():
    # Use a breakpoint in the code line below to debug your script.

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname="192.168.18.128", username="sftpuser", port=22, password="Zooming1983")
    print(os.path.abspath("."))
    stdin, stdout, stderr = ssh_client.exec_command("echo $HOME")
    print(stdout.readlines()[0].split('\n')[0])
    w = FeedWatcher(ssh_client, "/data/vulnerabilities", "/upload")
    w.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
