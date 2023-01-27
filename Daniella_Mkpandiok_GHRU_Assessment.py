#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing the needed libraries

import pandas as pd
import numpy as np


# In[2]:


df = pd.read_csv("data.csv")


# # Exploring our dataset 

# In[3]:


# Exploring the first few rows of the data
df.head(10)


# In[4]:


# exploring an overview of the data
df.info()


# In[5]:


df.describe()


# In[6]:


# examining the missing values in the dataset
df.isnull().sum() 


# In[ ]:


#This shows there is no missing value, hence we can proceed to answer the questions


# # Question 1: How many samples are there that have failed the contamination check and have contamination

# In[8]:


Q1 = df[(df['confindr.contam_status.check_result'] == 'FAILURE') & (df['confindr.percentage_contamination.metric_value'] > 0.05)]
Q1.shape[0]

This shows that 57 samples have failed the contamination check though contaminated with metric value > 0.05.
# # Question 2: How many samples are there that have less than or equal to 50 contigs and a N50 value of greater than or equal to 750,000

# In[9]:


Q2 = df[(df['quast.# contigs (>= 1000 bp).metric_value'] <= 50) & (df['quast.N50.metric_value'] >= 750000)]
Q2.shape[0]

This shows that 49 samples are there that have less than or equal to 50 contigs and N50 value greater than or equal to 750,000
# # Question 3: Select all numeric columns and rename them to remove the .quast prefix and .metric_value suffix, and rename confindr.percentage_contamination to contamination_percent

# In[17]:


num_col = df.select_dtypes(include='number').columns.tolist()

#remove the suffix quast. from all numerical columns
cols = []
for col in num_col:
    if col[:6] == "quast.":
        col = col[6:]
    cols.append(col)

#remove the prefix .metric_value from all numerical columns
num_cols = []
for col in cols: 
    if col[-13:] == ".metric_value":
        col = col[:-13]
    num_cols.append(col)
    
#replace 'confindr.percentage_contamination' with 'contamination_percent'
num_cols[0] = 'contamination_percent'

#rename all the columns names in the dataframe with the corrected names
col_dict = {}
for key,value in zip(num_col, num_cols):
    col_dict[key] = value
    
df = df.rename(columns=col_dict)
df.head()


# # Question 4: Make a box plot of Total Length (>= 1000 bp)

# In[23]:


import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12,6))
sns.set_style("darkgrid")
sns.boxplot(data=df, x='Total length (>= 1000 bp)', color = "blue")
plt.title("A box plot of Total length (>= 1000 bp)", fontsize=25);


# # Question 5: Pivot the table so that it is "tidy" with one observation per row and have a final column headings of sample_name, metric name

# In[37]:


import numpy as np


# In[38]:


new_df.head()


# In[39]:


transformed_data = pd.pivot_table(df, index = "sample_name", columns = "confindr.contam_status.metric_value")
transformed_data


# In[ ]:


The table shows the pivot table of each unique sample_name, the metrics and its respective values. 


# # Question 6: Make a violin plot for each of the numeric variables in a single plot. 

# In[18]:


#To make a violin plot, We extract the numeric columns from the dataset into a new dataframe called new_df

new_df = df[["contamination_percent", "# contigs (>= 1000 bp)", "N50", "Total length (>= 1000 bp)"]]
new_df.head()


# In[33]:


#Plotting the Violin plot of the numeric variables

plt.figure(figsize = [16, 8])

plt.subplot(2, 2, 1)
sns.violinplot(data=new_df, x="contamination_percent", color = "blue");
plt.title("A Violin Plot of Contamination_Percent", fontsize=14)

plt.subplot(2, 2, 2)
sns.violinplot(data=new_df, x="N50", color = "red");
plt.title("A Violin Plot of N50", fontsize=14)

plt.subplot(2, 2, 3)
sns.violinplot(data=new_df, x="# contigs (>= 1000 bp)", color = "purple");
plt.title("A Violin Plot of # contigs (>= 1000 bp)", fontsize=8)

plt.subplot(2, 2, 4)
sns.violinplot(data=new_df, x="Total length (>= 1000 bp)", color = "black");
plt.title("A Violin Plot of Total length (>= 1000 bp)", fontsize=8)


# In[36]:


#creating a n histogram to vie the distribution of the data
new_df.hist(figsize = (15,15), alpha = 1, color ="black")


# In[ ]:


#This shows that the contamination percent is low (o.e below 5%), hence it is rightly skewed.
#The dataset with N50 are cncentrated around 300000 is normally distributed. the total_length and contamination_percent is rightly skewed.   

