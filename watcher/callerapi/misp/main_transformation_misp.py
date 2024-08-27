import uuid

import pandas as pd
from sqlalchemy import text

from watcher.schemas import MispIOCORGA
from watcher.schemas.ingest_tidb import DatabaseConnection, QueryShadowServerFeeds


def main():
    # Use a breakpoint in the code line below to debug your script.
    db_session = DatabaseConnection().get_session()
    query = """SELECT  JSON_EXTRACT(raw_data, "$.Event.Orgc.name") AS organisation , JSON_EXTRACT(raw_data, "$.Event.Attribute") AS Attributes FROM misp_iocs"""
    results = db_session.execute(text(query)).fetchall()
    json_list = []
    for result in results:
        print("#################")
        print(result)
        # data = json.loads(result['Attributes'])
        # df = pd.DataFrame(data)

        if result['Attributes'] is not None:
            df = pd.read_json(result['Attributes'])
            df["organisation"] = result['organisation']

            # Filtrer le DataFrame selon les colonnes désirées
            if 'to_ids' in df.columns:
                filtered_df = df[df['to_ids']].copy()
            else:
                print("Colonne 'to_ids' absente dans le DataFrame")

            # Ajouter la colonne 'orga_event'
            filtered_df.loc[:, 'orga_event'] = filtered_df['organisation'] + '_' + filtered_df['uuid']

            # Sélection des colonnes projetées
            projected_df = filtered_df[['organisation', 'type', 'value', 'orga_event', 'timestamp', 'category']]

            for index, row in projected_df.iterrows():
                misp_ioc = MispIOCORGA(
                    uuid=uuid.uuid4().bytes,
                    orga_event=row['orga_event'],  # Assuming UUID is a string and needs encoding
                    ioc_type=row['type'],
                    ioc_value=row['value'],
                    organisation=row['organisation'],
                    category=row['category'],
                    timestamp=int(row['timestamp'].timestamp())

                )
                json_list.append(misp_ioc)

    QueryShadowServerFeeds().append_feeds(db_session, json_list)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
