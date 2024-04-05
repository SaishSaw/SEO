# importing necessary libraries.
import os
import sys
import kaggle
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

#Downloading file from kaggle.
#Kaggle credentials

@dataclass
class DataIngestionConfig:
    """Creating data ingestion configuration"""
    train_path : str = os.path.join('artifacts',"train.csv")
    test_path : str = os.path.join('artifacts',"test.csv")
    data_path : str = os.path.join('artifacts',"data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method") 
        try:
            #os.environ['KAGGLE_CONFIG_DIR'] = r'D:\\SearchEngine\\.kaggle'
            
            download_dir = r'D:\SearchEngine\src\dataset'
            os.makedirs(download_dir,exist_ok=True)
            # Download the dataset
            api = kaggle.api.authenticate()
            #available_versions = api.dataset_list_versions(dataset_id="saishsawant/Google%20SERP(search%20engine%20result)%20")
            #latest_version = available_versions[0]['versionNumber']
            kaggle.api.dataset_download_files(dataset="polartech/google-serpsearch-engine-result-seo-search-data", path=download_dir, unzip=True)

            # List downloaded files
            for file in os.listdir(download_dir):
            #for filename in downloaded_files:
                df = pd.read_csv(os.path.join(download_dir,file))
                logging.info("Read the dataset as dataframe")

                os.makedirs(os.path.dirname(self.ingestion_config.train_path),exist_ok=True)

                df.to_csv(self.ingestion_config.data_path, index = False, header = True)
                logging.info('Train test split initiated')
                train_set,test_set = train_test_split(df, test_size=0.2, random_state=12)

                train_set.to_csv(self.ingestion_config.train_path, index = False, header = True)
                test_set.to_csv(self.ingestion_config.test_path, index = False, header = True)

                logging.info('Ingestion of the data is completed')

                return(self.ingestion_config.train_path,
                    self.ingestion_config.test_path) 
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == '__main__':
    obj = DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()

    #data_transformation = DataTransformation()
    #train_arr,test_arr,_ = data_transformation.initiate_data_transformation(train_data,test_data)

    #modeltrainer = ModelTrainer()
    #print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
        