>An Amazon Kinesis Data Stream is a real-time data streaming service designed for collecting, processing, and analyzing large streams of data records. It acts as a continuously flowing data pipe, allowing multiple applications to process the same data concurrently

>Properties:  Data can be ingested from multiple sources [website clickstreams, financial transactions, social media feeds, IoT device data, realtime dashboards]
              Data records are stored durably for 24 hours by default --upto 365 days helps in reprocessing
              Records are strictly ordered within each shard based on their arrival time.
              Producers send data to the stream (e.g., using Kinesis Producer Library (KPL), AWS SDKs, or agents).
              Consumers read and process data from the stream (e.g., using Kinesis Client Library (KCL), AWS Lambda, or Kinesis Data Analytics)

