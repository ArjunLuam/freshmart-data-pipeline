import boto3
import pandas as pd
from datetime import datetime
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
        

def validator(df,expected_columns):
    validation_list = []
    for i in expected_columns:
        if i not in df.columns.to_list():
            validation_list.append('Fail')
    
    if df.shape[0] == 0:
        validation_list.append('Fail')

    return validation_list


def lambda_handler(event,context):

    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        client = boto3.client('s3')                          
        response = client.get_object(Bucket=bucket, Key=key)

        df = pd.read_csv(response['Body'])
        expected_columns = ['invoice_id', 'branch', 'city', 'product_line', 
                        'unit_price', 'quantity', 'date', 'payment', 'rating']
        
        
        
        if len(validator(df,expected_columns))==0:
            logger.info(f"File processed: {key}, Rows: {df.shape[0]}")
            print((f"File processed: {key}, Rows: {df.shape[0]}"))
            return{
                'status' : 'SUCCESS',
                'filename' : key,
                'row_count' : df.shape[0],
                'col_count' : len(expected_columns),
                'time_stamp': datetime.now().timestamp()
            }
        logger.info(f"File processed: {key}, Rows: {df.shape[0]},status : failed")    

        return{
                'status' : 'FAILURE',
                'filename' : key,
                'row_count' : df.shape[0],
                'col_count' : df.columns.to_list(),
                'time_stamp': datetime.now().timestamp()
            }
    except Exception as e:

        print(f"An exception occurred:{e}")
        logger.info(f"An exception occurred:{e}")


    