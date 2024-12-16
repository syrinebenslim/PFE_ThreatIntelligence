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

    parser = argparse.ArgumentParser(description="A script that processes Shadowserver reports.")
    parser.add_argument("-v", "--vul_name", type=str, required=True, help="The name of the vulnerability to process")

    args = parser.parse_args()
    db_session = DatabaseConnection().get_session()

    if "sinkhole" in args.vul_name:
        query = f"""SELECT JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_asn")) AS ASN, 
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_ip")) AS IP, 
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_city")) AS CITY, 
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_geo")) AS GEO,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_region")) AS REGION, 
                           STR_TO_DATE(JSON_UNQUOTE(JSON_EXTRACT(payload, "$.timestamp")), '%Y-%m-%d %H:%i:%s') AS TIMESTAMP,
                           JSON_EXTRACT(payload, "$.device_vendor") AS DEVICE_VENDOR, 
                           JSON_EXTRACT(payload, "$.device_type") AS DEVICE_TYPE, 
                           JSON_EXTRACT(payload, "$.device_model") AS DEVICE_MODEL, 
                           JSON_EXTRACT(payload, "$.query_type") AS QUERY_TYPE, 
                           JSON_EXTRACT(payload, "$.family") AS Family, 
                           JSON_EXTRACT(payload, "$.infection") AS INFECTION,
                           JSON_EXTRACT(payload, "$.tag") AS TAG,
                           JSON_EXTRACT(payload, "$.event_id") AS EVENT_ID,
                           JSON_EXTRACT(payload, "$.query") AS QUERY
                         
                    FROM {args.vul_name} """
    elif "honeypot" in args.vul_name:
        query = f"""SELECT JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_ip")) AS IP, 
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_asn")) AS ASN,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_geo")) AS GEO, 
                           JSON_EXTRACT(payload, "$.src_region") AS REGION,
                           JSON_EXTRACT(payload, "$.src_city") AS CITY, 
                           JSON_EXTRACT(payload, "$.device_vendor") AS DEVICE_VENDOR,
                           JSON_EXTRACT(payload, "$.device_type") AS DEVICE_TYPE, 
                           JSON_EXTRACT(payload, "$.device_model") AS DEVICE_MODEL,
                           JSON_EXTRACT(payload, "$.protocol") AS PROTOCOL, 
                           STR_TO_DATE(JSON_UNQUOTE(JSON_EXTRACT(payload, "$.timestamp")), '%Y-%m-%d %H:%i:%s') AS TIMESTAMP,
                           JSON_EXTRACT(payload, "$.username") AS USERNAME,
                           JSON_EXTRACT(payload, "$.password") AS PASSWORD,
                           JSON_EXTRACT(payload, "$.payload") AS PAYLOAD,
                           JSON_EXTRACT(payload, "$.vulnerability_id") AS VULNERABILITY_ID,
                           JSON_EXTRACT(payload, "$.vulnerability_score") AS VULNERABILITY_SCORE,
                           JSON_EXTRACT(payload, "$.vulnerability_severity") AS VULNERABILITY_SEVERITY,
                           JSON_EXTRACT(payload, "$.threat_tactic_id") AS THREAT_TACTIC_ID,
                           JSON_EXTRACT(payload, "$.threat_technique_id") AS THREAT_TECHNIQUE_ID,
                           JSON_EXTRACT(payload, "$.target_vendor") AS TARGET_VENDOR,
                           JSON_EXTRACT(payload, "$.target_product") AS TARGET_PRODUCT,
                           JSON_EXTRACT(payload, "$.target_class") AS TARGET_CLASS,
                           JSON_EXTRACT(payload, "$.src_hostname") AS SRC_HOSTNAME,
       JSON_EXTRACT(payload, "$.src_naics") AS SRC_NAICS,
       JSON_EXTRACT(payload, "$.src_sector") AS SRC_SECTOR,
       JSON_EXTRACT(payload, "$.src_port") AS SRC_PORT,
       JSON_EXTRACT(payload, "$.dst_ip") AS DST_IP,
       JSON_EXTRACT(payload, "$.dst_port") AS DST_PORT,
       JSON_EXTRACT(payload, "$.dst_asn") AS DST_ASN,
       JSON_EXTRACT(payload, "$.dst_geo") AS DST_GEO,
       JSON_EXTRACT(payload, "$.dst_region") AS DST_REGION,
       JSON_EXTRACT(payload, "$.dst_city") AS DST_CITY,
       JSON_EXTRACT(payload, "$.dst_hostname") AS DST_HOSTNAME,
       JSON_EXTRACT(payload, "$.dst_naics") AS DST_NAICS,
       JSON_EXTRACT(payload, "$.dst_sector") AS DST_SECTOR,
       JSON_EXTRACT(payload, "$.public_source") AS PUBLIC_SOURCE,
       JSON_EXTRACT(payload, "$.infection") AS INFECTION,
       JSON_EXTRACT(payload, "$.family") AS FAMILY,
       JSON_EXTRACT(payload, "$.tag") AS TAG,
       JSON_EXTRACT(payload, "$.event_id") AS EVENT_ID,
       JSON_EXTRACT(payload, "$.service") AS SERVICE
                    FROM {args.vul_name} """
    elif "scan" in args.vul_name:
        query = f"""SELECT JSON_UNQUOTE(JSON_EXTRACT(payload, "$.timestamp")) AS TIMESTAMP,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.ip")) AS IP,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.port")) AS PORT,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.asn")) AS ASN,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.geo")) AS GEO,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.region")) AS REGION,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.city")) AS CITY,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.protocol")) AS PROTOCOL,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.tag")) AS TAG,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.curr_connections")) AS CURR_CONNECTIONS,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.response_size")) AS RESPONSE_SIZE,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.ssl_version")) AS SSL_VERSION,
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.anonymous_access")) AS ANONYMOUS_ACCESS
                    FROM {args.vul_name} """
    else:
        query = f"""SELECT JSON_UNQUOTE(JSON_EXTRACT(payload, "$.asn")) AS ASN, 
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.ip")) AS IP, 
                           JSON_UNQUOTE(JSON_EXTRACT(payload, "$.city")) AS CITY, 
                           JSON_EXTRACT(payload, "$.geo") AS GEO,
                           JSON_EXTRACT(payload, "$.region") AS REGION, 
                           STR_TO_DATE(JSON_UNQUOTE(JSON_EXTRACT(payload, "$.timestamp")), '%Y-%m-%d %H:%i:%s') AS TIMESTAMP 
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
                query_type=row.get('QUERY_TYPE', None),
                query=row.get('QUERY', None),
                infection=row.get('INFECTION', None),
                family=row.get('FAMILY', None),
                tag=row.get('TAG', None),
                event_id=row.get('EVENT_ID', None),
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
                threat_tactic_id=row.get('THREAT_TACTIC_ID', None),
                threat_technique_id=row.get('THREAT_TECHNIQUE_ID', None),
                target_vendor=row.get('TARGET_VENDOR', None),
                target_product=row.get('TARGET_PRODUCT', None),
                target_class=row.get('TARGET_CLASS', None),
                src_hostname=row.get('SRC_HOSTNAME', None),
                src_naics=row.get('SRC_NAICS', None),
                src_sector=row.get('SRC_SECTOR', None),
                dst_ip=row.get('DST_IP', None),
                dst_port=row.get('DST_PORT', None),
                dst_asn=row.get('DST_ASN', None),
                dst_geo=row.get('DST_GEO', None),
                dst_region=row.get('DST_REGION', None),
                dst_city=row.get('DST_CITY', None),
                dst_hostname=row.get('DST_HOSTNAME', None),
                dst_naics=row.get('DST_NAICS', None),
                dst_sector=row.get('DST_SECTOR', None),
                public_source=row.get('PUBLIC_SOURCE', None),
                infection=row.get('INFECTION', None),
                family=row.get('FAMILY', None),
                tag=row.get('TAG', None),
                event_id=row.get('EVENT_ID', None),
                service=row.get('SERVICE', None),
                src_port=row.get('SRC_PORT', None),
                vulnerability_name=row['vulnerability_name']

            )

        elif "scan" in args.vul_name:
            misp_ioc = ShadowVulnerabilities(
                uuid=uuid.uuid4().bytes,
                asn_name=row['ASN_NAME'],
                asn=row['ASN'],
                ip=row['IP'],
                timestamp=row['TIMESTAMP'],
                city=row.get('CITY', None),
                region=row.get('REGION', None),
                geo=row.get('GEO', None),
                port=row.get('PORT', None),
                protocol=row.get('PROTOCOL', None),
                tag=row.get('TAG', None),
                curr_connections=row.get('CURR_CONNECTIONS', None),
                response_size=row.get('RESPONSE_SIZE', None),
                ssl_version=row.get('SSL_VERSION', None),
                anonymous_access=row.get('ANONYMOUS_ACCESS', None),
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
