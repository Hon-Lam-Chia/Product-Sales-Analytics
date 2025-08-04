import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import datetime
import plotly.graph_objects as go
from plotly.graph_objects import Figure
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
color = {'Email':'red', 'Call':'blue', 'Email + Call': 'green'}

# 1) Number of Customers per Sales Method
cus = df.groupby('sales_method')['customer_id'].count().reset_index()
cus = pd.DataFrame(cus)

fig1 = px.bar(cus, x="sales_method", y="customer_id", title = 'Number of Customers per Sales Method', labels={'sales_method': 'Sales Method', 'customer_id': 'Number of Customers'}, color = 'sales_method', color_discrete_map=color)
#fig1.show()

# 2) Spread of Revenue (Overall and by Method)
fig2 = px.box(df, x="revenue", title="Spread of Revenue (Overall)")
#fig2.show()
fig3 = px.box(df, x="revenue", y="sales_method", color="sales_method", title="Spread of Revenue (By Method)", color_discrete_map=color)
#fig3.show()

# 3) Revenue Over Time by Method

revenue_weekly = df.groupby(['week', 'sales_method'])['revenue'].sum().reset_index()

fig4 = px.line(revenue_weekly, x='week', y='revenue', color='sales_method',
              title='Revenue Over Time by Sales Method',
              labels={'week': 'Week Since Launch', 'revenue': 'Total Revenue'}, color_discrete_map=color)
fig4.update_traces(mode='lines+markers')
#fig4.show()

# 4) Sales Volumn Over Time by Method
sales_weekly = df.groupby(['week', 'sales_method'])['nb_sold'].sum().reset_index()

fig5 = px.line(sales_weekly, x='week', y='nb_sold', color='sales_method', color_discrete_map=color,
              title='Sales Volumn Over Time by Sales Method',
              labels={'week': 'Week Since Launch', 'nb_sold': 'Sales Volumn'})
fig5.update_traces(mode='lines+markers')
#fig5.show()

# 5) Customer Profile Comparison
# Number of Site Visits by Sales Method
fig6 = px.box(df, x="nb_site_visits", y="sales_method", color="sales_method", title="Number of Site Visits(By Method)", color_discrete_map=color)
#fig6.show()


#Number of Customers by State
NoCus = df['state'].value_counts()

fig7 = px.bar(NoCus, x=NoCus.index, y=NoCus.values, title="Number of Customers by State", width=1600, labels={"state": "State", "y":"Number of Customers"})
#fig7.show()

summary = df.groupby('sales_method').agg(
    total_customers=('customer_id', 'nunique'),
    total_revenue=('revenue', 'sum'),
    avg_revenue_per_customer=('revenue', lambda x: x.sum() / x.nunique()),
    avg_site_visits=('nb_site_visits', 'mean'),
    avg_years_as_customer=('years_as_customer', 'mean'),
    total_products_sold=('nb_sold', 'sum')
).round(2)

summary = summary.sort_values(by='total_revenue', ascending=False)
print(summary)

# ✅ Use summary instead of df in table cells
fig = go.Figure(data=[go.Table(
    header=dict(values=['Sales Method'] + list(summary.columns)),
    cells=dict(values=[[i for i in summary.index]] + [summary[col].tolist() for col in summary.columns])
)])
fig.show()
