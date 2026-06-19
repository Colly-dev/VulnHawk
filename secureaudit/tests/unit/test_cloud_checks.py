
import unittest
from unittest.mock import MagicMock, patch
from src.modules.cloud.aws.s3_checker import S3Checker

class TestS3Checker(unittest.TestCase):
    @patch("boto3.client")
    def test_s3_public_access_block_disabled(self, mock_boto_client):
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3

        # Simulate a bucket with no public access block
        mock_s3.list_buckets.return_value = {
            "Buckets": [{
                "Name": "test-bucket-public",
                "CreationDate": "2023-01-01T00:00:00Z"
            }]
        }
        mock_s3.get_public_access_block.side_effect = [
            {
                "PublicAccessBlockConfiguration": {
                    "BlockPublicAcls": False,
                    "IgnorePublicAcls": True,
                    "BlockPublicPolicy": True,
                    "RestrictPublicBuckets": True
                }
            }
        ]
        mock_s3.get_bucket_encryption.side_effect = Exception # Simulate no encryption

        checker = S3Checker()
        findings = checker.analyze()

        self.assertTrue(any(f["type"] == "S3_PUBLIC_ACCESS" for f in findings))
        self.assertTrue(any(f["id"] == "AWS_S3_PUBLIC_ACCESS_BLOCK_DISABLED" for f in findings))

    @patch("boto3.client")
    def test_s3_encryption_disabled(self, mock_boto_client):
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3

        # Simulate a bucket with encryption disabled
        mock_s3.list_buckets.return_value = {
            "Buckets": [{
                "Name": "test-bucket-unencrypted",
                "CreationDate": "2023-01-01T00:00:00Z"
            }]
        }
        mock_s3.get_public_access_block.return_value = {
            "PublicAccessBlockConfiguration": {
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True
            }
        }
        mock_s3.get_bucket_encryption.side_effect = ClientError({
            "Error": {"Code": "ServerSideEncryptionConfigurationNotFoundError"}
        }, "GetBucketEncryption")

        checker = S3Checker()
        findings = checker.analyze()

        self.assertTrue(any(f["type"] == "S3_ENCRYPTION_MISSING" for f in findings))

    def test_s3_demo_findings(self):
        checker = S3Checker()
        findings = checker.generate_demo_findings()
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["type"], "S3_PUBLIC_ACCESS")
