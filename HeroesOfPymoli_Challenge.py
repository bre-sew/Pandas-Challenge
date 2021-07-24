#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and setup
import pandas as pd

# File to load
file_to_load = "./purchase_data.csv"

# Read purchasing file and store into Pandas data frame
PurchaseData = pd.read_csv(file_to_load)

PurchaseData


# ## Player Count

# * Display the total number of players
# 

# In[2]:


# Find unique players
players = PurchaseData["SN"].unique()
players

# Count the players
playerscount=len(players)
print(f'Total Players: {playerscount}')


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

# In[3]:


# Identify the unique items
UniqueItems = PurchaseData["Item ID"].unique()

# Count the items
ItemsCount = len(UniqueItems)
ItemsCount


# In[4]:


# Find the average purchase price 
AvePrice = PurchaseData["Price"].mean()
AvePrice


# In[5]:


# Find the number of purchases
PurchaseCount = len(PurchaseData["Purchase ID"])
PurchaseCount


# In[6]:


# Find the total revenue
Revenue = PurchaseData["Price"].sum()
Revenue


# In[7]:


# Create a data frame for the analysis
PurchaseAnalysis_df = pd.DataFrame({"Unique Items": [ItemsCount],"Ave Purchase Price":[AvePrice],
    "Number of Purchases":[PurchaseCount],"Total Revenue":[Revenue]})

PurchaseAnalysis_df["Ave Purchase Price"] = PurchaseAnalysis_df["Ave Purchase Price"].map("${:.2f}".format)
PurchaseAnalysis_df["Total Revenue"] = PurchaseAnalysis_df["Total Revenue"].map("${:,.2f}".format)

PurchaseAnalysis_df


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

# In[8]:


# Check to see if there are stray values
PurchaseData.value_counts("Gender")


# In[9]:


# Extract players and gender columns
GenderAnalysis = PurchaseData.loc[:,["SN","Gender"]]
GenderAnalysis


# In[10]:


# Drop the duplicates in the SN column
GenderAnalysis = GenderAnalysis.drop_duplicates(subset=["SN"])
GenderAnalysis


# In[11]:


# Group the data by gender
GenderAnalysis_df = GenderAnalysis.groupby(["Gender"])
GenderDemo_df = GenderAnalysis_df.count()

# Rename the SN column
GenderDemo_df = GenderDemo_df.rename(columns={"SN":"Count"})

# Find the percentages and format
GenderDemo_df["Percent of Players"] = GenderDemo_df["Count"]/GenderDemo_df["Count"].sum()*100
GenderDemo_df["Percent of Players"] = GenderDemo_df["Percent of Players"].map("{:.1f}%".format)
GenderDemo_df


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

# In[12]:


# Group by gender
PurchaseAnalysisGender_df = PurchaseData.groupby(["Gender"])

# Find the number of purchases
PurchaseCountGender = PurchaseAnalysisGender_df["Purchase ID"].count()
PurchaseCountGender

# Find the average price
AveragePriceGender = PurchaseAnalysisGender_df["Price"].mean()
AveragePriceGender

# Find the total purchase value
TotalPurchaseGender = PurchaseAnalysisGender_df["Price"].sum()
TotalPurchaseGender

# Find the average purchase total per person by gender
# Find the purchase total for each person
PurchaseAnalysisGender_df2 = PurchaseData.groupby(["SN"])
PurchaseTotalPerson = PurchaseAnalysisGender_df2["Price"].sum()
PurchaseTotalPerson

# Merge the data sets by person
MergedPlayers = pd.merge(GenderAnalysis, PurchaseTotalPerson,on="SN")
MergedPlayers

# Group by gender
MergedPlayersGrouped = MergedPlayers.groupby(["Gender"])
AveTotalPersonGender = MergedPlayersGrouped["Price"].mean()
AveTotalPersonGender

# Create a summary table
SummaryTable = pd.merge(PurchaseCountGender,AveragePriceGender,on="Gender")
SummaryTable=SummaryTable.rename(columns={"Purchase ID":"Purchase Count","Price":"Average Purchase Price"})

SummaryTable = pd.merge(SummaryTable,TotalPurchaseGender,on="Gender")
SummaryTable = SummaryTable.rename(columns={"Price":"Total Purchase Value"})

SummaryTable = pd.merge(SummaryTable,AveTotalPersonGender,on="Gender")
SummaryTable = SummaryTable.rename(columns={"Price":"Ave Total Purchase per Person"})

# Format the values
SummaryTable["Average Purchase Price"] = SummaryTable["Average Purchase Price"].map("${:,.2f}".format)
SummaryTable["Total Purchase Value"] = SummaryTable["Total Purchase Value"].map("${:,.2f}".format)
SummaryTable["Ave Total Purchase per Person"] = SummaryTable["Ave Total Purchase per Person"].map("${:,.2f}".format)
SummaryTable


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

# In[13]:


PurchaseData


# In[14]:


# Find bounds of age
print(PurchaseData["Age"].min())
print(PurchaseData["Age"].max())


# In[15]:


# Create bins
bins = [6,10,14,18,22,26,30,34,38,42,46]
binlabels = ["6-10","10-14","14-18","18-22","22-26","26-30","30-34",
            "34-38","38-42","42-46"]


# In[16]:


# Place the data into bins
groupings = pd.cut(PurchaseData["Age"],bins,labels=binlabels,)
groupings


# In[17]:


# Add the data back into the dataframe 
PurchaseData["Age Group"] = groupings
PurchaseData


# In[18]:


# Find the numbers and percentages by age groups

AgeGroupReduced_df = PurchaseData.loc[:,["SN","Age","Age Group"]]
AgeGroupReduced_df


# In[19]:


# Drop the player duplicates to get unique players only
AgeGroupReduced_df =  AgeGroupReduced_df.drop_duplicates(subset=["SN"])
AgeGroupReduced_df


# In[20]:


# Find the count of each age group
AgeCounts = AgeGroupReduced_df["Age Group"].value_counts()
AgeCounts

# Find the total players
TotalPlayers = AgeGroupReduced_df["SN"].count()
print(TotalPlayers)

SummaryAgeGroups_df = pd.DataFrame(AgeCounts)
SummaryAgeGroups_df


# In[21]:


SummaryAgeGroups_df = SummaryAgeGroups_df.rename(columns={"Age Group":"Count"})
SummaryAgeGroups_df


# In[22]:


Percentages = AgeCounts/TotalPlayers*100
Percentages

SummaryAgeGroups_df["Percentage"]=Percentages
SummaryAgeGroups_df["Percentage"] = SummaryAgeGroups_df["Percentage"].map("{:,.2f}%".format)

SummaryAgeGroups_df.sort_index(inplace=True)
SummaryAgeGroups_df


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

# In[23]:


# Group by age group
AgeGrouping_df = PurchaseData.groupby(["Age Group"])

# Find purchase count by age group
AgeGroupPurchases = AgeGrouping_df["Purchase ID"].count()
AgeGroupPurchases

# Find average purchase price by age group
AgeGroupAvePrice = AgeGrouping_df["Price"].mean()
AgeGroupAvePrice

# Find total purchase value by age group
AgeGroupPurchaseValue = AgeGrouping_df["Price"].sum()
AgeGroupPurchaseValue


# In[24]:


# Find average purchase total per person by age group
# Extract SD and Age Group columns
AgeGrouping_df2 = PurchaseData.loc[:,["SN","Age Group"]]
AgeGrouping_df2 = AgeGrouping_df2.drop_duplicates(subset=["SN"])
AgeGrouping_df2

# Merge the dataframes
MergedPlayers2 = pd.merge(AgeGrouping_df2,PurchaseTotalPerson,on="SN")
MergedPlayers2

# Group by age and find the average price
GroupedMergedPlayers2 = MergedPlayers2.groupby(["Age Group"])
AveTotalPersonAge = GroupedMergedPlayers2["Price"].mean()
AveTotalPersonAge


# In[25]:


# Create a summary table
SummaryAge = pd.merge(AgeGroupPurchases,AgeGroupAvePrice,on="Age Group")
SummaryAge = SummaryAge.rename(columns={"Purchase ID":"Purchase Count","Price":"Average Purchase Price"})

SummaryAge = pd.merge(SummaryAge,AgeGroupPurchaseValue,on="Age Group")
SummaryAge = SummaryAge.rename(columns={"Price":"Total Purchase Value"})

SummaryAge = pd.merge(SummaryAge,AveTotalPersonAge,on="Age Group")
SummaryAge = SummaryAge.rename(columns={"Price":"Ave Purchase Total Per Person"})

# Format the summary table
SummaryAge["Average Purchase Price"] = SummaryAge["Average Purchase Price"].map("${:,.2f}".format)
SummaryAge["Total Purchase Value"] = SummaryAge["Total Purchase Value"].map("${:,.2f}".format)
SummaryAge["Ave Purchase Total Per Person"] = SummaryAge["Ave Purchase Total Per Person"].map("${:,.2f}".format)
SummaryAge


# In[ ]:





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

# In[26]:


# Remove the columns needed - player and price
TopSpenders = PurchaseData.loc[:,["SN","Price"]]

# Group by player
TopSpenders = TopSpenders.groupby("SN")
TopSpenders = TopSpenders["Price"].sum()
TopSpenders_df = pd.DataFrame(TopSpenders)
TopSpenders_df


# In[27]:


# Find the top 5 spenders
Top5 = TopSpenders_df.sort_values("Price",ascending = False)
Top5 = Top5.head()
Top5 = pd.DataFrame(Top5)
Top5


# In[28]:


# Create the summary table
TopSpenderSummary = Top5
TopSpenderSummary = TopSpenderSummary.rename(columns={"Price":"Total Purchase Value"})
TopSpenderSummary


# In[ ]:





# In[29]:


# Count the purchases
TopSpenderPurchaseCount = PurchaseData.loc[:,["SN","Price"]]

# Group by player
TopSpenderPurchaseCount = TopSpenderPurchaseCount.groupby("SN")
TopSpenderPurchaseCount = TopSpenderPurchaseCount["Price"].count()

TopSpenderPurchaseCount = pd.DataFrame(TopSpenderPurchaseCount)

# Extract the top 5
TopSpenderPurchaseCount = TopSpenderPurchaseCount.loc[["Lisosia93","Idastidru52","Chamjask73","Iral74","Iskadarya95"],:]

TopSpenderSummary["Purchase Count"] = TopSpenderPurchaseCount
TopSpenderSummary


# In[30]:


# Find the average purchase price per top 5 spender
TopSpenderAvePrice = PurchaseData.loc[:,["SN","Price"]]

# Group by player and find the average
TopSpenderAvePrice = TopSpenderAvePrice.groupby("SN")
TopSpenderAvePrice = TopSpenderAvePrice["Price"].mean()
TopSpenderAvePrice = pd.DataFrame(TopSpenderAvePrice)

# Extract the top 5
TopSpenderAvePrice = TopSpenderAvePrice.loc[["Lisosia93","Idastidru52","Chamjask73","Iral74","Iskadarya95"],:]

# Add to the summary table
TopSpenderSummary["Average Purchase Price"] = TopSpenderAvePrice
TopSpenderSummary


# In[31]:


# Format the data
TopSpenderSummary["Total Purchase Value"] = TopSpenderSummary["Total Purchase Value"].map("${:,.2f}".format)
TopSpenderSummary


# In[32]:


TopSpenderSummary["Average Purchase Price"] = TopSpenderSummary["Average Purchase Price"].map("${:,.2f}".format)
TopSpenderSummary


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

# In[33]:


# Pull the necessary columns
PopularItems = PurchaseData.loc[:,["Item ID","Item Name","Price"]]
PopularItems


# In[42]:


PopularItemsGrouped = PopularItems.groupby(["Item ID","Item Name"])
PurchaseCount = PopularItemsGrouped["Price"].count()
PurchaseCount


# In[43]:


PopularItemSummary = pd.DataFrame(PurchaseCount)
PopularItemSummary = PopularItemSummary.rename(columns={"Price":"Purchase Count"})

PopularItemSummary["Average Item Price"] = PopularItemsGrouped["Price"].mean()
PopularItemSummary["Total Purchase Value"] = PopularItemsGrouped["Price"].sum()

PopularItemSummary


# In[44]:


PopularItemSummaryFinal = pd.DataFrame(PopularItemSummary)
PopularItemSummaryFinal = PopularItemSummaryFinal.sort_values("Purchase Count",ascending = False)
PopularItemSummaryFinal


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

# In[45]:


ProfitableItemSummary = PopularItemSummary.sort_values("Total Purchase Value",ascending = False)
ProfitableItemSummary


# In[48]:


ProfitableItemSummary["Average Item Price"] = ProfitableItemSummary["Average Item Price"].map("${:,.2f}".format)
ProfitableItemSummary["Total Purchase Value"] = ProfitableItemSummary["Total Purchase Value"].map("${:,.2f}".format)
ProfitableItemSummary

