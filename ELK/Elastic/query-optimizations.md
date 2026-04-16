> filters for exact matches and range , makes faster queries and cacheable a they do not calculate relevant scores.
> Avoid wildcards
> only query and retrive the required fileds helps reduce data transfer and processing overhead.
> prefer sorting at index level rather at query time. limit the fileds in the _source to only whats necessary
> use profile api to understand how queries are executed and identify performance bottle necks.
> combine range queries and avoid costly operations.(over nested aggregations)
