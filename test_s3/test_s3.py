import boto3
import os
import pytest
import random
import string

import warnings

warnings.filterwarnings("ignore")


@pytest.fixture
def s3client():
    client = boto3.client(
        "s3",
        endpoint_url=f"https://{os.environ['MINIO_DOMAIN']}",
        verify=False,
    )

    return client


@pytest.fixture
def randomstring():
    return "".join(random.choice(string.ascii_lowercase) for i in range(10))


def test_list_buckets(s3client):
    res = s3client.list_buckets()
    assert "ResponseMetadata" in res
    assert res["ResponseMetadata"]["HTTPStatusCode"] == 200


def test_bucket_ops(s3client, randomstring):
    bucketname = f"testbucket-{randomstring}"

    res = s3client.list_buckets()
    assert "ResponseMetadata" in res
    assert res["ResponseMetadata"]["HTTPStatusCode"] == 200
    assert not any(bucket["Name"] == bucketname for bucket in res["Buckets"])

    res = s3client.create_bucket(Bucket=bucketname)
    assert "ResponseMetadata" in res
    assert res["ResponseMetadata"]["HTTPStatusCode"] == 200

    res = s3client.list_buckets()
    assert "ResponseMetadata" in res
    assert res["ResponseMetadata"]["HTTPStatusCode"] == 200
    assert len(res["Buckets"]) > 0
    assert any(bucket["Name"] == bucketname for bucket in res["Buckets"])

    res = s3client.delete_bucket(Bucket=bucketname)
    assert "ResponseMetadata" in res
    assert res["ResponseMetadata"]["HTTPStatusCode"] == 204
