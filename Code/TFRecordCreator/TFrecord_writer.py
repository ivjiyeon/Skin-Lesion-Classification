
# coding: utf-8

# In[22]:


import csv
import shutil
import numpy as np
from random import shuffle
import glob
import tensorflow as tf
import sys
import cv2

# In[23]:


def list_label(path_CSV, file_CSV, path_trainingSet):
    csv_file = path_CSV + file_CSV
    melanoma_image_name_dataset=[]
    non_cancer_image_name_dataset = []
    
    shuffle_data= True
    train_data_path = path_trainingSet
    
    addrs = sorted(glob.glob(train_data_path))
    
    try:
        with open(csv_file, "rt") as f:
            reader = csv.DictReader(f)
            labels = [1 if float(row['melanoma'])==1.0 else 0 for row in reader]
                      
    except Exception as e:
            print("Unable to read CSV file")
    
    if shuffle_data:
        c = list(zip(addrs,labels))
        shuffle(c)
        addrs,labels = zip(*c) 
        
    
    return addrs, labels
                    


# In[24]:


def load_image(addr):
    img = cv2.imread(addr)
    img = cv2.resize(img, (224, 224), interpolation = cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.uint8)
    
    return img


# In[25]:


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
    return tf.train.Feature(bytes_list = tf.train.BytesList(value=[value]))
    

def write_TF(path, train_addrs,train_labels):
    train_filename = path
    
    writer = tf.python_io.TFRecordWriter(train_filename)
    
    for i in range(len(train_addrs)):
        print(i,end=' ')
        if not i % 10:
            print ("Train data: {}/{}".format(i, len(train_addrs)))
            sys.stdout.flush()
    
        img = load_image(train_addrs[i])
        print("Image shape:", end= " ")
        print(img.shape, end = " ")
        img = img.tostring()
        print("Image shape after tostring:", end= " ")
        print(len(img), end = " ")
        img=tf.compat.as_bytes(img)
        label = train_labels[i]

        feature = {'train/label': _int64_feature(label),
                  'train/image':_bytes_feature(img)}

        example = tf.train.Example(features= tf.train.Features(feature = feature))

        writer.write(example.SerializeToString())
        

    writer.close()
    sys.stdout.flush()



def main():
<<<<<<< HEAD
    image_folder_path ="ISIC-2017_Validation_Data/*.jpg"
    csv_file_path = ""
    csv_file_name = "ISIC-2017_Validation_Part3_GroundTruth.csv"
    train_filename_path = "/home/mudit/Skin Lesion Classification/TFrecord_Datasets/Melanoma_validation_224_uint8.tfrecords"
=======
    image_folder_path ="/home/mudit/Skin Lesion Classification/ISIC-2017_Validation_Data/*.jpg"
    csv_file_path = "/home/mudit/Skin Lesion Classification/"
    csv_file_name = "ISIC-2017_Validation_Part3_GroundTruth.csv"
    train_filename_path = "/home/mudit/Skin Lesion Classification/TFrecord_Datasets/Melanoma_validation_uint8.tfrecords"
>>>>>>> c2e9d39f27e12a8d028b142ed4224633a2137cc6
    
    print("listing label")
    addrs, labels = list_label(csv_file_path, csv_file_name,image_folder_path)
    
    write_TF(train_filename_path,addrs, labels)


# In[28]:


main()

