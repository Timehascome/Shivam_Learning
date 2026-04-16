min_fields_query = {
    "aggs" : {
        "service" :{
            "terms" : {
                "field" : "eventType.keyword",
                "order" : {
                    "_count": "desc"
                },
                "size" : 2147483647
            },
            "aggs": {
                "1" : {
                    "min" : {
                        "field" : "elapsedTime"
                    }
                },
                "4" : {
                    "max" : {
                        "field" : "elapsedTime"
                    }
                },
                "7" : {
                    "avg" : {
                        "field" : "elapsedTime"
                    }
                }
            }
        }
    }
}