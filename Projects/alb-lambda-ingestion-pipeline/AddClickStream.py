import json, logging, uuid, os
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO").upper())

class AddPageEvent:
    def __init__(self, random_number):
        self.random_number = random_number
        logger.debug(f"{self.random_number}) - Initializing AddPageEvent class")

    async def AddPageEvent(self, random_number, requestdata, kinesis_client, stream_name):
        logger.debug(f"{self.random_number}- Inside AddPageEvent method")
        try:
            create_time= self._get_todays_date()
            uuid_string = str(uuid.uuid4())
            request_buffer = (json.dumps(requestdata) + "\n").encode('utf-8')

            kinesis_request = {
                "StreamName": stream_name,
                "Data" : request_buffer,
                "PartitionKey": uuid_string     
            }
            logger.debug(f"{self.random_number}- Kinesis Request : {kinesis_request}")

            reponse = await kinesis_client.put_record(**kinesis_request)
            logger.debug(f"{self.random_number}- Kinesis Response : {reponse}")
            return reponse
        except Exception as e:
            logger.error(f"{self.random_number}- Exception in AddPageEvent occured at {create_time}: {str(e)}")
            raise       
    def _get_todays_date(self):
        """ Returns today's date in YYYY-MM-DD format """
        today = datetime.now(timezone.utc)
        return today.strftime("%Y-%m-%d")               