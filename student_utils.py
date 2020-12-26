import pandas as pd
import numpy as np
import os
import tensorflow as tf
import functools
from sklearn.model_selection import train_test_split

####### STUDENTS FILL THIS OUT ######
#Question 3
def reduce_dimension_ndc(df, ndc_df):
    '''
    df: pandas dataframe, input dataset
    ndc_df: pandas dataframe, drug code dataset used for mapping in generic names
    return:
        df: pandas dataframe, output dataframe with joined generic drug name
    '''
    dfc = ndc_df[["NDC_Code","Non-proprietary Name"]].set_index('NDC_Code')
    labels = []
    for code in df.ndc_code.values:
        if isinstance(code,float):
            labels.append("")
        else:
            val = dfc["Non-proprietary Name"].get(code,"")
            if not isinstance(val,str):
#                 print(val)
                val = val.iloc[0]
            labels.append(val)
    df["generic_drug_name"] = labels   
    return df

#Question 4
def select_first_encounter(df):
    '''
    df: pandas dataframe, dataframe with all encounters
    return:
        - first_encounter_df: pandas dataframe, dataframe with only the first encounter for a given patient
    '''
    reduce_dim_df = df.sort_values("encounter_id")
    first_encounter_values = reduce_dim_df.groupby("patient_nbr")["encounter_id"].head(1)
    first_encounter_df = reduce_dim_df[reduce_dim_df["encounter_id"].isin(first_encounter_values)]
    return first_encounter_df


#Question 6
def patient_dataset_splitter(df, patient_key='patient_nbr'):
    '''
    df: pandas dataframe, input dataset that will be split
    patient_key: string, column that is the patient id

    return:
     - train: pandas dataframe,
     - validation: pandas dataframe,
     - test: pandas dataframe,
    '''
    patient_nbrs = df[patient_key].unique()
    np.random.shuffle(patient_nbrs)
    split = [.6,.2,.2]
    stop1 = round(len(patient_nbrs)*(split[0]))
    stop2 = round(len(patient_nbrs)*(split[0]+split[1]))
    ids_train = patient_nbrs[:stop1]
    ids_validation = patient_nbrs[stop1:stop2]
    ids_test = patient_nbrs[stop2:]
    assert(len(patient_nbrs)==len(ids_train)+len(ids_validation)+len(ids_test))
    train = df[df[patient_key].isin(ids_train)].reset_index(drop=True)
    validation = df[df[patient_key].isin(ids_validation)].reset_index(drop=True)
    test = df[df[patient_key].isin(ids_test)].reset_index(drop=True)    
    return train, validation, test

#Question 7

def create_tf_categorical_feature_cols(categorical_col_list,
                              vocab_dir='./diabetes_vocab/'):
    '''
    categorical_col_list: list, categorical field list that will be transformed with TF feature column
    vocab_dir: string, the path where the vocabulary text files are located
    return:
        output_tf_list: list of TF feature columns
    '''
    output_tf_list = []
    for c in categorical_col_list:
        if len(c):
            vocab_file_path = os.path.join(vocab_dir,  c + "_vocab.txt")
            '''
            Which TF function allows you to read from a text file and create a categorical feature
            You can use a pattern like this below...
            tf_categorical_feature_column = tf.feature_column.......

            '''
            tf_categorical_feature_column = tf.feature_column.categorical_column_with_vocabulary_file(c, vocab_file_path,num_oov_buckets=1)
            tf_indicator_column = tf.feature_column.indicator_column(tf_categorical_feature_column)
            output_tf_list.append(tf_indicator_column)
    return output_tf_list

#Question 8
def normalize_numeric_with_zscore(col, mean, std):
    '''
    This function can be used in conjunction with the tf feature column for normalization
    '''
    return (col - mean)/std



def create_tf_numeric_feature(col, MEAN, STD, default_value=0):
    '''
    col: string, input numerical column name
    MEAN: the mean for the column in the training data
    STD: the standard deviation for the column in the training data
    default_value: the value that will be used for imputing the field

    return:
        tf_numeric_feature: tf feature column representation of the input field
    '''
    normalizer = functools.partial(normalize_numeric_with_zscore, mean=MEAN, std=STD)
    return tf.feature_column.numeric_column(
        key=col, default_value = default_value, normalizer_fn=normalizer, dtype=tf.float64)
    return tf_numeric_feature

#Question 9
def get_mean_std_from_preds(diabetes_yhat):
    '''
    diabetes_yhat: TF Probability prediction object
    '''
    m = '?'
    s = '?'
    return m, s

# Question 10
def get_student_binary_prediction(df, col):
    '''
    df: pandas dataframe prediction output dataframe
    col: str,  probability mean prediction field
    return:
        student_binary_prediction: pandas dataframe converting input to flattened numpy array and binary labels
    '''
    return student_binary_prediction
