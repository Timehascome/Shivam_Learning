import sys, logging, os, time
import pandas as pd
import queries as mn
import traceback

#Logging
logger = logging.getLogger("e2e_performance")
logger.setLevel(logging.INFO)
handler = logging.FileHandler('e2e_performance_main.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s- %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def performance_query(channel, appId):
    if channel == "sgmb":
        base_query = {"timeout":"300s",
                      "query":{
                          "bool" : {
                              "filter" : [
                                  {
                                      "match_all" :{}
                                  },
                                  {
                                      "match_phrase":{"appId":appId}
                                  }
                              ]
                          }
                                              
                      }}
        return base_query
    
def aggregate_buckets(channel, base_query, _index):
    if channel == "sgmb":
        base_query.update(mn.min_fields_query)    
        #print(base_query)  #updated base query
    #js = es.search(index =_index, body = base_query)  #es is the connection to elastic search
    js = {
         "aggregations":{
             "service" : {
                 "buckets": [
                     {
                         "1":{
                             "value": 0.09399
                         },
                         "4":{
                             "value": 0.44
                         },
                         "7":{
                             "value": 0.38987
                         },
                     
                        "key" : "Splash",
                        "doc_count" : 645 }]
             }
         }

    }

    l_dict = []
    for d_service in js['aggregations']['service']['buckets']:
        print(f"printing data fromm output json {d_service}")
        eventType = d_service['key']
        _count = d_service['doc_count']
        _min = round(d_service['1']['value'],2)
        _max = round(d_service['4']['value'],2)
        _mean = round(d_service['7']['value'],2)
        l_dict.append({'evenType':eventType, 'Min':_min, 'Max':_max, 'Mean':_mean, 'Total_count':_count})
    min_fields_df = pd.DataFrame.from_dict(l_dict)
    return min_fields_df

def main():
    channel = str(sys.argv[1])
    try:
        if channel == "sgmb":
            _index = 'e2e_performance_log*' #reading all daily indexes
            #print(_index)
        else:
            logger.info("Channel does not exist")

        if channel == "sgmb":
            appId = "SG_MB"
        base_query = performance_query(channel, appId)
        #print(base_query)   # fetch the base query
        logger.info("Started running aggregation with for service" + time.asctime(time.localtime(time.time())))
        elastic_df = pd.DataFrame()

        min_fields_df  = aggregate_buckets(channel, base_query,_index)
        print(min_fields_df.head())
        elastic_df = min_fields_df
        elastic_df.drop_duplicates(inplace=True)
        #b = helpers.bulk(es, elastic_df.to_dict(orient='record'), index=f'e2e_performance_aggs_{channel}')
        logger.info("completed aggregation for service at" + time.asctime(time.localtime(time.time())))
    except:
        logger.error(str(traceback.format_exc()))
if __name__ == "__main__":
    main()    
        
