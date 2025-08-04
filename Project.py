import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import statsmodels.api as sm

df = pd.read_csv('product_sales.csv')

#1) Show the first 5 rows of the dataset
#print(df.head())


#2) Show the number of missing values in each column
NASS = df.isnull().sum()/len(df) * 100
#print(NASS) 
# Revenue has 7.16& missing values


# 3) Show the df's general information
#print(df.describe())
#print(df.shape) # (15000, 8)


#4) Show the data types of each column
#print(df.dtypes)
'''
week                   int64
sales_method          object
#customer_id           object
nb_sold                int64
revenue              float64
years_as_customer      int64
nb_site_visits         int64
state                 object
'''

#4) Show the number of unique values in each column
#print(df.nunique())
'''
week                     6
sales_method             5
customer_id          15000
nb_sold                 10
revenue               6743
years_as_customer       42
nb_site_visits          27
state                   50
'''


### Sales method has variation of email and call

#6) Different sales methods and their revenue
'''
fig2 = px.bar(df, x='sales_method', y='revenue', color='sales_method', opacity=1,
              title='Sales Method vs Revenue', 
              labels={'revenue': 'Revenue', 'sales_method': 'Sales Method'})
fig2.show()
'''
#7) Relationship between nb_sold and revenue
'''
fig2 = px.bar(df, x='nb_sold', y='revenue', color='sales_method',
              title='Number of New Products Sold vs Revenue by Sales Method',
              labels={'nb_sold': 'Number of New Products Sold', 'revenue': 'Revenue'})
fig.show()
'''

#8) Relationship between years_as_customer and revenue
'''
fig3 = px.bar(df, x='years_as_customer', y='revenue', color='sales_method',
              title='Year as Customer vs Revenue by Sales Method',
              labels={'years_as_customer': 'Years as Customer', 'revenue': 'Revenue'})
fig3.show()
'''
##Company is established 57 years ago, but there are customers with 63 years as customer, which is not possible.

#9) Boxplot of years_as_customer
'''
fig4 = px.box(df, x='years_as_customer')
fig4.show()
'''

#10) Different sales methods and their Number of Customers
'''
Sales_Method = df['sales_method'].value_counts().reset_index().rename(
    columns={'index': 'sales_method', 'sales_method': 'Number of Sales Methods'})
Number_of_customers = df.groupby('sales_method')['customer_id'].count().reset_index().rename(
    columns={'customer_id': 'Number of Customers'})
print(Sales_Method['Number of Sales Methods'])
print(Number_of_customers['Number of Customers'])

fig5 = px.bar(df, x=Sales_Method['Number of Sales Methods'], y=Number_of_customers['Number of Customers'], color=Sales_Method['Number of Sales Methods'],
              title='Number of Customers by Sales Method')
fig5.update_layout(
    xaxis_title='Number of Sales Methods',
    yaxis_title='Number of Customers',
    legend_title='Sales Method')
fig5.show()
'''



#11) Distribution of revenue
'''
fig6 = px.histogram(df, x='revenue', nbins=50, title='Distribution of Revenue',
                     labels={'revenue': 'Revenue'})
fig6.update_layout(
    xaxis_title='Revenue',
    yaxis_title='Count',
    bargap=0.01,
    bargroupgap=0.01)
fig6.update_layout(
    xaxis=dict(
        tickmode='linear',        # show every tick at a fixed interval
        tick0=0,                  # where to start
        dtick=5                   # step size (e.g., show every 5 units)
    )
)
fig6.show()

'''

#12) boxplot of number of site visits
'''
fig7 = px.box(df, x='nb_site_visits', title='Boxplot of Number of Site Visits',
              labels={'nb_site_visits': 'Number of Site Visits'})
fig7.show()
'''
#Looks okay, no unreasonable outliers

#13) All customer ids are unique
'''
print(df['customer_id'].nunique()) 
duplicate_rows = df.duplicated()
print(f"Duplicates: {duplicate_rows.sum()}") #0
'''

#14) Week Since Product Launch vs Number of New Products Sold
'''
dfweek = df.groupby('week')['nb_sold'].sum().reset_index()
fig8 = px.line(dfweek, x='week', y='nb_sold', title='Week Since Product Launch vs Number of New Products Sold',
                labels={'week': 'Week Since Product Launch', 'nb_sold': 'Number of New Products Sold'})
fig8.show()
'''

#15) Revenue by State
'''
dfstate = df.groupby('state')['revenue'].sum().reset_index().sort_values(by='revenue', ascending=False)
fig9 = px.bar(dfstate, x='state', y='revenue', title='Revenue by State',
              labels={'state': 'State', 'revenue': 'Revenue'})
fig9.update_layout(
    width=1200,  # pixels
    height=800,
    xaxis_title='State',
    yaxis_title='Total Revenue (USD)',
    margin=dict(t=60, b=100),
)
fig9.show()
'''


fig10 = px.bar(df, x='week', y='revenue', color='sales_method', opacity=1,
              title='Sales Method vs Revenue', 
              labels={'revenue': 'Revenue', 'sales_method': 'Sales Method'})
fig10.show()
