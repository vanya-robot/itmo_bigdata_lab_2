import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from configparser import ConfigParser

class DataProcessor:
    def __init__(self, config_path):
        config = ConfigParser()
        config.read(config_path)
        self.test_size = float(config['DATA']['test_size'])
        self.random_state = int(config['DATA']['random_state'])
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), ['culmen_length_mm', 'culmen_depth_mm', 
                 'flipper_length_mm', 'body_mass_g']),
                ('cat', OneHotEncoder(), ['island', 'sex'])
            ])

    def process(self, data_path):
        df = pd.read_csv(data_path)
        df = df.dropna()
        
        X = df.drop('species', axis=1)
        y = df['species']
        
        X_processed = self.preprocessor.fit_transform(X)
        return train_test_split(X_processed, y, 
                              test_size=self.test_size,
                              random_state=self.random_state)