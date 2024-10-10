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
        if asn != 0:
            if cache.get("asn") is None:
                read_asn = MispReader(f"https://api.shadowserver.org/net/asn?query={asn}")
                asn_name = "EMPTY"
                api = read_asn.get_data_from_api()
                if api != "KO":
                    asn_json = json.loads(api)
                    asn_name = asn_json['asn_name']
                    cache.set("asn", asn_name)
                return asn_name
            else:
                return cache.get("asn")
        else:
            return "EMPTY"
    except json.JSONDecodeError as e:
        return f"Error decoding JSON: {e}"


def main():
    cache = SimpleCache()

    parser = argparse.ArgumentParser(description="A script that takes a vulnerability name as an argument.")
    parser.add_argument("-v", "--vul_name", type=str, required=True, help="The name of the vulnerability to process")

    args = parser.parse_args()
    db_session = DatabaseConnection().get_session()

    if "sinkhole" in args.vul_name:
        query = f"""SELECT JSON_EXTRACT(payload, "$.src_asn") AS ASN, JSON_EXTRACT(payload, "$.src_ip") AS IP, 
                    JSON_EXTRACT(payload, "$.src_city") AS CITY, JSON_EXTRACT(payload, "$.src_geo") AS GEO,
                    JSON_EXTRACT(payload, "$.src_region") AS REGION, JSON_EXTRACT(payload, "$.timestamp") AS TIMESTAMP,
                    JSON_EXTRACT(payload, "$.device_vendor") AS DEVICE_VENDOR, JSON_EXTRACT(payload, "$.device_type") AS DEVICE_TYPE, 
                    JSON_EXTRACT(payload, "$.device_model") AS DEVICE_MODEL, JSON_EXTRACT(payload, "$.infection") AS INFECTION 
                    FROM {args.vul_name} """
    elif "honeypot" in args.vul_name:
        query = f"""SELECT JSON_EXTRACT(payload, "$.src_ip") AS IP, JSON_EXTRACT(payload, "$.src_asn") AS ASN,
                    JSON_EXTRACT(payload, "$.src_geo") AS GEO, JSON_EXTRACT(payload, "$.src_region") AS REGION,
                    JSON_EXTRACT(payload, "$.src_city") AS CITY, JSON_EXTRACT(payload, "$.device_vendor") AS DEVICE_VENDOR,
                    JSON_EXTRACT(payload, "$.device_type") AS DEVICE_TYPE, JSON_EXTRACT(payload, "$.device_model") AS DEVICE_MODEL,
                    JSON_EXTRACT(payload, "$.protocol") AS PROTOCOL, JSON_EXTRACT(payload, "$.timestamp") AS TIMESTAMP,
                    JSON_EXTRACT(payload, "$.username") AS USERNAME, JSON_EXTRACT(payload, "$.password") AS PASSWORD,
                    JSON_EXTRACT(payload, "$.payload") AS PAYLOAD, JSON_EXTRACT(payload, "$.vulnerability_id") AS VULNERABILITY_ID,
                    JSON_EXTRACT(payload, "$.vulnerability_score") AS VULNERABILITY_SCORE, JSON_EXTRACT(payload, "$.vulnerability_severity") AS VULNERABILITY_SEVERITY,
                    JSON_EXTRACT(payload, "$.count") AS COUNT, JSON_EXTRACT(payload, "$.bytes") AS BYTES, JSON_EXTRACT(payload, "$.avg_pps") AS AVG_PPS,
                    JSON_EXTRACT(payload, "$.max_pps") AS MAX_PPS, JSON_EXTRACT(payload, "$.threat_tactic_id") AS THREAT_TACTIC_ID,
                    JSON_EXTRACT(payload, "$.threat_technique_id") AS THREAT_TECHNIQUE_ID, JSON_EXTRACT(payload, "$.target_vendor") AS TARGET_VENDOR,
                    JSON_EXTRACT(payload, "$.target_product") AS TARGET_PRODUCT, JSON_EXTRACT(payload, "$.target_class") AS TARGET_CLASS
                    FROM {args.vul_name} """
    else:
        query = f"""SELECT JSON_EXTRACT(payload, "$.asn") AS ASN, JSON_EXTRACT(payload, "$.ip") AS IP, 
                    JSON_EXTRACT(payload, "$.city") AS CITY, JSON_EXTRACT(payload, "$.geo") AS GEO,
                    JSON_EXTRACT(payload, "$.region") AS REGION, JSON_EXTRACT(payload, "$.timestamp") AS TIMESTAMP 
                    FROM {args.vul_name} """

    results = db_session.execute(text(query)).fetchall()
    if not results:
        print("No data found for the specified vulnerability.")
        return

    columns = results[0].keys()
    df = pd.DataFrame(results, columns=columns)

    df['ASN_NAME'] = df['ASN'].apply(lambda x: call_api(x, cache))
    df['vulnerability_name'] = args.vul_name
    cache.clear()
    json_list = []

    for index, row in df.iterrows():
        if "sinkhole" in args.vul_name:
            misp_ioc = ShadowVulnerabilities(
                uuid=uuid.uuid4().bytes,
                asn_name=row['ASN_NAME'],
                asn=row['ASN'],
                ip=row['IP'],
                timestamp=row['TIMESTAMP'],
                city=row.get('CITY', None),
                region=row.get('REGION', None),
                geo=row.get('GEO', None),
                device_vendor=row.get('DEVICE_VENDOR', None),
                device_type=row.get('DEVICE_TYPE', None),
                device_model=row.get('DEVICE_MODEL', None),
                infection=row.get('INFECTION', None),
                vulnerability_name=row['vulnerability_name']
            )
        elif "honeypot" in args.vul_name:
            misp_ioc = ShadowVulnerabilities(
                uuid=uuid.uuid4().bytes,
                asn_name=row['ASN_NAME'],
                asn=row['ASN'],
                ip=row['IP'],
                timestamp=row['TIMESTAMP'],
                city=row.get('CITY', None),
                region=row.get('REGION', None),
                geo=row.get('GEO', None),
                device_vendor=row.get('DEVICE_VENDOR', None),
                device_type=row.get('DEVICE_TYPE', None),
                device_model=row.get('DEVICE_MODEL', None),
                protocol=row.get('PROTOCOL', None),
                username=row.get('USERNAME', None),
                password=row.get('PASSWORD', None),
                payload=row.get('PAYLOAD', None),
                vulnerability_id=row.get('VULNERABILITY_ID', None),
                vulnerability_score=row.get('VULNERABILITY_SCORE', None),
                vulnerability_severity=row.get('VULNERABILITY_SEVERITY', None),
                count=row.get('COUNT', None),
                bytes=row.get('BYTES', None),
                avg_pps=row.get('AVG_PPS', None),
                max_pps=row.get('MAX_PPS', None),
                threat_tactic_id=row.get('THREAT_TACTIC_ID', None),
                threat_technique_id=row.get('THREAT_TECHNIQUE_ID', None),
                target_vendor=row.get('TARGET_VENDOR', None),
                target_product=row.get('TARGET_PRODUCT', None),
                target_class=row.get('TARGET_CLASS', None),
                vulnerability_name=row['vulnerability_name']
            )
        else:
            misp_ioc = ShadowVulnerabilities(
                uuid=uuid.uuid4().bytes,
                asn_name=row['ASN_NAME'],
                asn=row['ASN'],
                ip=row['IP'],
                timestamp=row['TIMESTAMP'],
                city=row.get('CITY', None),
                region=row.get('REGION', None),
                geo=row.get('GEO', None),
                vulnerability_name=row['vulnerability_name']
            )
        json_list.append(misp_ioc)

    QueryShadowServerFeeds().append_feeds(db_session, json_list)


if __name__ == '__main__':
    main()
