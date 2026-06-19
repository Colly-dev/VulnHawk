
import boto3
from botocore.exceptions import ClientError
from typing import List, Dict, Any

class S3Checker:
    """
    Audits AWS S3 buckets for misconfigurations (Read-Only).
    """

    def __init__(self, session=None):
        self.s3 = (session or boto3.Session()).client('s3')

    def analyze(self) -> List[Dict[str, Any]]:
        findings = []
        try:
            buckets = self.s3.list_buckets().get('Buckets', [])
            for bucket in buckets:
                name = bucket['Name']
                
                # Check Public Access Block
                try:
                    pab = self.s3.get_public_access_block(Bucket=name)
                    config = pab.get('PublicAccessBlockConfiguration', {})
                    if not all(config.values()):
                        findings.append({
                            "id": "AWS_S3_PUBLIC_ACCESS_BLOCK_DISABLED",
                            "title": f"S3 Public Access Block not fully enabled: {name}",
                            "description": f"The bucket {name} does not have all 'Block Public Access' settings enabled.",
                            "severity": "HIGH",
                            "type": "S3_PUBLIC_ACCESS",
                            "category": "Cloud Security"
                        })
                except ClientError as e:
                    if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
                        findings.append({
                            "id": "AWS_S3_NO_PUBLIC_ACCESS_BLOCK",
                            "title": f"S3 Public Access Block missing: {name}",
                            "description": f"The bucket {name} has no Public Access Block configuration.",
                            "severity": "CRITICAL",
                            "type": "S3_PUBLIC_ACCESS",
                            "category": "Cloud Security"
                        })

                # Check Encryption
                try:
                    self.s3.get_bucket_encryption(Bucket=name)
                except ClientError as e:
                    if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                        findings.append({
                            "id": "AWS_S3_ENCRYPTION_DISABLED",
                            "title": f"S3 Default Encryption Disabled: {name}",
                            "description": f"The bucket {name} does not have default server-side encryption enabled.",
                            "severity": "MEDIUM",
                            "type": "S3_ENCRYPTION_MISSING",
                            "category": "Cloud Security"
                        })

        except Exception as e:
            # Handle permission errors or other issues
            pass
            
        return findings

    def generate_demo_findings(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "AWS_S3_PUBLIC_ACCESS_DEMO",
                "title": "S3 Bucket Publicly Accessible (Demo)",
                "description": "The bucket 'prod-backups-internal' is publicly accessible via ACL.",
                "severity": "CRITICAL",
                "type": "S3_PUBLIC_ACCESS",
                "category": "Cloud Security"
            }
        ]
