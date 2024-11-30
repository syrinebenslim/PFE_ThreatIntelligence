from sqlalchemy import Column, TIMESTAMP, JSON, BigInteger, Integer, String, VARBINARY,Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ShadowServerFeeds(Base):
    __abstract__ = True
    uuid = Column(VARBINARY(16), primary_key=True)
    payload = Column(JSON)
    ts = Column(TIMESTAMP)


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
    query= Column(String)
    family=Column(String)

    # Nouveaux champs ajoutés
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


class Event4MicrosoftSinkhole(ShadowServerFeeds):
    __tablename__ = "event4_microsoft_sinkhole"

    def __repr__(self):
        return f'Event4MicrosoftSinkhole(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Blocklist(ShadowServerFeeds):
    __tablename__ = "blocklist"

    def __repr__(self):
        return f'Blocklist(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class CompromisedAccount(ShadowServerFeeds):
    __tablename__ = "compromised_account"

    def __repr__(self):
        return f'CompromisedAccount(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class CompromisedWebsite(ShadowServerFeeds):
    __tablename__ = "compromised_website"

    def __repr__(self):
        return f'CompromisedWebsite(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class CompromisedWebsite6(ShadowServerFeeds):
    __tablename__ = "compromised_website6"

    def __repr__(self):
        return f'CompromisedWebsite6(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class DeviceId(ShadowServerFeeds):
    __tablename__ = "device_id"

    def __repr__(self):
        return f'DeviceId(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Device_Id6(ShadowServerFeeds):
    __tablename__ = "device_id6"

    def __repr__(self):
        return f'device_id6(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4DdosParticipant(ShadowServerFeeds):
    __tablename__ = "event4_ddos_participant"

    def __repr__(self):
        return f'Event4DdosParticipant(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4HoneypotDarknet(ShadowServerFeeds):
    __tablename__ = "event4_honeypot_darknet"

    def __repr__(self):
        return f'Event4HoneypotDarknet(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4HoneypotDdos(ShadowServerFeeds):
    __tablename__ = "event4_honeypot_ddos"

    def __repr__(self):
        return f'Event4HoneypotDdos(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4HoneypotDdosAmp(ShadowServerFeeds):
    __tablename__ = "event4_honeypot_ddos_amp"

    def __repr__(self):
        return f'Event4HoneypotDdosAmp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4HoneypotHttpScan(ShadowServerFeeds):
    __tablename__ = "event4_honeypot_http_scan"

    def __repr__(self):
        return f'Event4HoneypotHttpScan(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4HoneypotBruteForce(ShadowServerFeeds):
    __tablename__ = "event4_honeypot_brute_force"

    def __repr__(self):
        return f'Event4HoneypotBruteForce(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4HoneypotIcsScan(ShadowServerFeeds):
    __tablename__ = ".event4_honeypot_ics_scan "

    def __repr__(self):
        return f'Event4HoneypotIcsScan(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4HoneypotRdpScan(ShadowServerFeeds):
    __tablename__ = "event4_honeypot_rdp_scan"

    def __repr__(self):
        return f'Event4HoneypotRdpScan(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'

class Event4SinkholeDns(ShadowServerFeeds):
    __tablename__ = "event4_sinkhole_dns"

    def __repr__(self):
        return f'Event4SinkholeDns(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'
