> Efficient indexing is important foe both write and read speeds
> Create separate indices for separate use cases 
>Define mappinf where possible inclusing field types and analyzers. Aviod dynamic mapping where possible.
>Correct data types for efficient storage and querying. text for full text serach, keyword for exact matches.
>Index only necessary fileds needed for analyzing data and improve performance.
>Use _source to control what is stored. Specify the fields that need to be stored.
>Use BULK API for ingesting large volumes of data.
>Refresh interval low for real time and high for batch loads.
>Auto generated id's is a good option, elastic do not have to check again for duplicates.
>Shard size optimization, 10GB to 50GB optimal.