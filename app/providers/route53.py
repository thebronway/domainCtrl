import boto3
import logging
from botocore.exceptions import ClientError, NoCredentialsError
from app.providers.base import BaseDNSProvider
from app.config import Config

logger = logging.getLogger(__name__)

class Route53Provider(BaseDNSProvider):
    def __init__(self):
        # We access os.environ directly or via Config helper
        # Logic moved from services.py
        access_key = Config().get_env_compat(['AWS_ACCESS_KEY_ID', 'USERNAME'])
        secret_key = Config().get_env_compat(['AWS_SECRET_ACCESS_KEY', 'PASSWORD'])

        if not access_key or not secret_key:
             raise Exception("Route53 requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")

        try:
            self.client = boto3.client(
                'route53',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key
            )
            self.client.list_hosted_zones(MaxItems='1') # Connectivity check
            logger.info("Route 53 provider initialized.")
        except Exception as e:
            raise Exception(f"Route53 Init Error: {e}")

    def _find_zone_id(self, domain):
        # ... (Same logic as before) ...
        try:
            paginator = self.client.get_paginator('list_hosted_zones')
            for page in paginator.paginate():
                for zone in page['HostedZones']:
                    if domain.endswith(zone['Name'][:-1]):
                        return zone['Id']
        except Exception as e:
            logger.error(f"R53 API Error: {e}")
        return None

    def get_record_ip(self, domain):
        # ... (Same logic, renamed from get_a_record_ip) ...
        zone_id = self._find_zone_id(domain)
        if not zone_id: return None
        try:
            response = self.client.list_resource_record_sets(
                HostedZoneId=zone_id, StartRecordName=domain, StartRecordType='A', MaxItems='1'
            )
            sets = response.get('ResourceRecordSets', [])
            if sets and sets[0]['Name'] == f"{domain}.":
                if 'ResourceRecords' in sets[0]: return sets[0]['ResourceRecords'][0]['Value']
                if 'AliasTarget' in sets[0]: return f"ALIAS: {sets[0]['AliasTarget']['DNSName']}"
            return None
        except ClientError as e:
            logger.error(f"Error getting record for {domain}: {e}")
            return None

    def update_record_ip(self, domain, new_ip):
        # ... (Same logic, renamed from update_a_record_ip) ...
        zone_id = self._find_zone_id(domain)
        if not zone_id: return False
        try:
            self.client.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={
                    'Comment': f'domainCtrl DDNS update',
                    'Changes': [{'Action': 'UPSERT', 'ResourceRecordSet': {
                        'Name': domain, 'Type': 'A', 'TTL': 300,
                        'ResourceRecords': [{'Value': new_ip}],
                    }}]
                }
            )
            return True
        except ClientError as e:
            logger.error(f"Error updating record for {domain}: {e}")
            return False

    def get_certbot_flags(self):
        # Route53 specific flags
        return "--dns-route53"