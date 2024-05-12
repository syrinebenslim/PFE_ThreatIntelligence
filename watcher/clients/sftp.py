import pandas as pd
import paramiko


class SFTPServerClient:

    def __init__(self, hostname, port, username, password):
        self.__hostName = hostname
        self.__port = port
        self.__userName = username
        self.__password = password
        self.__SSH_Client = paramiko.SSHClient()

    def connect(self):
        try:
            self.__SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__SSH_Client.connect(
                hostname=self.__hostName,
                port=self.__port,
                username=self.__userName,
                password=self.__password,
                look_for_keys=False
            )
        except Exception as excp:
            raise Exception(excp)
            return
        else:
            print(f"Connected to server {self.__hostName}:{self.__port} as  {self.__userName}.")

    def disconnect(self):
        self.__SSH_Client.close()
        print(f"{self.__userName} is disconnected to server  {self.__hostName}:{self.__port}")

    def read_csv_sftp(self, remoteFilePath, delimiter=","):
        sftp_client = self.__SSH_Client.open_sftp()
        remote_file = sftp_client.open(remoteFilePath)
        dataframe = pd.read_csv(filepath_or_buffer=remote_file, delimiter=delimiter)
        remote_file.close()
        sftp_client.close()
        return dataframe

    def getListofFiles(self, remoteFilePath):
        sftp_client = self.__SSH_Client.open_sftp()

        try:
            listdir = sftp_client.listdir(remoteFilePath)
            print(f"lists of files {listdir}")
            return listdir
        except IOError as e:
            print(f"Error while getting the list of files")

    def download_files(self, remote_filepath, local_filepath):
        print(f"downloading file {remote_filepath} to local {local_filepath}")

        sftp_client = self.__SSH_Client.open_sftp()
        try:
            sftp_client.get(remote_filepath, local_filepath)
        except FileNotFoundError as err:
            print(f"File: {remote_filepath} was not found on the server")
        sftp_client.close()

    def rename_files(self, remote_filepath, remote_filepath_dest):
        print(f"move file to remote {remote_filepath_dest}")

        sftp_client = self.__SSH_Client.open_sftp()
        try:
            sftp_client.rename(remote_filepath, remote_filepath_dest)
        except IOError as err:
            print(f"File: {remote_filepath} was not found on the server")
        sftp_client.close()

    def upload_files(self, remote_filepath, local_filepath):
        print(f"uploading file {local_filepath} to remote {remote_filepath}")

        sftp_client = self.__SSH_Client.open_sftp()
        try:
            sftp_client.put(local_filepath, remote_filepath)
        except IOError as err:
            print(f"File {local_filepath} was not found on the local system")
        sftp_client.close()

    def remove_files(self, remote_filepath):
        print(f"removing file from remote {remote_filepath}")

        sftp_client = self.__SSH_Client.open_sftp()
        try:
            sftp_client.remove(remote_filepath)
        except IOError as err:
            print(f"File {remote_filepath} was not removed")
        sftp_client.close()

    def execute_command(self, command):
        stdin, stdout, stderr = self.__SSH_Client.exec_command(command)
        print(stdout.readlines())
        print(stderr.readlines())

    def check_exist(self, remote_filepath):
        print(f"check exist file {remote_filepath}")

        sftp_client = self.__SSH_Client.open_sftp()
        try:
            sftp_client.stat(remote_filepath)
            print(f"File: {remote_filepath} exist ")
        except IOError as err:
            print(f"File: {remote_filepath} dosnt not exist ")
            return False
        return True
