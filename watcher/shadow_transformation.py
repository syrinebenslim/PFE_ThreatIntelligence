import argparse
import json
import uuid

import pandas as pd
from sqlalchemy import text

from watcher.callerapi.misp.reader import MispReader
from watcher.config.cache import SimpleCache
from watcher.schemas import ShadowVulnerabilities
from watcher.schemas.ingest_tidb import DatabaseConnection, QueryShadowServerFeeds


def call_api(asn, cache):
    try:
        # Charger le JSON en tant qu'objet Python
        if asn != 0:
            if cache.get("asn") is None:
                read_asn = MispReader(f"https://api.shadowserver.org/net/asn?query={asn}")
                asn_name = "EMPTY"
                api = read_asn.get_data_from_api()
                if api != "KO":
                    asn_json = json.loads(api)
                    asn_name = asn_json['asn_name']
                    cache.set("asn", asn_name)
                # Convertir l'objet Python en une seule ligne de JSON
                return asn_name
            else:
                return cache.get("asn")

        else:
            return "EMPTY"
    except json.JSONDecodeError as e:
        return f"Error decoding JSON: {e}"


def main():
    # Use a breakpoint in the code line below to debug your script.
    cache = SimpleCache()

    parser = argparse.ArgumentParser(description="A script that takes a vulnerability name as an argument.")
    parser.add_argument("-v", "--vul_name", type=str, required=True, help="The name of the vulnerability to process")

    args = parser.parse_args()
    db_session = DatabaseConnection().get_session()
    if "sinkhole" in args.vul_name:
        query = f"""SELECT  JSON_EXTRACT(payload, "$.src_asn") AS ASN , JSON_EXTRACT(payload, "$.src_ip") AS IP , JSON_EXTRACT(payload, "$.src_city") AS CITY,JSON_EXTRACT(payload, "$.src_geo") AS GEO,JSON_EXTRACT(payload, "$.src_region") AS REGION, JSON_EXTRACT(payload, "$.timestamp") AS TIMESTAMP,
        JSON_EXTRACT(payload, "$.device_vendor") AS DEVICE_VENDOR, JSON_EXTRACT(payload, "$.device_type") AS DEVICE_TYPE,JSON_EXTRACT(payload, "$.device_model") AS DEVICE_MODEL,JSON_EXTRACT(payload, "$.infection") AS INFECTION FROM {args.vul_name} """

    else:
        query = f"""SELECT  JSON_EXTRACT(payload, "$.asn") AS ASN , JSON_EXTRACT(payload, "$.ip") AS IP , JSON_EXTRACT(payload, "$.city") AS CITY,JSON_EXTRACT(payload, "$.geo") AS GEO,JSON_EXTRACT(payload, "$.region") AS REGION, JSON_EXTRACT(payload, "$.timestamp") AS TIMESTAMP FROM {args.vul_name} """

    results = db_session.execute(text(query)).fetchall()
    columns = results[0].keys()
    print(columns)
    # Convert to DataFrame
    df = pd.DataFrame(results, columns=columns)

    df['ASN_NAME'] = df['ASN'].apply(lambda x: call_api(x, cache))
    df['vulnerability_name'] = args.vul_name
    cache.clear()
    json_list = []

    for index, row in df.iterrows():
        misp_ioc = ShadowVulnerabilities(
            uuid=uuid.uuid4().bytes,
            asn_name=row['ASN_NAME'],
            asn=row['ASN'],
            ip=row['IP'],
            timestamp=row['TIMESTAMP'],
            city=row['CITY'],
            region=row['REGION'],
            geo=row['GEO'],
            device_vendor=row['DEVICE_VENDOR'],
            device_type=row['DEVICE_TYPE'],
            device_model=row['DEVICE_MODEL'],
            infection=row['INFECTION'],
            vulnerability_name=row['vulnerability_name']
        )
        json_list.append(misp_ioc)

    QueryShadowServerFeeds().append_feeds(db_session, json_list)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
