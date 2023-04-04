#!/usr/bin/env python
# coding: utf-8

# # ----Business Problem----

# ## In recent years, City Hotel and Resort Hotel have seen high cancellation rates. Each hotel is now dealing with number of issues as a result, including fewer revenues and less than ideal hotel room use. Consequently , lowering cancellation rates is both hotels' primary goal in order to increase thier efficiency in generating revenue, and for us to offer thorough business advice to address this problem.

# ## The analysis of hotel booking cancellations as well as other factors that have no bearing on their business and yearly revenue generation are the main topics of this report.

# # ----Research Questions----

# ### 1. What are the variables that affect hotel reservation cancellations?

# ### 2. How can we make hotel reservations cancellations better?

# ### 3. How will hotels be assisted in making pricing and promotional decisions?

# # Importing Libraries

# In[1]:


from warnings import filterwarnings
filterwarnings ("ignore")
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# # Loading the Dataset

# In[2]:


df= pd.read_csv("C:/Users/satya/OneDrive/Desktop/New folder/hotel_bookings.csv")


# In[3]:


df.head()


# In[4]:


df.shape


# In[5]:


df.columns


# In[6]:


df.info()


# In[7]:


df['reservation_status_date']=pd.to_datetime(df['reservation_status_date'])


# In[8]:


df.info()


# In[9]:


df.describe()


# In[10]:


df.describe(include ='object')


# In[11]:


for col in df.describe(include ='object').columns:
    print(col)
    print(df[col].unique())
    print('-'*50)


# In[12]:


df.isnull().sum()


# In[13]:


df.drop(['company','agent'], axis =1 , inplace =True)
df.dropna(inplace=True)


# In[14]:


df.isnull().sum()


# In[15]:


df.describe()


# In[16]:


df['adr'].plot(kind="box")


# In[17]:


df= df[df['adr']<5000]


# In[18]:


df.describe()


# # Data Analysis and Visualizations

# In[19]:


cancelled_perc = df['is_canceled'].value_counts(normalize = True)
print(cancelled_perc)

plt.figure(figsize=(5,4))
plt.title('Reservation status count')
plt.bar(['Not canceled', 'Canceled'],df['is_canceled'].value_counts(), edgecolor = 'k', width= 0.7)
plt.show()


# ## The accompanying bar graph shows the percentage of reservations that are canceled and those that are not. It is obvious that there are still a significant number of reservations that have not been canceled. There are still 37% of clients who canceled their reservation, which has a significant impact on the hotels' earnings.

# In[20]:


plt.figure(figsize=(8,4))
ax1=sns.countplot(x = 'hotel', hue = 'is_canceled',data = df, palette='Blues')
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Reservation status in different hotels', size =20)
plt.xlabel('hotel')
plt.ylabel('number of reservations')


# ## In comparison to resort hotels, city hotels have more bookings. It's possible that resort hotels are more expensive than those in cities.

# In[21]:


resort_hotel = df[df['hotel']== 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize=True)


# In[22]:


city_hotel = df[df['hotel']== 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize=True)


# In[23]:


resort_hotel= resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel= city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[24]:


plt.figure(figsize=(20,8))
plt.title('Average Daily Rate in City and Resort Hotel', fontsize = 30)
plt.plot(resort_hotel.index, resort_hotel['adr'], label = 'Resort Hotel')
plt.plot(city_hotel.index, city_hotel['adr'], label = 'City Hotel')
plt.legend(fontsize = 20)
plt.show()


# ## The line graph above shows that, on certain days , the average daily rate for city hotel is less than that of resort hotel, and on other days, it is even less. It goes without saying that weekends and holidays may see a rise in resort hotel rates.

# In[25]:


df['month']= df['reservation_status_date'].dt.month
plt.figure(figsize = (16,8))
ax1 = sns.countplot(x = 'month', hue = 'is_canceled', data = df, palette= 'bright')
legend_labels,_= ax1.get_legend_handles_labels()
plt.title('Reservation status per month', size = 20)
plt.xlabel('month')
plt.ylabel('number of reservations')
plt.legend(['not_canceled', 'canceled'])
plt.show()


# ## We have developed the grouped bar graph to analyze the months with the highest and lowest reservation levels according to reservation status. As can be seen, both the number of confirmed reservations and the number of canceled reservations are largest in the month of August, whereas January is the month with the most canceled reservations.

# In[26]:


plt.figure(figsize = (15,10))
plt.title('ADR per month', fontsize = 30)
sns.barplot('month', 'adr', data= df[df['is_canceled']==1].groupby('month')[['adr']].sum().reset_index())
plt.show()


# ## This bar graph demonstrates that cancellations are most common when prices are greatest and are least common when they are lowest. Therefore, the cost of the accommodation is solely responsible for the cancellation.

# ## Now , let's see which country has the highest reservation canceled.

# In[27]:


cancelled_data = df[df['is_canceled'] == 1]
top_10_country = cancelled_data ['country'].value_counts()[:10]
plt.figure(figsize = (8,8))
plt.title('Top 10 countries with reservation cancelled')
plt.pie(top_10_country, autopct = '%.2f', labels= top_10_country.index)
plt.show()


# ## The top country is Portugal with the highest number of cancellations.

# In[28]:


df['market_segment'].value_counts()


# In[29]:


df['market_segment'].value_counts(normalize= True)


# In[34]:


cancelled_data['market_segment'].value_counts(normalize= True)


# ## From above observations we see that , around 46% of the clients come from online travel agencies , whereas 27% come from groups. Only 4% of clients book hotels directly by visiting them and making reservations.

# In[31]:


cancelled_df_adr = cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace = True)
cancelled_df_adr.sort_values('reservation_status_date', inplace=True)

not_cancelled_data = df[df['is_canceled']==0]
not_cancelled_df_adr = not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index(inplace= True)
not_cancelled_df_adr.sort_values('reservation_status_date', inplace= True)



plt.figure(figsize= (20,6))
plt.title('Average Daily Rate')
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label='not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label = 'cancelled')
plt.legend()


# In[32]:


cancelled_df_adr = cancelled_df_adr[(cancelled_df_adr['reservation_status_date']>'2016') & (cancelled_df_adr['reservation_status_date']<'2017-09')]
not_cancelled_df_adr = not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date']>'2016') & (not_cancelled_df_adr['reservation_status_date']<'2017-09')]


# In[33]:


plt.figure(figsize= (20,6))
plt.title('Average Daily Rate', fontsize = 20)
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label='not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label = 'cancelled')
plt.legend(fontsize =  20)
plt.show()


# ## As seen in the graph , reservations are canceled when the average daily rate is higher than when it is not canceled. It clearly proves all the above analysis, that the higher price leads to higher cancellation.

# # SUGGESTIONS:-

# ## 1. Cancellations rates rise as the price does. In order to prevent cancellations of reservations, hotels could work on their pricing strategies and try to lower the rates for specific hotels based on locations. They can also provide some discounts to the consumers.

# ## 2. As the ratio of the cancellation and not cancellation of the resort hotel is higher in the resort hotel than the city hotels. So the hotels should provide a reasonable discount on the room prices on weekends or on holidays.

# ## 3. In the month of January, hotels can start campaigns or marketing with a reasonable amount to increase their revenue as the cancellation is the highest in this month.

# ## 4. They can also increase the quality of their hotels and their services mainly in Portugal to reduce the cancellation rate.

# In[ ]:




