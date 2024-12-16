from sqlalchemy import Column, TIMESTAMP, JSON, BigInteger, Integer, String, VARBINARY, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Classe abstraite
class ShadowServerFeeds(Base):
    __abstract__ = True
    uuid = Column(VARBINARY(16), primary_key=True)
    payload = Column(JSON)
    ts = Column(TIMESTAMP)

# Modèle MISP
class MispIOC(Base):
    __tablename__ = 'misp_iocs'

    uuid = Column(VARBINARY(16), primary_key=True)
    date = Column(String)
    info = Column(String)
    threat_level_id = Column(Integer)
    timestamp = Column(BigInteger)
    raw_data = Column(JSON)


class MispIOCORGA(Base):
    __tablename__ = 'misp_iocs_organisation_final'

    uuid = Column(VARBINARY(16), primary_key=True)
    orga_event = Column(String)
    ioc_type = Column(String)
    ioc_value = Column(String)
    timestamp = Column(BigInteger)
    category = Column(String)
    organisation = Column(String)


# Modèle ShadowVulnerabilities
from sqlalchemy import Column, String, BigInteger, Integer, Float, TIMESTAMP, VARBINARY

class ShadowVulnerabilities(Base):
    __tablename__ = 'shadow_vulnerabilities'

    uuid = Column(VARBINARY(16), primary_key=True)
    vulnerability_name = Column(String)
    asn_name = Column(String)
    asn = Column(BigInteger)
    ip = Column(String)
    timestamp = Column(TIMESTAMP)
    city = Column(String)
    region = Column(String)
    geo = Column(String)
    device_model = Column(String)
    device_type = Column(String)
    device_vendor = Column(String)
    infection = Column(String)
    query_type = Column(String)
    query = Column(String)
    family = Column(String)
    protocol = Column(String)
    username = Column(String)
    password = Column(String)
    payload = Column(String)
    vulnerability_id = Column(String)
    vulnerability_score = Column(Float)
    vulnerability_severity = Column(String)
    threat_tactic_id = Column(String)
    threat_technique_id = Column(String)
    target_vendor = Column(String)
    target_product = Column(String)
    target_class = Column(String)
    port = Column(Integer)
    tag = Column(String)
    curr_connections = Column(Integer)
    response_size = Column(Integer)
    ssl_version = Column(String)
    anonymous_access = Column(String)

    # Colonnes manquantes ajoutées
    src_hostname = Column(String)
    src_naics = Column(String)
    src_sector = Column(String)
    src_port = Column(Integer)
    dst_ip = Column(String)
    dst_port = Column(Integer)
    dst_asn = Column(BigInteger)
    dst_geo = Column(String)
    dst_region = Column(String)
    dst_city = Column(String)
    dst_hostname = Column(String)
    dst_naics = Column(String)
    dst_sector = Column(String)
    public_source = Column(String)
    service = Column(String)


# Modèles individuels
class Event4MicrosoftSinkhole(ShadowServerFeeds):
    __tablename__ = "event4_microsoft_sinkhole"

    def __repr__(self):
        return f'Event4MicrosoftSinkhole(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'

# Autres classes
class Blocklist(ShadowServerFeeds):
    __tablename__ = "blocklist"

    def __repr__(self):
        return f'Blocklist(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class CompromisedWebsite(ShadowServerFeeds):
    __tablename__ = "compromised_website"

    def __repr__(self):
        return f'CompromisedWebsite(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class DeviceId6(ShadowServerFeeds):
    __tablename__ = "device_id6"

    def __repr__(self):
        return f'DeviceId6(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4HoneypotBruteForce(ShadowServerFeeds):
    __tablename__ = "event4_honeypot_brute_force"

    def __repr__(self):
        return f'Event4HoneypotBruteForce(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4HoneypotDarknet(ShadowServerFeeds):
    __tablename__ = "event4_honeypot_darknet"

    def __repr__(self):
        return f'Event4HoneypotDarknet(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4HoneypotDdosAmp(ShadowServerFeeds):
    __tablename__ = "event4_honeypot_ddos_amp"

    def __repr__(self):
        return f'Event4HoneypotDdosAmp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4HoneypotHttpScan(ShadowServerFeeds):
    __tablename__ = "event4_honeypot_http_scan"

    def __repr__(self):
        return f'Event4HoneypotHttpScan(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4MicrosoftSinkholeHttp(ShadowServerFeeds):
    __tablename__ = "event4_microsoft_sinkhole_http"

    def __repr__(self):
        return f'Event4MicrosoftSinkholeHttp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4Sinkhole(ShadowServerFeeds):
    __tablename__ = "event4_sinkhole"

    def __repr__(self):
        return f'Event4Sinkhole(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4SinkholeDns(ShadowServerFeeds):
    __tablename__ = "event4_sinkhole_dns"

    def __repr__(self):
        return f'Event4SinkholeDns(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event6Sinkhole(ShadowServerFeeds):
    __tablename__ = "event6_sinkhole"

    def __repr__(self):
        return f'Event6Sinkhole(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Ftp(ShadowServerFeeds):
    __tablename__ = "scan6_ftp"

    def __repr__(self):
        return f'Scan6Ftp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Http(ShadowServerFeeds):
    __tablename__ = "scan6_http"

    def __repr__(self):
        return f'Scan6Http(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6HttpVulnerable(ShadowServerFeeds):
    __tablename__ = "scan6_http_vulnerable"

    def __repr__(self):
        return f'Scan6HttpVulnerable(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Ntp(ShadowServerFeeds):
    __tablename__ = "scan6_ntp"

    def __repr__(self):
        return f'Scan6Ntp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Ssh(ShadowServerFeeds):
    __tablename__ = "scan6_ssh"

    def __repr__(self):
        return f'Scan6Ssh(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanLdapTcp(ShadowServerFeeds):
    __tablename__ = "scan_ldap_tcp"

    def __repr__(self):
        return f'ScanLdapTcp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanLdapUdp(ShadowServerFeeds):
    __tablename__ = "scan_ldap_udp"

    def __repr__(self):
        return f'ScanLdapUdp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanNtp(ShadowServerFeeds):
    __tablename__ = "scan_ntp"

    def __repr__(self):
        return f'ScanNtp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanNtpmonitor(ShadowServerFeeds):
    __tablename__ = "scan_ntpmonitor"

    def __repr__(self):
        return f'ScanNtpmonitor(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanSmtpVulnerable(ShadowServerFeeds):
    __tablename__ = "scan_smtp_vulnerable"

    def __repr__(self):
        return f'ScanSmtpVulnerable(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanSnmp(ShadowServerFeeds):
    __tablename__ = "scan_snmp"

    def __repr__(self):
        return f'ScanSnmp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanSsdp(ShadowServerFeeds):
    __tablename__ = "scan_ssdp"

    def __repr__(self):
        return f'ScanSsdp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanSsh(ShadowServerFeeds):
    __tablename__ = "scan_ssh"

    def __repr__(self):
        return f'ScanSsh(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanTftp(ShadowServerFeeds):
    __tablename__ = "scan_tftp"

    def __repr__(self):
        return f'ScanTftp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'
