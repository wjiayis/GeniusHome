from common.util import handle_boto_exceptions

@handle_boto_exceptions
def get_item(dynamodb_client, TableName, Key):
    body = dynamodb_client.get_item(TableName=TableName, Key=Key)
    return body, 200, "Successful dynamodb:GetItem!"

@handle_boto_exceptions
def put_item(dynamodb_client, TableName, Item):
    dynamodb_client.put_item(TableName=TableName, Item=Item)
    return None, 200, "Successful dynamodb:PutItem!"

@handle_boto_exceptions
def delete_item(dynamodb_client, TableName, Key):
    dynamodb_client.delete_item(TableName=TableName, Key=Key)
    return None, 200, "Successful dynamodb:DeleteItem!"