import boto3
import json
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = "Resumes"

# Custom serializer for DynamoDB Decimals
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  # Debugging

    table = dynamodb.Table(TABLE_NAME)

    # Check if user provided an applicant_id
    if "queryStringParameters" in event and event["queryStringParameters"]:
        applicant_id = event["queryStringParameters"].get("applicant_id")

        if not applicant_id:
            return {"statusCode": 400, "body": json.dumps("Missing applicant_id")}

        response = table.get_item(Key={"ApplicantID": applicant_id})

        if "Item" not in response:
            return {"statusCode": 404, "body": json.dumps("Resume not found")}

        return {"statusCode": 200, "body": json.dumps(response["Item"], default=decimal_default)}

    # If no applicant_id, return all resumes
    response = table.scan()
    return {
        "statusCode": 200,
        "body": json.dumps(response['Items'], default=decimal_default)
    }
