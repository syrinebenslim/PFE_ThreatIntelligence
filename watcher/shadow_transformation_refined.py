import json
import uuid

import pandas as pd
from sqlalchemy import text

from watcher.callerapi.misp.reader import MispReader
from watcher.config.cache import SimpleCache
from watcher.schemas import ShadowVulnerabilities
from watcher.schemas.ingest_tidb import DatabaseConnection, QueryShadowServerFeeds


class ShadowTransformationRefined:
    def __init__(self, vul_types: str):
        self.vul_types = vul_types

    def call_api(self, asn, cache):
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

    def refine(self):
        cache = SimpleCache()

        vul_type_array = self.vul_types.strip().split(",")
        db_session = DatabaseConnection().get_session()

        for vul_name in vul_type_array:
            if "sinkhole" in vul_name:
                query = f"""SELECT JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_asn")) AS ASN, JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_ip")) AS IP, 
                            JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_city")) AS CITY, JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_geo")) AS GEO,
                            JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_region")) AS REGION, STR_TO_DATE(JSON_UNQUOTE(JSON_EXTRACT(payload, "$.timestamp")), '%Y-%m-%d %H:%i:%s') AS TIMESTAMP,
                            JSON_EXTRACT(payload, "$.device_vendor") AS DEVICE_VENDOR, JSON_EXTRACT(payload, "$.device_type") AS DEVICE_TYPE, 
                            JSON_EXTRACT(payload, "$.device_model") AS DEVICE_MODEL, JSON_EXTRACT(payload, "$.query_type") AS QUERY_TYPE, JSON_EXTRACT(payload, "$.query") AS QUERY,JSON_UNQUOTE(JSON_EXTRACT(payload, "$.infection")) AS INFECTION,JSON_UNQUOTE(JSON_EXTRACT(payload, "$.family")) AS FAMILY 
                            FROM {vul_name} """
            elif "honeypot" in vul_name:
                query = f"""SELECT JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_ip")) AS IP, JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_asn")) AS ASN,
                            JSON_UNQUOTE(JSON_EXTRACT(payload, "$.src_geo")) AS GEO, JSON_EXTRACT(payload, "$.src_region") AS REGION,
                            JSON_EXTRACT(payload, "$.src_city") AS CITY, JSON_EXTRACT(payload, "$.device_vendor") AS DEVICE_VENDOR,
                            JSON_EXTRACT(payload, "$.device_type") AS DEVICE_TYPE, JSON_EXTRACT(payload, "$.device_model") AS DEVICE_MODEL,
                            JSON_EXTRACT(payload, "$.protocol") AS PROTOCOL, STR_TO_DATE(JSON_UNQUOTE(JSON_EXTRACT(payload, "$.timestamp")), '%Y-%m-%d %H:%i:%s') AS TIMESTAMP,
                            JSON_EXTRACT(payload, "$.username") AS USERNAME, JSON_EXTRACT(payload, "$.password") AS PASSWORD,
                            JSON_EXTRACT(payload, "$.payload") AS PAYLOAD, JSON_EXTRACT(payload, "$.vulnerability_id") AS VULNERABILITY_ID,
                            JSON_EXTRACT(payload, "$.vulnerability_score") AS VULNERABILITY_SCORE, JSON_EXTRACT(payload, "$.vulnerability_severity") AS VULNERABILITY_SEVERITY,
                            
                             JSON_EXTRACT(payload, "$.threat_tactic_id") AS THREAT_TACTIC_ID,
                            JSON_EXTRACT(payload, "$.threat_technique_id") AS THREAT_TECHNIQUE_ID, JSON_EXTRACT(payload, "$.target_vendor") AS TARGET_VENDOR,
                            JSON_EXTRACT(payload, "$.target_product") AS TARGET_PRODUCT, JSON_EXTRACT(payload, "$.target_class") AS TARGET_CLASS
                            FROM {vul_name} """
            else:
                query = f"""SELECT JSON_UNQUOTE(JSON_EXTRACT(payload, "$.asn")) AS ASN, JSON_UNQUOTE(JSON_EXTRACT(payload, "$.ip")) AS IP, 
                            JSON_UNQUOTE(JSON_EXTRACT(payload, "$.city")) AS CITY, JSON_EXTRACT(payload, "$.geo") AS GEO,
                            JSON_EXTRACT(payload, "$.region") AS REGION, STR_TO_DATE(JSON_UNQUOTE(JSON_EXTRACT(payload, "$.timestamp")), '%Y-%m-%d %H:%i:%s') AS TIMESTAMP 
                            FROM {vul_name} """

            results = db_session.execute(text(query)).fetchall()
            if not results:
                print("No data found for the specified vulnerability.")
                return

            columns = results[0].keys()
            df = pd.DataFrame(results, columns=columns)

            df['ASN_NAME'] = df['ASN'].apply(lambda x: self.call_api(x, cache))
            df['vulnerability_name'] = vul_name

            json_list = []

            for index, row in df.iterrows():
                if "sinkhole" in vul_name:
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
                        vulnerability_name=row['vulnerability_name']
                    )
                elif "honeypot" in vul_name:
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
                        family=row.get('FAMILY', None),
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
        cache.clear()
