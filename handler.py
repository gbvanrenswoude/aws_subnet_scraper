import json
import boto3

def lambda_handler(event, context):
    region = context.invoked_function_arn.split(":")[3]
    if region == None:
        region="eu-central-1"
    print("Region set to: " + region)
    client = boto3.client('ec2', region_name=region)

    subnet_list = []
    response = client.describe_subnets(
    )
    subnet_list += response['Subnets']
    while "nextToken" in response:
        response = client.describe_subnets(
            nextToken=response['nextToken']
        )
        subnet_list += response['Subnets']
    print("Got the following list of dics: " + str(subnet_list))
    
    subnet_ids = []
    subnet_ids += [subnet['SubnetId'] for subnet in subnet_list]
    
    print("Found the following subnets: " + str(subnet_ids))
    
    return {
        'statusCode': 200,
        'body': json.dumps("Done scraping subnets, found " + str(subnet_ids))
    }
