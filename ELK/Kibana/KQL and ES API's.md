Add a document:
PUT /<index>/_doc/<id>
{
    "title" : "My first blog",
    "content" : "This is a content of my first blog"
    "tags" : ["blog", "first"]
    "timestamp" : "2025-11-18T21:00:00"

}


PUT /<index>/_doc/     # uses auto id
{
    "title" : "My first blog",
    "content" : "This is a content of my first blog"
    "tags" : ["blog", "first"]
    "timestamp" : "2025-11-18T21:00:00"

}


GET /my_index/_doc/1
POST /my_index/_update/1
{
    <data>
}

Retrieve all documents:

GET my_index/_search
{
    "query" : {
        "match_all" : {}
    }
}



GET /_cluster/health
GET /_cluster/stats
