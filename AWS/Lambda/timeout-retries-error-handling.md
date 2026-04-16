>ALB Target Group Timeout: By default, it's 60 seconds, but for Lambda targets, the health check timeout is 30 seconds by default, and can be configured up to 120 seconds

>Lambda Function Timeout: Each Lambda function has a configurable timeout, ranging from 1 second to 15 minutes (900 seconds)

>Ensure the ALB's idle timeout is greater than or equal to the Lambda function's timeout to allow the Lambda to complete its execution or explicitly time out.

>Monitor CloudWatch logs for Task timed out messages to identify functions that are frequently hitting their timeout limits

>Timeout: The context helps in returning remaining can be used to handle timeout errors gracefully
>def lambda_handler(event, context):
     lambda_remaining_time_seconds = context.get_remaining_time_in_millis() / 1000

>Retry: Can implement a retry logic to run the function with n retry's. An example below
def exponential_backoff_retry(max_attempts=3, initial_delay=1, backoff_factor=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_attempts - 1:
                        wait_time = initial_delay * (backoff_factor ** attempt) + random.uniform(0, 0.5) # Adding jitter
                        print(f"Retrying in {wait_time:.2f} seconds...")
                        time.sleep(wait_time)
                    else:
                        raise # Re-raise the last exception if all attempts fail
        return wrapper
    return decorator


>Error Handling: Use try-except blocks to catch specific types of errors (json.JSONDecodeError, ValueError) and returns appropriate HTTP status codes (400 for client errors) and informative messages

Good Practice:
>Asynchronous Invocation using SQS DLQ with Maximum Age of Event and retrt attempts: If a request is tried twice with in the time of Maximum age evnt and still fails to process during aysynchrnous execution or throttle it will be sent to SQS DLQ.

