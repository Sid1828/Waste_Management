#!/usr/bin/env python
# coding: utf-8

# In[403]:


import pandas as pd 


# In[404]:


df = pd.read_excel (r"C:\Users\SIDDHARTH EKBOTE\Downloads\Final Waste Management Data (1).xlsx")


# In[405]:


df.head()


# In[406]:


df.tail()


# In[407]:


df.info()


# In[408]:


cols_to_drop = [
    'typeCode',
    'freqCode',
    'refPeriodId',
    'partner2Code',
    'partner2ISO',
    'partner2Desc',
    'classificationSearchCode',
    'isOriginalClassification',
    'isLeaf',
    'customsCode',
    'customsDesc',
    'mosCode',
    'motCode',
    'motDesc',
    'qtyUnitCode',
    'qtyUnitAbbr',
    'isQtyEstimated',
    'altQtyUnitCode',
    'altQtyUnitAbbr',
    'isAltQtyEstimated',
    'isNetWgtEstimated',
    'isGrossWgtEstimated',
    'legacyEstimationFlag',
    'isReported',
    'isAggregate',
    'refYear',
    'reporterCode',
    'reporterISO',
    'flowCode',
    'partnerCode',
    'cmdCode',
    'aggrLevel',
    'qty',
    'grossWgt',
    'cifvalue',
    'primaryValue',
    'classificationCode',
    'partnerISO'
]

df.drop(columns=cols_to_drop, inplace=True,errors='ignore')


# In[409]:


df.head()


# In[410]:


df.isnull()


# In[411]:


df.info()


# In[412]:


df['cmdDesc'] = df['cmdDesc'].replace({
    'Retreaded or used pneumatic tyres of rubber; solid or cushion tyres, tyre treads and tyre flaps, of rubber': 'Rubber',
    'Textiles; worn clothing and other worn articles': 'Textiles',
    'Residual products of the chemical or allied industries, not elsewhere specified or included; municipal waste; sewage sludge; other residual products.': 'Industrial And Municipal Waste',
    'Waste, parings and scrap, of plastics':'Plastic',
    'Waste and scrap of precious metal or of metal clad with precious metal; other waste and scrap containing precious metal compounds, of a kind uses principally for the recovery of precious metal':'Metal'


})


# In[413]:


df.head()


# In[414]:


df.rename(columns={
    'period': 'Year',
    'reporterDesc': 'Reporter',
    'cmdDesc': 'Commodity',
    'flowDesc':'Trade',
    'partnerDesc':'Partner',
    'altQty':'Quantity',
    'netWgt':'Weight',
    'fobvalue':'Fob_Value'
}, inplace=True)


# In[415]:


df.info()


# In[416]:


df.head()


# In[417]:


df.isnull().sum()


# In[418]:


# Drop rows where Weight is missing
df = df.dropna(subset=['Weight'])

# Optional: check if missing values are gone
print(df.isnull().sum())


# In[419]:


df.info()


# In[420]:


#Question 1 Yearly Export Trade Overview
import seaborn as sns
df.groupby('Year')[['Quantity','Weight','Fob_Value']].sum()


# In[421]:


#Question 2 FOB Trend Over the years
import matplotlib.pyplot as plt
import seaborn as sns

# Aggregate by Year
yearly = df.groupby('Year')[['Quantity','Weight','Fob_Value']].sum().reset_index()

# Conversion to human-readable units
yearly['Weight_kt'] = yearly['Weight'] / 1e6        # kilotons
yearly['Fob_million'] = yearly['Fob_Value'] / 1e6  # million USD


# In[422]:


plt.figure(figsize=(12,6))

#sns.lineplot(data=yearly, x='Year', y='Quantity', marker='o', label='Quantity')
#sns.lineplot(data=yearly, x='Year', y='Weight_kt', marker='o', label='Weight (kt)')
sns.lineplot(data=yearly, x='Year', y='Fob_Value', marker='o', label='Fob Value (Million USD)')

plt.title('Trade Data Summary by Year')
plt.ylabel('Value (converted units)')
plt.xlabel('Year')
plt.legend()
plt.show()


# In[423]:


#Question 3 By Weight Export Trend Over the years
plt.figure(figsize=(12,6))
sns.lineplot(data=yearly, x='Year', y='Weight_kt', marker='o', label='Weight (kt)')

plt.title('Trade Data Summary by Year')
plt.ylabel('Value (converted units)')
plt.xlabel('Year')
plt.legend()
plt.show()


# In[424]:


#Question 4 By Quantity Trend Over the years
plt.figure(figsize=(12,6))

sns.lineplot(data=yearly, x='Year', y='Quantity', marker='o', label='Quantity')


plt.title('Trade Data Summary by Year')
plt.ylabel('Value (converted units)')
plt.xlabel('Year')
plt.legend()
plt.show()


# In[647]:


##Question 5 Top Trading Partners
df[df['Year'] == 2015].groupby('Partner')['Fob_Value'].sum().sort_values(ascending=False).head(5)


# In[426]:


top_partners = df[df['Year']==2015].groupby('Partner')['Fob_Value'].sum().sort_values(ascending=False).head(5)

top_partners.plot(kind='bar', color='skyblue')
plt.ylabel('Fob Value (Million USD)')
plt.title('Top 5 Trading Partners (2015)')
plt.show()


# In[427]:


#Question 6 Top Commodity in 2015
df[df['Year'] == 2015].groupby('Commodity')['Weight'].sum().sort_values(ascending=False).head(10)


# In[428]:


top_commodities = df[df['Year']==2015].groupby('Commodity')['Weight'].sum().sort_values(ascending=False).head(10)

top_commodities.plot(kind='barh', color='lightgreen')
plt.xlabel('Weight')
plt.title('Top Commodities by Weight ')
plt.gca().invert_yaxis()
plt.show()


# In[595]:


df['Commodity'] = df['Commodity'].replace({'Waste and scrap of precious metal or of metal clad with precious metal; other waste and scrap containing precious metal compounds, of a kind uses principally for the recovery of precious metal other than goods of heading 85.49':'Metal',
                                          'Electrical and electronic waste and scrap':'Electronics'})


# In[597]:


#Question 6 Top Commodity in recent year 2024
top_commodities = df[df['Year']==2024].groupby('Commodity')['Weight'].sum().sort_values(ascending=False).head(10)

top_commodities.plot(kind='barh', color='lightgreen')
plt.xlabel('Weight')
plt.title('Top Commodities by Weight ')
plt.gca().invert_yaxis()
plt.show()


# In[599]:


#Question 7 Trade by Type
trade_type = df.groupby('Trade')[['Quantity','Weight','Fob_Value']].sum()

trade_type.plot(kind='bar', stacked=False)
plt.title('Total Trade by Type')
plt.ylabel('Sum')
plt.show()


# In[601]:


#8 Year over year growth in Fob Value
annual_fob = df.groupby('Year')['Fob_Value'].sum()
annual_growth = annual_fob.pct_change() * 100

annual_growth.plot(kind='bar', color='orange')
plt.ylabel('Growth (%)')
plt.title('Year-over-Year Growth in Fob Value')
plt.show()


# In[603]:


# Top 5 partners by share of Fob value
partner_trade = df.groupby('Partner')['Fob_Value'].sum()
partner_trade_percent = (partner_trade / partner_trade.sum()) * 100
partner_trade_percent.sort_values(ascending=False).head(5).plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.ylabel('')
plt.title('Top 5 Partners by Share of Fob Value')
plt.show()


# In[604]:


df.groupby(['Partner','Commodity'])['Fob_Value'].sum().reset_index().sort_values(['Partner','Fob_Value'], ascending=[True, False]).groupby('Partner').first()


# In[607]:


# Question 9 Top commodity per partner
top_per_partner = df.groupby(['Partner','Commodity'])['Fob_Value'].sum().reset_index()
top_commodities_partner = top_per_partner.sort_values(['Partner','Fob_Value'], ascending=[True, False]).groupby('Partner').first().head(5)

top_commodities_partner.reset_index().plot(kind='bar', x='Partner', y='Fob_Value', color='purple')
plt.ylabel('Fob Value (Million USD)')
plt.title('Top Commodity per Partner')
plt.show()


# In[608]:


df.groupby('Trade')[['Quantity','Weight','Fob_Value']].sum()


# In[611]:


partner_trade = df.groupby('Partner')['Fob_Value'].sum()
partner_trade_percent = (partner_trade / partner_trade.sum()) * 100
partner_trade_percent.sort_values(ascending=False)


# In[612]:


partner_yearly = df.groupby(['Partner','Year'])['Fob_Value'].sum().reset_index()
partner_yearly['YoY_growth'] = partner_yearly.groupby('Partner')['Fob_Value'].pct_change() * 100


# In[615]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Aggregate Fob_Value by Partner and Year
partner_yearly = df.groupby(['Partner','Year'])['Fob_Value'].sum().reset_index()

# Compute YoY growth (%) per Partner
partner_yearly['YoY_growth'] = partner_yearly.groupby('Partner')['Fob_Value'].pct_change() * 100


# In[617]:


# Pivot so each row = Partner, each column = Year, values = YoY growth
growth_pivot = partner_yearly.pivot(index='Partner', columns='Year', values='YoY_growth')


# In[619]:


# Average YoY growth per partner
avg_growth = partner_yearly.groupby('Partner')['YoY_growth'].mean().sort_values(ascending=False)

# Top 10 partners
top10_partners = avg_growth.head(10).index.tolist()

# Filter original dataframe for these top 10 partners
top10_growth = partner_yearly[partner_yearly['Partner'].isin(top10_partners)]


# In[621]:


growth_pivot = top10_growth.pivot(index='Partner', columns='Year', values='YoY_growth')


# In[623]:


#Question 10 Groth of FOB Over th years
plt.figure(figsize=(12,6))
sns.heatmap(growth_pivot, annot=True, fmt=".1f", cmap='RdYlGn', center=0)
plt.title('Year-over-Year Fob_Value Growth - Top 10 Partners (%)')
plt.xlabel('Year')
plt.ylabel('Partner')
plt.show()


# In[624]:


#Question 11 Growing Trade partners
plt.figure(figsize=(10,6))
sns.barplot(x=avg_growth[top10_partners].values, y=top10_partners, palette='viridis')
plt.xlabel('Average Year-over-Year Growth (%)')
plt.ylabel('Partner')
plt.title('Top 10 Fastest Growing Trade Partners (Fob_Value)')
plt.show()


# In[625]:


top10_df = df[df['Partner'].isin(top10_partners)]


# In[627]:


commodity_trade = top10_df.groupby(['Partner', 'Commodity'])['Fob_Value'].sum().reset_index()


# In[628]:


# Sort by Fob_Value per partner
commodity_trade = commodity_trade.sort_values(['Partner', 'Fob_Value'], ascending=[True, False])

# Pick top 3 commodities per partner
top_commodities_per_partner = commodity_trade.groupby('Partner').head(1)
top_commodities_per_partner


# In[629]:


#Question 12 Top 3 Commodities for Top 10 growing countries
plt.figure(figsize=(12,8))
sns.barplot(data=top_commodities_per_partner, x='Fob_Value', y='Partner', hue='Commodity', dodge=False)
plt.xlabel('Fob Value (USD)')
plt.ylabel('Partner')
plt.title('Top 3 Commodities for Top 10 Fastest Growing Partners')
plt.legend(title='Commodity', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


# In[634]:


df[['Weight', 'Fob_Value']].corr()


# In[635]:


#Question 13 Heavier shipments are more valuable or not.
sns.scatterplot(data=df, x='Weight', y='Fob_Value')
sns.regplot(data=df, x='Weight', y='Fob_Value', scatter=False, color='red')


# In[637]:


#Question 14 Top commodity share per partner
import pandas as pd

# Total Fob_Value per Partner
partner_total = df.groupby('Partner')['Fob_Value'].sum().reset_index().rename(columns={'Fob_Value':'Total_Fob'})

# Total Fob_Value per Partner & Commodity
partner_commodity = df.groupby(['Partner','Commodity'])['Fob_Value'].sum().reset_index()

# Merge to calculate share
partner_commodity = partner_commodity.merge(partner_total, on='Partner')
partner_commodity['Share'] = partner_commodity['Fob_Value'] / partner_commodity['Total_Fob']

# Sort commodities by share per partner
partner_commodity = partner_commodity.sort_values(['Partner','Share'], ascending=[True, False])


# In[638]:


top_commodity_per_partner = partner_commodity.groupby('Partner').head(1).copy()

# Flag partners with high dependence (>70% of total trade)
top_commodity_per_partner['High_Dependence'] = top_commodity_per_partner['Share'] > 0.7

# Display as a table
top_commodity_per_partner[['Partner','Commodity','Fob_Value','Total_Fob','Share','High_Dependence']].reset_index(drop=True)


# In[649]:


#Question 15 Share of Commodity per partner
import pandas as pd

# Step 1: Total Fob_Value per Partner
partner_total = df.groupby('Partner')['Fob_Value'].sum().reset_index()
partner_total = partner_total.rename(columns={'Fob_Value':'Total_Fob'})

# Step 2: Total Fob_Value per Partner & Commodity
partner_commodity = df.groupby(['Partner','Commodity'])['Fob_Value'].sum().reset_index()

# Step 3: Merge to calculate share
partner_commodity = partner_commodity.merge(partner_total, on='Partner')
partner_commodity['Share'] = partner_commodity['Fob_Value'] / partner_commodity['Total_Fob']

# Step 4: Sort commodities by share per partner
partner_commodity = partner_commodity.sort_values(['Partner','Share'], ascending=[True, False])

# Step 5: Keep only top 3 commodities per partner
top_commodities_per_partner = partner_commodity.groupby('Partner').head(3)

# Step 6: Pivot to table format
table_df = top_commodities_per_partner.pivot(index='Partner', columns='Commodity', values='Share').fillna(0)

# Optional: format as percentages
table_df = table_df.applymap(lambda x: f"{x*100:.1f}%")

# Display the table
table_df


# In[ ]:





# In[ ]:





# In[ ]:




