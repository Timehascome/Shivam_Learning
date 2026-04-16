>>Why do you get 502 response ?

>The ALB expects response in a particular format as below any deviation an result in 502 reponse OR reponse boby greater than 1 MB:
     let response = {
        "traceId":traceId,
        "requestId":requestId,
        "isBase64Encoded": false,
        "statusCode": 200,
        "statusDescription": "200 OK",
        "headers": {
        "Content-Type": "application/json",
        "X-Frame-Options": "SAMEORIGIN",
        "Strict-Transport-Security": "max-age=31536000; includeSubdomains; preload",
        "Content-Security-Policy": "default-src 'self'; script-src: https://*-digital.com",
        "X-Content-Type-Options": "nosniff",
        "X-Permitted-Cross-Domain-Policies": "none",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "content-type,key,secret,inputvalidation,authverification"
        "body" : {}
        } }


>> What to do when you get high target response time ?
   > Check the Lambda process (here) or the target process metrics such as invocations , throttling, concurrency quota 
   > Identify the bottle necks in the whole pipeline to catch the latency points.
