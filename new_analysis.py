import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
from PIL import Image
import numpy as np

import seaborn as sns
sns.set()
import mysql.connector as connection
    
GOsales = connection.connect(host="relational.fit.cvut.cz", database='GOSales', user="guest", passwd="relational", use_pure=True)

IMG = Image.open("GettyImages-879652108-72f1349e0fd342e6927a8b40d16dff2a.jpg")
st.image(IMG)

go_product = pd.read_sql_query("SELECT gr.`Retailer name`, gr.`Country`, gds.`Retailer code`, gds.`Product number`, gds.`Date`, gds.`Quantity`, \
                                 gp.`Product line`, gp.`Product brand`, gp.`Product type`, gp.`Unit cost`, \
                                 gp.`Unit price`, gp.`Product` \
                                 FROM go_retailers as gr \
                                 RIGHT JOIN go_daily_sales as gds \
                                 ON gr.`Retailer code` = gds.`Retailer code` \
                                 RIGHT JOIN go_products as gp \
                                 ON gds.`Product number` = gp.`Product number`", GOsales)


st.sidebar.title("Filter")
product_status = st.sidebar.selectbox('Select Product Line ', go_product['Product line'].unique())

filtered_df = go_product[(go_product['Product line'] == product_status)]
st.title('Live Visualisation Of Chart')
st.write(filtered_df)


filtered_df["Year"] = pd.to_datetime(filtered_df["Date"], format="%Y-%m-%d").dt.year

fig, (ax1, ax2, ax3,ax4) = plt.subplots(nrows=4, ncols=1, figsize=(16, 35), facecolor = '#beeffa')
ax1.bar(filtered_df['Year'], filtered_df['Quantity'], edgecolor = '#B2BEB5', color = '#CAA472', hatch='|*', width = 0.3)
ax1.set_xlabel('Date',fontsize = 20, c ='black') #labeling of our chart x and y label
ax1.set_ylabel('Quantity Sold',fontsize = 20, c= 'black')
ax1.set_title('Quantity Sold Over Time ', fontsize = 20, color ='black')



colors = np.random.rand(len(filtered_df))


ax2.scatter(filtered_df['Unit cost'], filtered_df['Unit price'], alpha=0.5, c=colors, s=30, label='Unit price')
ax2.set_title('has changed over time')
ax2.set_xlabel('Unit cost')
ax2.set_ylabel('Unit price')

ax2.legend()
plt.show()


counts = Counter(filtered_df['Product type'])
counts_dict = dict(counts)

ax3.pie(counts_dict.values(), labels = counts_dict.keys(), autopct='%1.2f%%', hatch ='*', startangle=90, shadow=True)
ax3.axis('equal')
ax3.legend(facecolor = 'm', fontsize = 15,)
ax3.legend(loc='upper right')
ax3.set_title('Percentage of Product Type Sold')


plt.grid()


ax4.barh(filtered_df['Product'], filtered_df['Quantity'], label=filtered_df['Product'])
ax4.set_title('product and Quantity sold')
ax4.set_xlabel('Quantity sold')
ax4.set_ylabel('Products')
plt.grid()

st.pyplot(fig)
