import os
import logging
import json
import asyncio
import uuid
from datetime import datetime, timedelta, timezone
import aiobotocore.seesion as aiosession
from botocore.exceptions import ClientError

from AddClickStream import AddPageEvent

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO").upper())
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

logger.info('##loading AWS Module outside handler started##')
session = aiosession.get_session()
kinesis_client = None
stream_name = os.environ.get("STREAM_NAME")
dbsa_key = os.environ.get('DBSAKEY')
dbsa_secret = os.environ.get('DBSASECRET')
dbsa_input_validation = os.environ.get('DBSA_INPUT_VALIDATION')
dbsa_auth_verification = os.environ.get('DBSA_AUTH_VERIFICATION')
logger.info('##loading AWS Module outside handler completed##')


async def index_handler(event, context):
    global kinesis_client
    if kinesis_client is None:
        kinesis_client = await session.create_client('kinesis',region_name=os.environ.get('AWS_REGION'))
    request_id = f"{context.aws_request_id} {context.log_stream_name}"
    trace_id = event.get('headers',{}).get('x-amz-trace-ifid')

    response_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET", 
        "Access-Control-Allow-Headers": "Content-Type,Authorization"
    }
    response ={
        "statusCode": 200,
        "headers": response_headers,
        "body": json.dumps({
            "message": "Index handler executed successfully",
            "request_id": request_id,
            "trace_id": trace_id
        })
    }
    failure_reponse_headers =response_headers.copy()
    failure_reponse= {
        "statusCode": 500,
        "headers": failure_reponse_headers,
        "body": json.dumps({
            "message": "Index handler execution failed",
            "request_id": request_id,
            "trace_id": trace_id
        })
    }   

    allowed_origins = ["hhtps://uat-axe-digital-analytics.xxx.com"]
    origin = event.get('headers', {}).get('origin')
    if origin in allowed_origins:
        response['headers']["Access-Control-Allow-Origin"] = origin
        failure_reponse['headers']["Access-Control-Allow-Origin"] = origin
        response['headers']['Access-Control-Allow-Credentials'] = 'true'
        failure_reponse['headers']['Access-Control-Allow-Credentials'] = 'true'

        if event.get('httpMethod') == 'OPTIONS':
            response['statusCode'] = 204
            failure_reponse['statusCode'] = 204
            return response

    logger.info(f"Index handler started for request_id: {request_id}, trace_id: {trace_id}")
    logger.info (f"Event received: {json.dumps(event)}")
    request_body = event.get('body', '{}')
    logger.info(f"Request body: {request_body}")
    request_data = {}
    if request_body:
        try:
            request_data =json.loads(request_body)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return failure_reponse  
    else:
        response['body'] = json.dumps({"message": "No body in request"})
        return response 
    
    headers = event.get('headers', {})
    auth_passed = False
    if dbsa_auth_verification and dbsa_auth_verification.lower() == 'true': 
        auth_passed = True

    if not auth_passed:
        logger.warning(f"Authentication failed for request_id: {request_id}")
        failure_reponse['statusCode'] = 401
        failure_reponse['body'] = json.dumps({"message": "Authentication failed"})
        return failure_reponse

    try:
        random_number = context.aws_request_id.split('-')[0]
        event_object = AddPageEvent(random_number)
        event_status ="Event logged failed"

        try :
            add_event_log_object = await event_object.AddPageEvent(random_number, request_data, kinesis_client, stream_name)
            if add_event_log_object and "ShardId" in add_event_log_object:
                event_status ="Event logged successfully"
            else:
                logger.error(f"Failed to log event to Kinesis for request_id: {request_id}")    
    
        except ClientError as e:
            logger.error(f"ClientError while logging event to Kinesis for request_id: {request_id}, error: {e}")        
            event_status ="Event logged Failed"

        except Exception as e:    
            logger.error(f"Exception while logging event to Kinesis for request_id: {request_id}, error: {e}")  
            event_status ="Event logged Failed"

        if event_status == "Event logged Failed":
            body_content = {"message": "Failed to log event", "request_id": request_id, "trace_id": trace_id}
            failure_reponse['body'] = json.dumps(body_content)
            return failure_reponse              
        else:
            body_content = {"message": "Event logged successfully", "request_id": request_id, "trace_id": trace_id}
            response['body'] = json.dumps(body_content)             
            return response        
    except Exception as e:
        logger.error(f"Exception in index_handler for request_id: {request_id}, error: {e}")
        return failure_reponse  
    
asyncio.run(index_handler())    