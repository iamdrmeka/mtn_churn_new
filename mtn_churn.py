import pandas as pd
import matplotlib.pyplot as plt

# import dataset, preview and clean
df = pd.read_csv(r'mtn_churn.csv')
df.columns = df.columns.str.replace(' ', '_').str.lower()
print(df.sample(3))

# remove spaces and implement lower cases on all columns
for cols in df.select_dtypes(include='object'):
    df[cols] = df[cols].str.strip().str.lower()
print(df.sample(5))

# COUNT DISTINCT CUSTOMERS
df['customer_id'].nunique()

# COunt churn Volume
churn = df.groupby('customer_churn_status')[
    'customer_id'].nunique().reset_index(name='count')
churn.columns = ['churn status', 'Count']
print(churn)

# Plot for churn volume
plt.bar(churn['churn status'], churn['Count'], color=["darkgreen", "red"])
plt.xticks([1, 0], ["Churned Customers", "Active Customers"])
plt.title('Customer churn')
plt.show()

# Get churn rate
summary = df.groupby("customer_churn_status")["customer_id"].nunique()

churn_rate = 100 * summary["yes"] / summary.sum()
print(f'Churn Rate: {churn_rate:,.2f}')

# Proper table of Customer churn details
unique_customers = df['customer_id'].nunique()
churn_customers = df.loc[df['customer_churn_status']
                         == 'yes', 'customer_id'] .nunique()
overall_churn_rate = round((100 * churn_customers / unique_customers), 2)
active_customers = unique_customers - churn_customers

churn_table = pd.DataFrame({
    'Details': ["unique_customers", "active_customers", "churned_customers", "overall_churn_rate"],
    'Count':   [unique_customers, active_customers, churn_customers, overall_churn_rate]
})

print(churn_table)

# Plot for active customers and churned customers
plt.bar(churn_table.loc[1:2, 'Details'],
        churn_table.loc[1:2, 'Count'], color=['black', 'grey'])
plt.xticks([1, 0], ['Active Customers', 'Churned Customers'])
plt.show()

# churn by gender
genders = df.groupby('gender')[
    'customer_id'].nunique().reset_index(name='count')
print(genders)
# Plot for gender churn
plt.bar(genders['gender'], genders['count'], color=['blue', 'pink'])
plt.title('Gender Distribution')
plt.show()

# Proper Gender churn table
customers = df.groupby('gender')['customer_id'].nunique()
churned_customers = (df[df['customer_churn_status'] == 'yes']
                     .groupby('gender')['customer_id'].nunique())
churn_gender = pd.concat([customers, churned_customers], axis=1)
churn_gender.columns = ['customers', 'churned']
churn_rate = round((100 * churned_customers/customers), 2)
churn_gender['churn_rate'] = churn_rate
churn_gender.reset_index(inplace=True)
churn_gender

# Add Region to the  Table so we can analyse by regions
region_map = {
    'Benue': 'North Central', 'Kogi': 'North Central', 'Kwara': 'North Central',
    'Nasarawa': 'North Central', 'Niger': 'North Central', 'Plateau': 'North Central', 'Abuja (FCT)': 'North Central',

    'Adamawa': 'North East', 'Bauchi': 'North East', 'Borno': 'North East',
    'Gombe': 'North East', 'Taraba': 'North East', 'Yobe': 'North East',

    'Jigawa': 'North West', 'Kaduna': 'North West', 'Kano': 'North West',
    'Katsina': 'North West', 'Kebbi': 'North West', 'Sokoto': 'North West', 'Zamfara': 'North West',

    'Abia': 'South East', 'Anambra': 'South East', 'Ebonyi': 'South East',
    'Enugu': 'South East', 'Imo': 'South East',

    'Akwa Ibom': 'South South', 'Bayelsa': 'South South', 'Cross River': 'South South',
    'Delta': 'South South', 'Edo': 'South South', 'Rivers': 'South South',

    'Ekiti': 'South West', 'Lagos': 'South West', 'Ogun': 'South West',
    'Ondo': 'South West', 'Osun': 'South West', 'Oyo': 'South West'
}

df['region'] = df['state'].map(region_map)


# Regional analysis
regions = df.groupby('region')['customer_id'].nunique()
churn_regions = df[df['customer_churn_status'] == 'yes'].groupby('region')[
    'customer_id'].nunique()
region_churn = pd.concat([regions, churn_regions], axis=1)
region_churn.columns = ['Total Customers', 'Churned Customers']
region_churn['churn_rate'] = round((100 * churn_regions)/regions)
region_churn.reset_index(inplace=True)
rccp = region_churn.sort_values(
    by='Total Customers', ascending=False)  # Region Churn Customer Plot
# Region Churn Customer Plot
rcp = region_churn.sort_values(by='churn_rate', ascending=False)
print(region_churn)
# plot
plt.bar(rccp['region'], rccp['Total Customers'], color=['black'])
plt.title("customers by Regions")
plt.xticks(rotation=55)
plt.show()
# Plot for churn
plt.bar(rcp['region'], rcp['churn_rate'], color=['black'])
plt.title("customer churn - Regoin")
plt.xticks(rotation=55)
plt.show()

# Revenue by region
Total_revenue = df.groupby('region')['total_revenue'].sum(
).reset_index().sort_values(by='total_revenue', ascending=False)
Total_revenue['total_revenue'] = Total_revenue['total_revenue'].apply(
    lambda x: f'{x:,.2f}')
