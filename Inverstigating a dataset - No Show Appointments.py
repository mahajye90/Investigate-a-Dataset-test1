#!/usr/bin/env python
# coding: utf-8

# # Project: Investigate a Dataset (Medical Appointment No Shows)
# 
# ## Introduction 
# In this project I will investigate a dataset that contains 110.527 medical appointments of in Brazil and its 14 associated variables. The main variable is whether or not patients show up for their appointment. 
# 
# The other variables are ; PatientId, AppointmentID, The day someone called or registered the appointment, The day of the actuall appointment, Gender, Age , Neighbourhood,  Scholarship, Hipertension, Diabetes, Alcoholism, Handcap, SMS_received , No-show. There are plenty of questions that can be explored using this information. 
# 
# The goals of this investigation is to find the common reasons behind patient no-shows. I will look for each factor and its effects. <br/>
# 

# ## Data Wrangling
# 

# > Importing packages and data csv 

# In[94]:


#Importing packages
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


#   

# In[95]:


#reading dataset
df = pd.read_csv('MedAppt_v0.csv')
df.head(1)


# > Description of tha data 

# In[96]:


#summary of the dataset
df.describe()


# In[97]:


df.info()


# >  Dropping columns that are not useful at this point.
# Some columns can be dropped as ID nummber and appointment ID. <br/>

# In[98]:


#Dropping unnecessary columns ussing pandas 
df.drop(['PatientId', 'AppointmentID'], axis=1, inplace= True)
df.head(1)


# #### Cleaning the data
# > Scheduled Day and Appointment Day contain two types of data that needed to be splited by using datetime function. Then create seperated columns for day , month, year, and time. <br/>

# In[99]:


#split Scheduled Day into date and time 
df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'],errors='coerce')
df['Scheduled_date'] = df['ScheduledDay'].dt.weekday_name 
df['Scheduled_month'] = df['ScheduledDay'].dt.month_name 
df['Scheduled_year'] = df['ScheduledDay'].dt.year
df['Scheduled_time'] = df['ScheduledDay'].dt.time

df['Scheduled_time'] = df['ScheduledDay'].dt.time
#Now we can drop ScheduledDay 
df.drop (['ScheduledDay'], axis=1, inplace=True)
df.head(1)


# In[100]:


#split Appointment Day into date and time 
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
df['Appointment_date'] = df['AppointmentDay'].dt.weekday_name
df['Appointment_month'] = df['AppointmentDay'].dt.month_name 
df['Appointment_year'] = df['AppointmentDay'].dt.year 
df['Appointment_time'] = df['AppointmentDay'].dt.time
#Now we can drop ScheduledDay and Appointment_time(cuz all values are zero)
df.drop (['AppointmentDay'], axis=1, inplace=True)
df.drop (['Appointment_time'], axis=1, inplace=True)

df.head(6)


# ##### Renaming 
# > Rename column No-show to be easy to use 

# In[101]:


# rename no-show to no_show 
df.rename(columns={"No-show": "no_show"}, inplace=True)
df.head(1)


# ### Finding Missing Values 

# In[102]:


#Finding ionly zero column
(df == 0).all()


# In[103]:


#missing vale
df.isnull().sum()


# > We can see that the data are clean at this point.

#  #### Finally the shape and # of unique values for each variables

# In[104]:


df.shape


# In[105]:


#unique values 
df.nunique()


# In[106]:


#unique number of age
np.unique(df.Age)


# # Exploratory Data Analysis  <br />

# ### Gender

# ### Which gender visiting hospital more? <b>

# In[107]:


#using sns to find which gender visiting clinic more
sns.set(style="darkgrid")
sns.countplot(x='Gender',data=df);


# > The number of female is approximately double the number of male.  <br /> <br />
# 
# 

# ## The percentage of  female and male

# In[108]:


df['Gender'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'


# ### Which gender missed more appointment? <br/>

# In[124]:


sns.catplot(x="Gender", col="no_show",

               data=df, kind="count");


# > It seems that there is no difference between these proportion. 

# ## Age 

# #### Calculating the mean age  <br/>

# In[110]:


#calculating the mean of age for ones who missed their appointment
df_noShow = df[df['no_show'] == 'Yes']
df_noShow.mean().Age


# In[111]:


#calculating the mean of age for ones who show

df_Show = df[df['no_show'] == 'No']
df_Show.mean().Age


# > There is a slight differences. <br/>

# #### Age based on gender<br/>

# In[112]:


#plotting age and gender
sns.kdeplot(df.Age[df.Gender == 'M'], color = 'b',shade=True)
sns.kdeplot(df.Age[df.Gender == 'F'],color = 'r',shade=True)
plt.legend(['M','F'])
plt.xlabel('Age');


# ## The percentage of  show and no show

# In[113]:


df['no_show'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'


# ### The effect of sending SMS <br/>

# In[114]:


#the effect of sending SMS 
sns.catplot(x="SMS_received", col="no_show",

                data=df, kind="count");


# > In the no show group, the received SMS has no effect.

# ### The effect of Scholarship, Hipertension, Diabetes, Alcoholism,and  Handcap

# In[115]:


#the effect of Scholarship
sns.catplot(x="Scholarship", col="no_show",

                data=df, kind="count");


# > The majority of people who missed their appointment do not have a Scholarship. 

# In[116]:


#the effect of Hipertension
sns.catplot(x="Hipertension", col="no_show",

                data=df, kind="count");


# > Hipertension seems to have no effect on no shows.

# In[117]:


#the effect of Diabetes
sns.catplot(x="Diabetes", col="no_show",

                data=df, kind="count");


# > Diabetes also have no effect on no shows.

# In[118]:


#the effect of Alcoholism
sns.catplot(x="Alcoholism", col="no_show",

                data=df, kind="count");


# In[119]:


#the effect of  Handcap
sns.catplot(x="Handcap", col="no_show",

                data=df, kind="count");


# > Handcap and Alcoholism have no effect on no shows.

# ### The number of not showing based on neighbourhood <br/>

# ##### Which neighbourhoods have the highest number of no shows? <br/>
# 

# In[120]:


# which neighbourhoods have the highest number of no shows?
show = df[df['no_show'] == 'Yes']
show.groupby('Neighbourhood')['no_show'].count().sort_values(ascending=False).head(5)


# > These are the top 5 neighbourhood in the missing appointment group

# ##### Which neighbourhoods have the lowest number of no shows? <br/>
# 

# In[121]:


show.groupby('Neighbourhood')['no_show'].count().sort_values(ascending=True).head(5)


# ### Neighbourhood vs show and no show <br/>

# In[122]:



plt.figure(figsize=(25,8))
sns.countplot(x='Neighbourhood', hue='no_show', data=df)
plt.xticks(rotation=90);


# 
# ##### The influnce of the day of the week <br/>
# 

# In[123]:


sns.catplot(x="Scheduled_date", col="no_show",

                data=df, kind="count");


# > We can see that there is no significant difference based on the day of week.

# ## Conclusion <br/>
# 

# >The most factor that related to no shows is the neighbourhood. However, the data are limited to explore this factor throughly. <br/>
# 
# >There are some surprising results such as patients show for their appointments despite having no scholarship, also not receiving a SMS. <br/>
# 
# >Females are the majority of the patients but there is no difference between the proportions of no show of females and males. <br/>

# <br/>
