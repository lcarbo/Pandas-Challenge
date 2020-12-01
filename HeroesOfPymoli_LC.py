#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[2]:


# Dependencies and Setup
import pandas as pd

#Load the datafile
datafile = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(datafile)


# In[3]:


purchase_data_df=pd.DataFrame(purchase_data)
purchase_data_df


# ## Player Count

# * Display the total number of players
# 

# In[4]:


#extract the list of players by identifying unique SNs
unique_players = purchase_data_df["SN"].unique()


# In[5]:



#count how many players are in the list of unique SNs 
player_count = len(unique_players)
player_count


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[6]:


#identify unique items 
item_list = purchase_data_df["Item Name"].unique()
unique_items = len(item_list)

#calculate Average Price per item
avg_price =purchase_data_df["Price"].mean()

#calculate total revenue 
total_rev = purchase_data_df["Price"].sum()


#count total number of purchases 
total_purchases = purchase_data_df["Purchase ID"].count()


#combine stats into a summary data frame 
purchase_summary = pd.DataFrame({"Unique Items": [unique_items], "Average Price": [avg_price], 
                                 "Number of Purchases": [total_purchases], "Total Revenue": [total_rev]})

#convert price columns into a currency format
purchase_summary["Average Price"] = purchase_summary["Average Price"].astype(float).map(
    "${:,.2f}".format)
purchase_summary["Total Revenue"] = purchase_summary["Total Revenue"].astype(float).map(
    "${:,.2f}".format)

#display the summary dataframe
purchase_summary.head()


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[7]:


#Use loc to extract relevant demographic information 
player_demog=purchase_data_df.loc[:,["Gender","SN", "Age"]]

#count number of unique players per gender 
gender_counts=player_demog.groupby(["Gender"]).nunique()["SN"]

#calculate percentage of players per gender
gender_percent=gender_counts/player_count

#capture these stats in a dataframe 
gender_demogs=pd.DataFrame({"Total Count": gender_counts, "Percentage of Players": gender_percent})
gender_demogs["Percentage of Players"]= gender_demogs["Percentage of Players"].astype(float).map(
    "{:,.2%}".format)

gender_demogs=gender_demogs.sort_values("Total Count", ascending=False)

gender_demogs


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[8]:


#group original dataset by gender column to run basic calculations based on number of purchases
gender_purchase_total = purchase_data_df.groupby(["Gender"]).sum()["Price"].rename("Total Purchase Value")
gender_average = purchase_data_df.groupby(["Gender"]).mean()["Price"].rename("Average Purchase Price")
gender_purchase_count = purchase_data_df.groupby(["Gender"]).count()["Price"].rename("Purchase Count")

#account for players making multiple purchases by identifying how many unique SNs there are per gender 
gender_person_count = purchase_data_df.groupby(["Gender"]).nunique()["SN"].rename("Person Count")

#use the person count to calculate avg price per person as opposed to per transaction
avg_per_person=gender_purchase_total/gender_person_count

#put calculations into a dataframe and sort 
gender_data=pd.DataFrame({"Purchase Count": gender_purchase_count, "Average Purchase Price":gender_average, 
                          "Total Purchase Value":gender_purchase_total, "Average Purchase per Person":avg_per_person})

gender_data=gender_data.sort_values("Total Purchase Value", ascending=False)

#format prices as currency
gender_data["Total Purchase Value"] = gender_data["Total Purchase Value"].astype(float).map(
    "${:,.2f}".format)
gender_data["Average Purchase Price"] = gender_data["Average Purchase Price"].astype(float).map(
    "${:,.2f}".format)
gender_data["Average Purchase per Person"] = gender_data["Average Purchase per Person"].astype(float).map(
    "${:,.2f}".format)

#print the data frame
gender_data


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[9]:


#create bins of ages, then label them accordingly

age_bins=[0,9.90,14.90,19.90,24.90,29.90,34.90,39.90,9999]
group_names=["<10", "10-14","15-19", "20-24", "25-29", "30-34", "35-39","40+"]


#cut the data by the defined bins 
player_demog["Age Ranges"]=pd.cut(player_demog["Age"],age_bins,labels=group_names)

##account for players making multiple purchases by identifying how many unique SNs there are per age group
age_person_count = purchase_data_df.groupby([player_demog["Age Ranges"]]).nunique()["SN"].rename("Person Count")

#calculate percentage
age_percentage=age_person_count/player_count

#put the values into a dataframe, indexed by age ranges
age_demogs=pd.DataFrame({"Player Count":age_person_count, "Percentage of Players":age_percentage})

