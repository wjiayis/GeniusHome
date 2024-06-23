import boto3
from common.util import handle_boto_exceptions

dynamodb_client = boto3.client("dynamodb")

@handle_boto_exceptions
def get_item(TableName, Key):
    body = dynamodb_client.get_item(TableName=TableName, Key=Key)
    return body, 200, "Successful dynamodb:GetItem!"

@handle_boto_exceptions
def put_item(TableName, Item):
    dynamodb_client.put_item(TableName=TableName, Item=Item)
    return None, 200, "Successful dynamodb:PutItem!"

@handle_boto_exceptions
def delete_item(TableName, Key):
    dynamodb_client.delete_item(TableName=TableName, Key=Key)
    return None, 200, "Successful dynamodb:DeleteItem!"

@handle_boto_exceptions
def scan(TableName):
    response = dynamodb_client.scan(TableName=TableName)
    body = [d["chat_id"]["S"] for d in response["Items"]]
    return body, 200, "Successful dynamodb:Scan!"