class Event4HoneypotSmbScan(ShadowServerFeeds):
    __tablename__ = "event4_honeypot_smb_scan"

    def __repr__(self):
        return f'Event4HoneypotSmbScan(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4IpSpoofer(ShadowServerFeeds):
    __tablename__ = "event4_ip_spoofer"

    def __repr__(self):
        return f'Event4IpSpoofer(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4MicrosoftSinkholeHttp(ShadowServerFeeds):
    __tablename__ = "event4_microsoft_sinkhole_http"

    def __repr__(self):
        return f'Event4MicrosoftSinkholeHttp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4Sinkhole(ShadowServerFeeds):
    __tablename__ = "event4_sinkhole"

    def __repr__(self):
        return f'Event4Sinkhole(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4SinkholeHttp(ShadowServerFeeds):
    __tablename__ = "event4_sinkhole_http"

    def __repr__(self):
        return f'Event4SinkholeHttp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4SinkholeHttpReferer(ShadowServerFeeds):
    __tablename__ = "event4_sinkhole_http_referer"

    def __repr__(self):
        return f'Event4SinkholeHttpReferer(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event6Sinkhole(ShadowServerFeeds):
    __tablename__ = "event6_sinkhole"

    def __repr__(self):
        return f'Event6Sinkhole(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event6SinkholeHttp(ShadowServerFeeds):
    __tablename__ = "event6_sinkhole_http"

    def __repr__(self):
        return f'Event6SinkholeHttp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event6SinkholeHttpReferer(ShadowServerFeeds):
    __tablename__ = "event6_sinkhole_http_referer"

    def __repr__(self):
        return f'Event6SinkholeHttpReferer(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class MalwareUrl(ShadowServerFeeds):
    __tablename__ = "malware_url"

    def __repr__(self):
        return f'MalwareUrl(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Population6Bgp(ShadowServerFeeds):
    __tablename__ = "population6_bgp"

    def __repr__(self):
        return f'Population6Bgp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Population6HttpProxy(ShadowServerFeeds):
    __tablename__ = "population6_http_proxy"

    def __repr__(self):
        return f'Population6HttpProxy(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Population6Msmq(ShadowServerFeeds):
    __tablename__ = "population6_msmq"

    def __repr__(self):
        return f'Population6Msmq(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class PopulationBgp(ShadowServerFeeds):
    __tablename__ = "population_bgp"

    def __repr__(self):
        return f'PopulationBgp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class PopulationHttpProxy(ShadowServerFeeds):
    __tablename__ = "population_http_proxy"

    def __repr__(self):
        return f'PopulationHttpProxy(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class PopulationMsmq(ShadowServerFeeds):
    __tablename__ = "population_msmq"

    def __repr__(self):
        return f'PopulationMsmq(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class SandboxConn(ShadowServerFeeds):
    __tablename__ = "sandbox_conn"

    def __repr__(self):
        return f'SandboxConn(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class SandboxUrl(ShadowServerFeeds):
    __tablename__ = "sandbox_url"

    def __repr__(self):
        return f'SandboxUrl(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Activemq(ShadowServerFeeds):
    __tablename__ = "scan6_activemq"

    def __repr__(self):
        return f'Scan6Activemq(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Bgp(ShadowServerFeeds):
    __tablename__ = "scan6_bgp"

    def __repr__(self):
        return f'Scan6Bgp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Cwmp(ShadowServerFeeds):
    __tablename__ = "scan6_cwmp"

    def __repr__(self):
        return f'Scan6Cwmp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Dns(ShadowServerFeeds):
    __tablename__ = "scan6_dns"

    def __repr__(self):
        return f'Scan6Dns(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Elasticsearch(ShadowServerFeeds):
    __tablename__ = "scan6_elasticsearch"

    def __repr__(self):
        return f'Scan6Elasticsearch(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Exchange(ShadowServerFeeds):
    __tablename__ = "scan6_exchange"

    def __repr__(self):
        return f'Scan6Exchange(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Ftp(ShadowServerFeeds):
    __tablename__ = "scan6_ftp"

    def __repr__(self):
        return f'Scan6Ftp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Http(ShadowServerFeeds):
    __tablename__ = "scan6_http"

    def __repr__(self):
        return f'Scan6Http(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6HttpProxy(ShadowServerFeeds):
    __tablename__ = "scan6_http_proxy"

    def __repr__(self):
        return f'Scan6HttpProxy(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6HttpVulnerable(ShadowServerFeeds):
    __tablename__ = "scan6_http_vulnerable"

    def __repr__(self):
        return f'Scan6HttpVulnerable(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Ipp(ShadowServerFeeds):
    __tablename__ = "scan6_ipp"

    def __repr__(self):
        return f'Scan6Ipp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Isakmp(ShadowServerFeeds):
    __tablename__ = "scan6_isakmp"

    def __repr__(self):
        return f'Scan6Isakmp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6LdapTcp(ShadowServerFeeds):
    __tablename__ = "scan6_ldap_tcp"

    def __repr__(self):
        return f'Scan6LdapTcp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Mqtt(ShadowServerFeeds):
    __tablename__ = "scan6_mqtt"

    def __repr__(self):
        return f'Scan6Mqtt(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6MqttAnon(ShadowServerFeeds):
    __tablename__ = "scan6_mqtt_anon"

    def __repr__(self):
        return f'Scan6MqttAnon(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Mysql(ShadowServerFeeds):
    __tablename__ = "scan6_mysql"

    def __repr__(self):
        return f'Scan6Mysql(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Ntp(ShadowServerFeeds):
    __tablename__ = "scan6_ntp"

    def __repr__(self):
        return f'Scan6Ntp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Ntpmonitor(ShadowServerFeeds):
    __tablename__ = "scan6_ntpmonitor"

    def __repr__(self):
        return f'Scan6Ntpmonitor(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Postgres(ShadowServerFeeds):
    __tablename__ = "scan6_postgres "

    def __repr__(self):
        return f'Scan6Postgres(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Rdp(ShadowServerFeeds):
    __tablename__ = "scan6_rdp"

    def __repr__(self):
        return f'Scan6Rdp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Slp(ShadowServerFeeds):
    __tablename__ = ".scan6_slp"

    def __repr__(self):
        return f'Scan6Slp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Smb(ShadowServerFeeds):
    __tablename__ = "scan6_smb"

    def __repr__(self):
        return f'Scan6Smb(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Smtp(ShadowServerFeeds):
    __tablename__ = "scan6_smtp"

    def __repr__(self):
        return f'Scan6Smtp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6SmtpVulnerable(ShadowServerFeeds):
    __tablename__ = "scan6_smtp_vulnerable"

    def __repr__(self):
        return f'Scan6SmtpVulnerable(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6snmp(ShadowServerFeeds):
    __tablename__ = "scan6_snmp"

    def __repr__(self):
        return f'Scan6snmp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Scan6Ssh(ShadowServerFeeds):
    __tablename__ = "scan6_ssh"

    def __repr__(self):
        return f'Scan6Ssh(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanLdapUdp(ShadowServerFeeds):
    __tablename__ = "scan_ldap_udp"

    def __repr__(self):
        return f'ScanLdapUdp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanLdapTcp(ShadowServerFeeds):
    __tablename__ = "scan_ldap_tcp"

    def __repr__(self):
        return f'ScanLdapTcp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanNtp(ShadowServerFeeds):
    __tablename__ = "scan_ntp"

    def __repr__(self):
        return f'ScanNtp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanNtpmonitor(ShadowServerFeeds):
    __tablename__ = "scan_ntpmonitor"

    def __repr__(self):
        return f'ScanNtpmonitor(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanTftp(ShadowServerFeeds):
    __tablename__ = "scan_tftp"

    def __repr__(self):
        return f'ScanTftp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanSslPoodle(ShadowServerFeeds):
    __tablename__ = "scan_ssl_poodle"

    def __repr__(self):
        return f'ScanSslPoodle(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanSsl(ShadowServerFeeds):
    __tablename__ = "scan_ssl"

    def __repr__(self):
        return f'ScanSsl(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanSsh(ShadowServerFeeds):
    __tablename__ = "scan_ssh"

    def __repr__(self):
        return f'ScanSsh(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanSsdp(ShadowServerFeeds):
    __tablename__ = "scan_ssdp"

    def __repr__(self):
        return f'ScanSsdp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanSnmp(ShadowServerFeeds):
    __tablename__ = "scan_snmp"

    def __repr__(self):
        return f'ScanSnmp(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanSmtpVulnerable(ShadowServerFeeds):
    __tablename__ = "scan_smtp_vulnerable"

    def __repr__(self):
        return f'ScanSmtpVulnerable(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class SpamUrl(ShadowServerFeeds):
    __tablename__ = "spam_url"

    def __repr__(self):
        return f'SpamUrl(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class ScanWsDiscovery(ShadowServerFeeds):
    __tablename__ = "scan_ws_discovery"

    def __repr__(self):
        return f'ScanWsDiscovery(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'


class Event4HoneypotDdosTarget(ShadowServerFeeds):
    __tablename__ = "event4_honeypot_ddos_target"

    def __repr__(self):
        return f'Event4HoneypotDdosTarget(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'