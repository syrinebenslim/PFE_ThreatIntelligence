import dataclasses
import json
import uuid

import pandas as pd
import requests

from watcher.schemas import MispIOC
from watcher.schemas.ingest_tidb import DatabaseConnection, QueryShadowServerFeeds


@dataclasses.dataclass
class MispReader:
    url: str

    def convert_json_to_single_line(self, json_str):
        try:
            # Charger le JSON en tant qu'objet Python
            data = json.loads(json_str)
            # Convertir l'objet Python en une seule ligne de JSON
            return data
        except json.JSONDecodeError as e:
            return f"Error decoding JSON: {e}"

    def write_misp_events(self):
        manifest_rows = self.read_manifest()
        if not manifest_rows:
            print("Manifest is empty or could not be read.")
            return None

        df = pd.json_normalize(manifest_rows, 'Tag',
                               ['uuid', 'info', 'date', 'analysis', 'threat_level_id', 'timestamp']).filter(
            ['uuid', 'info', 'date', 'analysis', 'threat_level_id', 'timestamp'])

        if df.empty:
            print("DataFrame is empty after normalization.")
            return None

        df['raw_data'] = df['uuid'].map(self.get_raw_data)
        df['raw_data'] = df['raw_data'].apply(self.convert_json_to_single_line)

        db_session = DatabaseConnection().get_session()
        json_list = []
        for index, row in df.iterrows():
            misp_ioc = MispIOC(
                uuid=uuid.uuid4().bytes,  # Assuming UUID is a string and needs encoding
                date=row['date'],
                info=row['info'],
                threat_level_id=int(row['threat_level_id']),
                timestamp=int(row['timestamp']),
                raw_data=row['raw_data']
            )
            json_list.append(misp_ioc)

        QueryShadowServerFeeds().append_feeds(db_session, json_list)

        return df  # Ensure the DataFrame is returned

    @staticmethod
    def clean_raw_data(as_in: str):
        output = as_in.replace("\n", "").replace('\\', '').strip()
        if output.startswith('"') and output.endswith('"'):
            output = output[1:-1]
        print(output)
        return output

    def read_manifest(self):
        response = self.get_data_from_api("/manifest.json")
        if response is None:
            return None

        try:
            data = json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

        rows = [{'uuid': key, **content} for key, content in data.items()]
        return rows

    def get_raw_data(self, uuid):
        return self.get_data_from_api("/" + uuid + ".json")

    def get_data_from_api(self, prefix=None):
        try:
            r = requests.get(self.url + prefix if prefix is not None else self.url, timeout=360)
            r.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
            return r.text
        except requests.RequestException as e:
            print(f"HTTP Request failed: {e}")
            return "KO"