print(Total_revenue)

# TOP 10 performing states
perfomance = df.groupby(['state', 'region'])['total_revenue'].sum(
).reset_index().sort_values('total_revenue', ascending=False)
perfomance['total_revenue'] = perfomance['total_revenue'].apply(
    lambda x: f'{x:,.2f}')

top = perfomance.head(10).reset_index(drop=True)
bottom = perfomance.tail(10).reset_index(drop=True)
top_and_bottom = pd.concat([top, bottom], axis=1, keys=['Top 10', 'Bottom 10'])
top_and_bottom

# create an age group column
df['age_group'] = pd.cut(
    df['age'],
    bins=[1, 24, 34, 44, 59, 100],
    labels=[
        'Youths(16-24)',
        'Young_adults(25-34)',
        'Adults(35-44)',
        'Middle_Age(45-59)',
        'Seniors(60 Above)'
    ]
)
# analyse age groups
age_groups_revenue = df.groupby('age_group')['total_revenue'].sum()
age_group_distr = df.groupby('age_group')['customer_id'].nunique()
age_group_churn = df[df['customer_churn_status'] == 'yes'].groupby('age_group')[
    'customer_id'].nunique()
age_grp_report = pd.concat(
    [age_groups_revenue, age_group_distr, age_group_churn], axis=1)
age_grp_report.columns = ['Revenue', 'Customer Distr', 'Churn']
age_grp_report['churn Rate'] = round(
    (100 * age_group_churn / age_group_distr), 2)
age_grp_report.sort_values(by='Revenue', ascending=False, inplace=True)
age_grp_report.reset_index(inplace=True)
plt.bar(age_grp_report['age_group'],
        age_grp_report['Revenue'], color=['black', 'grey'])
plt.xticks(rotation=75)
plt.title("Revenue by age groups")
age_grp_report['Revenue'] = age_grp_report['Revenue'].apply(
    lambda x: f'{x:,.2f}')
display(age_grp_report)
plt.show()
# plot
plt.bar(age_grp_report['age_group'],
        age_grp_report['Customer Distr'], color=['black', 'grey'])
plt.xticks(rotation=75)
plt.title("customer Distribution by age groups")
plt.show()
# plot
plt.bar(age_grp_report['age_group'],
        age_grp_report['churn Rate'], color=['black', 'grey'])
plt.title("Churn Rate by age Groups")
plt.xticks(rotation=75)
plt.show()
# revenue by MTN DEVICE

mtn_Device = df.groupby('mtn_device')['total_revenue'].sum(
).reset_index().sort_values(by='total_revenue', ascending=False)
plt.bar(mtn_Device['mtn_device'], mtn_Device['total_revenue'], color='black')
plt.xticks(rotation=70)
mtn_Device['total_revenue'] = mtn_Device['total_revenue'].apply(
    lambda x: f'{x:,.2f}')
mtn_Device
# Count device usage
mtn_Device_count = df.groupby('mtn_device')['customer_id'].count(
).reset_index().sort_values(by='customer_id', ascending=False)
display(mtn_Device_count)
plt.bar(mtn_Device_count['mtn_device'],
        mtn_Device_count['customer_id'], color='black')
plt.xticks(rotation=70)
plt.show()
# device popularity by regions
df.pivot_table(
    values='customer_id',
    index='region',
    columns=['mtn_device'],
    aggfunc='count')
# count subs
subs_count = df.groupby('subscription_plan')['customer_id'].count(
).reset_index().sort_values(by='customer_id', ascending=False)
plt.barh(subs_count['subscription_plan'],
         subs_count['customer_id'], color='darkgoldenrod')
plt.show()
display(subs_count.head(5))  # top 5
display(subs_count.tail(5))  # bottom 5
# Subcription plans by revenue
subs = df.groupby('subscription_plan')['total_revenue'].sum(
).reset_index().sort_values(by='total_revenue', ascending=False)
plt.barh(subs['subscription_plan'],
         subs['total_revenue'], color='darkgoldenrod')
subs['total_revenue'] = subs['total_revenue'].apply(lambda x: f'{x:,.2f}')
display(subs.head(5))
display(subs.tail(5))
# which plans are the top spenders buying?
top_subs = df[df['age'] > 45].groupby('subscription_plan')['customer_id'].count(
).reset_index().sort_values(by='customer_id', ascending=False).head(5)
top_subs.columns = ['Subs', 'Purchase']
display(top_subs)
# which plans are the top spenders buying?
botttom_subs = df[df['age'] < 25].groupby('subscription_plan')['customer_id'].count(
).reset_index().sort_values(by='customer_id', ascending=False).head(5)
botttom_subs.columns = ['Subs', 'Purchase']
display(botttom_subs)
# customer review
review = df[df['customer_churn_status'] == 'yes'].groupby(['customer_review', 'satisfaction_rate'])[
    'customer_id'].nunique().reset_index().sort_values(by='satisfaction_rate')
review.columns = ['Review', 'Satisfaction Score', 'Churn']
display(review)
# churn reason
churn_reason = df[df['customer_churn_status'] == 'yes'].groupby(['reasons_for_churn'])[
    'customer_id'].nunique().reset_index().sort_values(by='customer_id', ascending=False)
churn_reason.columns = ['Reason', 'Churn']
display(churn_reason)
