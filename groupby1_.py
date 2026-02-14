import pandas as pd
df=pd.read_csv("ecomerece_transaction.csv")

df["revenue"]=df["price"]*df["quantity"]

df["order_date"]=pd.to_datetime(df["order_date"])

df["order_hour"]=df["order_hour"].astype(int)
df["order_date1"]=df["order_date"]+pd.to_timedelta(df["order_hour"],unit='h')

df=df.set_index("order_date1")
df.sort_index(inplace=True)

#1
daily_revenue=df.resample("D")["revenue"].sum().fillna(0)

#2
month_revenue=df.resample("M")["revenue"].pct_change().fillna(0)
#3
last7=df.rolling('7D')["revenue"].mean()
last30=df.rolling('30D')["revenue"].mean()

#4
last4=df["order_id"].rolling('4H').count()

total_revenue=df.groupby("customer_id")["revenue"].sum()

#5
cumulative_revenue=df["revenue"].expanding().sum()

cumulative_order=df["order_id"].expanding().count()

#6 
cumulative_failure_rate=(
    (df["order_status"]=='Failed').astype(int)
                    .expanding().
                    mean()*100).fillna(0)


alert=cumulative_failure_rate.apply(lambda x: 'Alert' if x>25 else "Normal") 

#7
category_month=(
    df.groupby("category").
                resample('M')['revenue'].sum()
                .groupby('category')
                .rolling(3)
                .mean()
                .reset_index(level=0,drop=True)
                .fillna(0)
                )

#8
cumulative_spend=(
    df.groupby('customer_id')['revenue'].
                  expanding().
                  sum().
                  reset_index()
        )

last_7_spend=(df.groupby('customer_id')['revenue']
              .rolling('7D')
              .sum()
              .reset_index()
              )

#9

b=df.groupby('customer_id')['revenue'].expanding().mean().reset_index(level=0,drop=True).sum()

suspicious_act= (last4>=2) & (df["revenue"].sum()>2*b)

#10

aaa=(df['order_status']=='Failed').astype(int)
daily_failure_rate=aaa.resample('D').mean()*100


rolling_failure_rate=aaa.rolling('7D').mean()*100
rolling_failure_alert=rolling_failure_rate.apply(lambda c: "Alert" if c>30 else "Normal")

print(suspicious_act)

# BONUS'

daily_revenue1=df.groupby(pd.Grouper(key="order_date",freq='D'))["revenue"].sum()
#daily_revenue and daily_revenue1 same hai check kar lena 

# roliing- this function is use to find previous n calculation , for example find the average of last 4 month 
# expanding-this function is used where we want start to end operations , for example how much customer are joined from start to end
    
#  why resample better - because it is short as compare to pd.Grouper and there is a condition the index should be datetime format   