import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns


df= pd.read_csv('./asset/dataset.csv')
fig, ax = plt.subplots()
sns.histplot(x=df.price,ax=ax)
ax.set_xlim(0.0,1000.0) #specify the range since tons of data
plt.show()

#Clean Data by dropping duplicate
df=df.drop_duplicates().reset_index()

#Auquire data from string
str_time_stlip=df.event_time.str.split(' ', expand=True)
df['time_hours']=pd.to_numeric(str_time_stlip.get(1).str[0:2])

#Datetime datatype for weekday() function
df['weekday']=str_time_stlip.get(0)
df['year']=str_time_stlip.get(0).str[0:4]
pd.to_datetime(df['weekday'], format='%Y-%m-%d')
df['weekday']=df.weekday.apply(lambda x: datetime.strptime(x,'%Y-%m-%d').weekday())

#Top 5 sales volume in brands
#Only drop null in 'Brand' column
df_for_top5_brand=df.dropna(subset=['brand'])
top5_brands=df_for_top5_brand.groupby('brand').order_id.count().reset_index().sort_values('order_id', ascending=False).head(5)
top5_brands=top5_brands.rename(columns={'order_id':'number_of_sales'}).reset_index()
plt.plot(top5_brands.brand, top5_brands.number_of_sales)
plt.show()

#1st sales in category
#Only drop null in 'category_code' and 'price column
df_for_category=df.dropna(subset=['category_code','price'])
top_sales_in_category=df_for_category.groupby('category_code').price.mean().reset_index().sort_values('price',ascending=False)
top_sales_in_category.reset_index(inplace=True)
the_highest_avg_price=top_sales_in_category.head(1)
print(the_highest_avg_price)


#data below 20 currency units
drop_df=df.dropna(subset=['category_code','price','brand'])
df_price_under_20=drop_df[drop_df.price<20.0]
#check the mean price for each brand and category
mean_price_groupby_brand_and_category=df_price_under_20.groupby(['brand', 'category_code']).price.mean().reset_index()
#groupby category and brands for sales volumes
sales_groupby_brand_and_category=df_price_under_20.groupby(['brand', 'category_code']).order_id.count().reset_index()
#most sales in brand and category under 20 currency units
sales_groupby_brand_and_category['avg_price']=mean_price_groupby_brand_and_category.price
brand_and_category_sorted=sales_groupby_brand_and_category.reset_index().sort_values('order_id',ascending=False)
brand_and_category_sorted.reset_index(inplace=True)
print(brand_and_category_sorted.head(1))

#Distribution of weekdays based on time_hours
weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
for i in range(7):
    sns.displot(data=df, x=df.time_hours[df.weekday==i], binwidth=1).set(title=weekDays[i])
    plt.show()

#Total cost of sales volumes in a specific year
def calculate_category_sales_in_year(X, Y):
    category_code = str(X)
    year = str(Y)
    if (category_code in df_for_category.category_code.unique()) & (year in df_for_category.year.unique()):
        category_sales_in_year = df_for_category.groupby(['category_code', 'year']).order_id.count().reset_index()
        data = category_sales_in_year[(category_sales_in_year.category_code == category_code) & (
                    category_sales_in_year.year == year)].reset_index()
        price = df_for_category[(df_for_category.category_code == category_code) & (df_for_category.year == year)].price
        if (len(price), data.order_id):
            print('In {}, the total cost of {} is {}'.format(year, category_code, price.sum()))
        else:
            print('Length of "price" and "sales volumes" is different')

    else:
        print('Either category_code or year do not exist in data')

df_for_prob=df_for_top5_brand.dropna(subset=['price'])
def prob_brand_to_currency(X, Y):
    brand = str(X)
    currency = float(Y)
    max_currency = df_for_prob.price.max()
    min_currency = df_for_prob.price.min()
    #Brand needs to be in DataFrame and The currency needs to be with in the range
    if (brand in df_for_prob.brand.unique()) & (currency <= max_currency) & (currency >= min_currency):
        total_sales_volumes_intotal = df_for_prob.groupby('brand').order_id.count().reset_index()
        total = total_sales_volumes_intotal[total_sales_volumes_intotal.brand == X].order_id
        totals_sales_volumes_more_than_Y = df_for_prob[df_for_prob.price > Y].groupby('brand').order_id.count().reset_index()
        #Maybe the brand does not sell anything above the currency
        if (brand in totals_sales_volumes_more_than_Y.brand.unique()):
            purchased_item = totals_sales_volumes_more_than_Y[totals_sales_volumes_more_than_Y.brand == X].order_id
            print('The total order is {}, and the order above {} is {} for {}. The probability is {}.'.format(
                total.iloc[0], currency, purchased_item.iloc[0], brand, purchased_item.iloc[0] / total.iloc[0]))
        else:
            print('The input brand does not have any sales above the input currency')

    else:
        print('The input Brand is not in DataFrame, or the input currency is out of the range')
