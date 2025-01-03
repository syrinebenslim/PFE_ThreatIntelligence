# This is a sample Python script.
import json
import uuid

from watcher.clients.sftp import SFTPServerClient
# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from watcher.feed_parsers_shadow import FeedParser
from watcher.schemas.ingest_tidb import DatabaseConnection, QueryShadowServerFeeds

BUFSIZE = 8 * 1024


def to_camel_case(test_str):
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
                remote_archive_file_path = f"/sftpuser/vulnerabilities_archive/{remote_file}"
                remote_errors_file_path = f"/sftpuser/vulnerabilities_errors/{remote_file}"
                remote_server_path = f"{data_vulnerabilities_}{remote_file}"
                if client_sftp.check_exist(remote_archive_file_path):
                    client_sftp.remove_files(remote_server_path)
                    continue
                if client_sftp.check_exist(remote_errors_file_path):
                    client_sftp.remove_files(remote_server_path)
                    continue
                local_file_path = f"/data/vulnerabilities/{remote_file}"
                date, name = FeedParser(remote_file).parse_feed_name()
                print(name)
                if name == "FILE_IGNORE":
                    raise IOError("Unsupported File")

                df = client_sftp.read_csv_sftp(remote_server_path)
                jsons_data = df.to_json(orient='records', lines=True).splitlines()
                json_list = []
                case_class = to_camel_case(name)
                print(f"using CLASS  <{case_class}>")
                for data in jsons_data:
                    class_ = get_model_db_name(case_class)
                    instance = class_(uuid=uuid.uuid4().bytes, payload=json.loads(data))
                    json_list.append(instance)

                QueryShadowServerFeeds().append_feeds(db_session, json_list)

                print(f"data copied to local {local_file_path}")
                client_sftp.rename_files(remote_server_path, remote_archive_file_path)
                print(f"data moved  to remote {remote_archive_file_path}")

            except IOError as e:
                print("error during uploading files")

                client_sftp.rename_files(remote_server_path, remote_errors_file_path)


def get_model_db_name(case_class):
    try:
        import_module = "watcher.schemas"
        modules = import_module.split(".")
        module = __import__(modules[0])
        for mod in modules[1:]:
            module = getattr(module, mod)
        class_ = getattr(module, case_class)
    except Exception as exp:
        print("model not found , please verify list of models ")
        raise IOError
    return class_


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
