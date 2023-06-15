import json
import os
import socket

import boto3
import dns.resolver
from nslookup import Nslookup

# Python DNS libraries
# socket
# + native simple lookup
# dnspython: https://pypi.org/project/dnspython/
# + advanced DNS toolkit
# - little documentation (examples: https://github.com/rthalley/dnspython/tree/master/examples)
# nslookup: https://pypi.org/project/nslookup/
# + high-level wrapper around dnspython

def handler(event, context):
    # Inspect LocalStack endpoint
    endpoint_url = f"http://{os.environ['LOCALSTACK_HOSTNAME']}:{os.environ['EDGE_PORT']}"
    aws_endpoint_url = os.environ['AWS_ENDPOINT_URL']
    # or LOCALSTACK_HOST in the future (not in the docs and env yet): https://github.com/localstack/localstack/pull/7893
    assert endpoint_url == aws_endpoint_url
    print(f"{endpoint_url=}")
    print('====================')

    # Inspect DNS resolver
    dns_resolver = dns.resolver.Resolver()
    print(f"dns_resolvers={dns_resolver.nameservers}")
    print('====================')

    # Test DNS resolution
    domains = [
        "localstack",
        "localhost.localstack.cloud",
        "lambda.us-east-1.amazonaws.com",
        "aws.amazon.com",
        "amazonaws.com",
        "s3.aws.amazon.com",
        "github.com",
        "invalid.com",
        "host.docker.internal",
    ]
    for domain in domains:
        try:
            ip = dns_lookup_nslookup(domain)
            print(f"{domain}=>{ip}")
        except Exception as e:
            print(f"{domain}=>None (error: {e})")
    print('====================')

    # Test transparent endpoint injection
    client = boto3.client('lambda')
    ls_client = boto3.client('lambda', endpoint_url=endpoint_url)
    account_settings = client.get_account_settings()
    print(account_settings)
    print('====================')

    return {
        "statusCode": 200,
        "body": json.dumps({
            "endpoint_url": endpoint_url,
        }),
    }

def dns_lookup_native(domain):
    return socket.gethostbyname(domain)

def dns_lookup_nslookup(domain):
    dns_query = Nslookup()
    ips_record = dns_query.dns_lookup(domain)
    return ips_record.answer