#format data as percent 
age_demogs["Percentage of Players"]= age_demogs["Percentage of Players"].astype(float).map(
    "{:,.2%}".format)

#Sort the data and print the new dataframe 
age_demogs=age_demogs.sort_index()
age_demogs


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[10]:


#use the previously set age groups
player_demog["Age Ranges"]=pd.cut(player_demog["Age"],age_bins,labels=group_names)

#run the basic calculations grouped by the establish age ranges 
age_purchase_total = purchase_data_df.groupby([player_demog["Age Ranges"]]).sum()["Price"].rename("Total Purchase Value")
age_average = purchase_data_df.groupby([player_demog["Age Ranges"]]).mean()["Price"].rename("Average Purchase Price")
age_purchase_count = purchase_data_df.groupby([player_demog["Age Ranges"]]).count()["Price"].rename("Purchase Count")

#use the person count to calculate avg price per person as opposed to per transaction
age_person_average=age_purchase_total/age_person_count

#put calculations into a dataframe
age_purchase_data=pd.DataFrame({"Purchase Count":age_purchase_count, "Average Purchase Price":age_average, 
                                   "Total Purchase Value": age_purchase_total, "Player Count":age_person_count, "Average Purchase per Person": age_person_average})
#format price columns
age_purchase_data["Total Purchase Value"] = age_purchase_data["Total Purchase Value"].astype(float).map(
    "${:,.2f}".format)
age_purchase_data["Average Purchase Price"] = age_purchase_data["Average Purchase Price"].astype(float).map(
    "${:,.2f}".format)
age_purchase_data["Average Purchase per Person"] = age_purchase_data["Average Purchase per Person"].astype(float).map(
    "${:,.2f}".format)

#display 
age_purchase_data


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[11]:


#extract relevant data columns 
player_purchases= purchase_data_df.loc[:,["SN", "Purchase ID", "Price"]]

#run the basic calculations grouped by SN
player_total_purchase = player_purchases.groupby(["SN"]).sum()["Price"].rename("Total Purchase Value")
player_purchase_count = player_purchases.groupby(["SN"]).count()["Purchase ID"].rename("Purchase Count")
player_avg_purchase = player_total_purchase/player_purchase_count 

#put calculated values into a new dataframe and sort by total purchase value
player_purchase_stats = pd.DataFrame({"Purchase Count":player_purchase_count, "Average Purchase Price":player_avg_purchase,
                                     "Total Purchase Value":player_total_purchase})

player_purchase_stats=player_purchase_stats.sort_values("Total Purchase Value", ascending=False)

#format price columns 
player_purchase_stats["Total Purchase Value"] = player_purchase_stats["Total Purchase Value"].astype(float).map(
    "${:,.2f}".format)

player_purchase_stats["Average Purchase Price"] = player_purchase_stats["Average Purchase Price"].astype(float).map(
    "${:,.2f}".format)

#display the top 5
player_purchase_stats.head(5)


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, average item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[12]:


#extract relevant data columns 
item_data=purchase_data_df.loc[:,["Item ID","Item Name", "Purchase ID", "Price"]]

#run the basic calculation, grouped by both Item ID and Name 
item_count=item_data.groupby(["Item ID", "Item Name"]).count()["Purchase ID"].rename("Purchase Count")
item_total=item_data.groupby(["Item ID", "Item Name"]).sum()["Price"].rename("Total Purchase Value")
item_price=item_data.groupby(["Item ID", "Item Name"]).mean()["Price"].rename("Item Price")


#capture calculations in a new dataframe and sort by number of purchases per item
item_summary=pd.DataFrame({"Purchase Count":item_count, "Item Price": item_price, 
                           "Total Purchase Value":item_total})

item_summary=item_summary.sort_values("Purchase Count", ascending=False)

#format the price columns
item_summary["Item Price"] = item_summary["Item Price"].astype(float).map("${:,.2f}".format)
item_summary["Total Purchase Value"] = item_summary["Total Purchase Value"].astype(float).map("${:,.2f}".format)

#print top 5 items by purchase count
item_summary.head(5)


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[14]:


#recall the dataframe
item_summary=pd.DataFrame({"Purchase Count":item_count, "Item Price": item_price, 
                           "Total Purchase Value":item_total})

#sort the data frame by purchase value this time
item_summary=item_summary.sort_values("Total Purchase Value", ascending=False)

#reformat price columns 
item_summary["Item Price"] = item_summary["Item Price"].astype(float).map("${:,.2f}".format)
item_summary["Total Purchase Value"] = item_summary["Total Purchase Value"].astype(float).map("${:,.2f}".format)

#print top 5 items by total purchase value
item_summary.head(5)


# In[ ]:




