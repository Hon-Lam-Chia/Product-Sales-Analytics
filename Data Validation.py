import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('product_sales.csv')

#print(df['sales_method'].value_counts())
#Replacing 'email' with 'Email' and 'call' with 'Call'
df['sales_method'] = df['sales_method'].replace({'email': 'Email', 'call': 'Call', 'em + call': 'Email + Call'})
#print(df['sales_method'].value_counts())


#print(df.isna().sum())
#print(df.isna().sum()/df.shape[0] * 100)

# Imputation of 'revenue' column by subgroup mean
revdict = df.groupby("sales_method")['revenue'].mean().to_dict()
#print(revdict)
df['revenue'] = df.groupby("sales_method")['revenue'].fillna(df['sales_method'].map(revdict))
#print(df.isna().sum())

# Removal of outliers in 'years_as_customer' column
age_of_company = datetime.datetime.now().year - 1984  # The company was established in 1984
df = df[df['years_as_customer'] <= age_of_company]


custom_order = ['Email', 'Call', 'Email + Call']


# 1)  Frequency of Sales Methods

##Total Revenue
# 2)  Total Revenue by Sales Methods 

# 3)  Average Revenue by Sales Method

##Total Volume Sold
# 4)  Total Number of New Products Sold by Sales Method

# 5)  Average Number of New Products Sold by Sales Method


sales_count = df['sales_method'].value_counts().reset_index()
sales_count.columns = ['sales_method', 'count']


total_revenue = df.groupby('sales_method')['revenue'].sum().reset_index()

avg_revenue = df.groupby('sales_method')['revenue'].mean().reset_index()

total_nb_sold = df.groupby('sales_method')['nb_sold'].sum().reset_index()

avg_nb_sold = df.groupby('sales_method')['nb_sold'].mean().reset_index()

#Arranging all dataframe's categories in the same manner
dataframes = {
    'sales_count': sales_count,
    'total_revenue': total_revenue,
    'avg_revenue': avg_revenue,
    'total_nb_sold': total_nb_sold,
    'avg_nb_sold': avg_nb_sold
}

# Your desired order
custom_order = ['Email', 'Call', 'Email + Call']  # Example order

# Apply categorical ordering to each DataFrame
for name, df_ in dataframes.items():
    df_['sales_method'] = pd.Categorical(
        df_['sales_method'],
        categories=custom_order,
        ordered=True
    )
    dataframes[name] = df_.sort_values('sales_method')  # Optional: sort by the order

sales_count = dataframes['sales_count']
total_revenue = dataframes['total_revenue']
avg_revenue = dataframes['avg_revenue']
total_nb_sold = dataframes['total_nb_sold']
avg_nb_sold = dataframes['avg_nb_sold']



# Create subplot layout
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=[
        "1) Frequency of Sales Methods",
         "",  # leave 2nd cell empty
        "2) Total Revenue by Sales Method",
        "3) Avg Revenue by Sales Method",
        "4) Total New Products Sold",
        "5) Avg New Products Sold",
    ]
)

# Add bar charts
fig.add_trace(go.Bar(x=sales_count['sales_method'], y=sales_count['count'], name="Frequency"), row=1, col=1)
fig.add_trace(go.Bar(x=total_revenue['sales_method'], y=total_revenue['revenue'], name="Total Revenue"), row=2, col=1)
fig.add_trace(go.Bar(x=avg_revenue['sales_method'], y=avg_revenue['revenue'], name="Avg Revenue"), row=2, col=2)

fig.add_trace(go.Bar(x=total_nb_sold['sales_method'], y=total_nb_sold['nb_sold'], name="Total Sold"), row=3, col=1)
fig.add_trace(go.Bar(x=avg_nb_sold['sales_method'], y=avg_nb_sold['nb_sold'], name="Avg Sold"), row=3, col=2)

fig.update_layout(
    height=700,
    width=1000,
    title_text="Sales Method Comparison Dashboard",
    showlegend=False
)


fig.show()



##Conversion Efficiency
# 6)   nb_sold / nb_site_visits
'''
CE = round((df.groupby('sales_method')['nb_sold'].mean() / 
      df.groupby('sales_method')['nb_site_visits'].mean()) * 100, 2)

CE = CE.reset_index(name='Conversion Efficiency')
print(CE)

fig2 = px.bar(CE, x='sales_method', y='Conversion Efficiency')
fig2.show()
'''

##Average Revenue per Product	
# 7) sum(revenue) / sum(nb_sold)
'''
ARP = round(df.groupby('sales_method')['revenue'].sum() / 
      df.groupby('sales_method')['nb_sold'].sum(), 2)

ARP = ARP.reset_index(name='Average Revenue per Product')
print(ARP)

fig3 = px.bar(ARP, x='sales_method', y='Average Revenue per Product')
fig3.show()
'''

##Customer Engagement
# 8) avg(nb_site_visits)
'''
CusEngage = round(df.groupby('sales_method')['nb_site_visits'].mean(), 2)
CusEngage = CusEngage.reset_index(name='Average Number of Site Visits')
print(CusEngage)

fig4 = px.bar(CusEngage, x='sales_method', y='Average Number of Site Visits')
fig4.show()
'''

##Revenue per Customer
# 9) sum(revenue) / count(customer_id)
'''
RpC = round(df.groupby('sales_method')['revenue'].sum() / df.groupby('sales_method')['customer_id'].count(), 2)
RpC = RpC.reset_index(name='Revenue per Customer')
print(RpC)

fig5 = px.bar(RpC, x='sales_method', y='Revenue per Customer')
fig5.show()
'''

## Site Visits Over Time From New Product Launch
# 10)
'''
AveSV = round(df.groupby("week")['nb_sold'].mean(), 2)
print(AveSV)
AveSV = AveSV.reset_index(name='Average Number of Site Visits')
print(AveSV)

fig6 = px.line(AveSV, x="week", y='Average Number of Site Visits', title="Site Visits Over Time From New Product Launch")
fig6.show()
'''

## Histogram of Revenue
fig7 = px.histogram(df, x="revenue", nbins=10)
fig7.show()