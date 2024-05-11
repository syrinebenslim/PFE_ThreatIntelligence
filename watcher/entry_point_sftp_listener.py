# This is a sample Python script.
import io
import os
import uuid

from watcher.clients.sftp import SFTPServerClient
# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from watcher.feed_parsers_shadow import FeedParser
from watcher.parser.data_parser import Csv2Json
from watcher.schemas.ingest_tidb import QueryShadowServerFeeds, DatabaseConnection

BUFSIZE = 8 * 1024


def fetch_file_as_bytesIO(sftp, path):
    """
    Using the sftp client it retrieves the file on the given path by using pre fetching.
    :param sftp: the sftp client
    :param path: path of the file to retrieve
    :return: bytesIO with the file content
    """
    with sftp.file(path, mode='rb') as file:
        file_size = file.stat().st_size
        file.prefetch(file_size)
        file.set_pipelined()
        return io.BytesIO(file.read(file_size))


def to_camel_case(self, test_str):
    # printing original string
    print("The original string is : " + str(test_str))

    # split underscore using split
    temp = test_str.split('_')

    # joining result
    res = temp[0] + ''.join(ele.title() for ele in temp[1:])

    # printing result
    print("The camel case string is : " + str(res))
    text = str(res)
    return text[0].upper() + text[1:]


def main():
    # Use a breakpoint in the code line below to debug your script.

    client_sftp = SFTPServerClient(hostname="192.168.1.140", port=22, username="sftpuser", password="syrinebs")
    db_session = DatabaseConnection().get_session()
    client_sftp.connect()

    data_vulnerabilities_ = "/sftpuser/data-vulnerabilities/"
    remote_files = client_sftp.getListofFiles(data_vulnerabilities_)
    if remote_files is not None:
        for remote_file in remote_files:
            try:

                remote_server_path = f"{data_vulnerabilities_}{remote_file}"
                local_file_path = f"/data/vulnerabilities/{remote_file}"
                file_byte = fetch_file_as_bytesIO(client_sftp, remote_server_path)
                basename = os.path.basename(remote_server_path)
                data, name = FeedParser(basename).parse_feed_name()
                print(name)
                jsons_data = Csv2Json(input_file_csv=file_byte) \
                    .make_json()
                print(jsons_data)
                json_list = []
                case_class = to_camel_case(name)
                print(f"CLASS  <{case_class}>")
                for data in jsons_data:
                    json_list.append(
                        globals()[case_class](uuid=uuid.uuid4().bytes, payload=data))

                QueryShadowServerFeeds().append_feeds(db_session, json_list)

                remote_archive_file_path = f"/sftpuser/vulnerabilities_archive/{remote_file}"
                print(f"data copied to local {local_file_path}")
                client_sftp.rename_files(remote_server_path, remote_archive_file_path)
                print(f"data moved  to remote {remote_archive_file_path}")






            except IOError as e:
                print("error during uploading files")
                remote_errors_file_path = f"/sftpuser/vulnerabilities_errors/{remote_file}"
                client_sftp.rename_files(remote_server_path, remote_errors_file_path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
