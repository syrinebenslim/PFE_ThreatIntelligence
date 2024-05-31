import dataclasses
import json
import sys

import pandas as pd
import requests

from watcher.schemas import MispIOC
from watcher.schemas.ingest_tidb import DatabaseConnection, QueryShadowServerFeeds


@dataclasses.dataclass
class MispReader:
    url: str

    def write_misp_events(self):
        manifest_rows = self.read_manifest()
        df = pd.json_normalize(manifest_rows, 'Tag',
                               ['uuid', 'info', 'date', 'analysis', 'threat_level_id', 'timestamp']).filter(
            ['uuid', 'info', 'date', 'analysis', 'threat_level_id', 'timestamp'])

        df['raw_data'] = df['uuid'].map(self.get_raw_data)
        db_session = DatabaseConnection().get_session()
        json_list = []
        for index, row in df.iterrows():
            misp_ioc = MispIOC(
                uuid=row['uuid'],  # Assuming UUID is a string and needs encoding
                date=row['date'],
                info=row['info'],
                threat_level_id=int(row['threat_level_id']),
                timestamp=int(row['timestamp']),
                raw_data=row['raw_data']
            )
            json_list.append(misp_ioc)

        QueryShadowServerFeeds().append_feeds(db_session, json_list)



    def read_manifest(self):
        response = self.get_data_from_api("/manifest.json")
        data = json.loads(response)
        rows = []
        for key, content in data.items():
            rows.append({'uuid': key, **content})

        return rows

    def get_raw_data(self, uuid):
        return self.get_data_from_api("/" + uuid + ".json")

    def get_data_from_api(self, prefix=None):
        try:
            r = requests.get(self.url + prefix if prefix is not None else self.url, timeout=360)  #
            r.raise_for_status()
        except requests.exceptions.ConnectionError as errc:
            print("\r\nError Connecting:", errc)
            sys.exit()
        except requests.exceptions.HTTPError as errh:
            print("\r\nHttp Error:", errh)
            sys.exit()
        except requests.exceptions.Timeout as errt:
            print("\r\nTimeout Error:", errt)
            sys.exit()
        except requests.exceptions.RequestException as err:
            print("\r\nOOps: Something Else", err)
            sys.exit()

        if r.status_code == requests.codes.ok:
            return r.text
        else:
            print("Error occurred when listing API content")
            sys.exit()
