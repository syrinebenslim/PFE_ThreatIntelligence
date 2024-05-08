# This is a sample Python script.
import os

from watcher.clients.sftp import SFTPServerClient


# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():
    # Use a breakpoint in the code line below to debug your script.

    client_sftp = SFTPServerClient(hostname="192.168.1.114", port=22, username="sftpuser", password="changeit")

    client_sftp.connect()

    remote_files = client_sftp.getListofFiles("/data/vulnerabilities")

    for remote_file in remote_files:
        base_name = os.path.basename(remote_file)
        try:

            local_file_path = f"/data/vulnerabilities/{base_name}"
            remote_archive_file_path = f"/data/vulnerabilities_archive/{base_name}"
            client_sftp.download_files(remote_file, local_file_path)
            print(f"data copied to local {local_file_path}")
            client_sftp.rename_files(remote_file, remote_archive_file_path)
            print(f"data moved  to remote {remote_archive_file_path}")
        except IOError as e:
            print("error during uploading files")
            remote_errors_file_path = f"/data/vulnerabilities_errors/{base_name}"
            client_sftp.rename_files(remote_file, remote_errors_file_path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
