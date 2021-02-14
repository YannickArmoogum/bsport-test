import boto3

client = boto3.client('dynamodb',endpoint_url="http://host.docker.internal:8000/", region_name='us-west-1')
tableList = client.list_tables()
table_name = 'Appointments'

if table_name in tableList['TableNames']:
    pass


else:
    dynamodb = boto3.resource('dynamodb',endpoint_url="http://host.docker.internal:8000/", region_name='us-west-1')
    table = dynamodb.create_table(
        TableName=table_name,

        KeySchema = [
            {
                'AttributeName':'id',
                'KeyType':'HASH'
            },
            {
                'AttributeName':'user_FK',
                'KeyType':'N'
            }

        ],
        AttributeDefinitions=[
            {
                'AttributeName':'id',
                'AttributeType':'N'
            },
            {
                'AttributeName':'user_FK',
                'AttributeType':'N'
            }          
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits':10,
            'WriteCapacityUnits':10
        }

    )