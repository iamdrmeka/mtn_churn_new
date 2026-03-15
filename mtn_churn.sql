-- EXPLORE DATA
SELECT * FROM mtn_churn;

--RENAME CUSTOMER ID COLUMN
ALTER TABLE mtn_churn
RENAME COLUMN `Date of Purchase` TO date_of_purchase;
-- Count number of rows
SELECT COUNT(*) FROM mtn_churn;


-- Churn rate from distinct customers
--
WITH churn_calc as (
SELECT 
    (SELECT 
         COUNT(DISTINCT customer_id)
    FROM mtn_churn
    WHERE customer_churn_status = 'YES'
    ) AS Churn,
COUNT(DISTINCT(customer_id)) as UNIQUE_CUSTOMERS 
FROM mtn_churn
)

SELECT 'Churn' as METRIC, churn as VALUE
FROM churn_calc
UNION ALL
SELECT 'Unique customers', UNIQUE_CUSTOMERS
from churn_calc
UNION ALL
SELECT 'Churn Rate', ROUND((churn * 100) / UNIQUE_CUSTOMERS,2) 
from churn_calc;

-- GEnder Analysis

--COUNT CUSTOMER BY GENDER, churn and churn rate

SELECT 
    Gender,
    Customers,
    churn,
    ROUND((100 * churn)/Customers,2) AS Churn_rate
FROM (SELECT  
    Gender,
    count(DISTINCT customer_id) as Customers,
    count(DISTINCT CASE WHEN customer_churn_status = 'yes' then customer_id END) AS Churn
FROM mtn_churn
GROUP BY Gender)T
ORDER BY Churn_rate DESC;

-- Total Revenue by Gender
select 
    gender,
    FORMAT(sum(total_revenue), 2)
    
FROM mtn_churn
group by gender;

-- Customomer Concentration by states and regions

-- Create a region column

ALTER TABLE mtn_churn
ADD region VARCHAR(20)

-- cREATE A CASE STATEMENT FOR THE DIFFERENT REGIONS

UPDATE mtn_churn
SET region =
CASE
    WHEN state IN ('Benue','Kogi','Kwara','Nasarawa','Niger','Plateau','Abuja (FCT)')
        THEN 'North Central'
    WHEN state IN ('Adamawa','Bauchi','Borno','Gombe','Taraba','Yobe')
        THEN 'North East'
    WHEN state IN ('Jigawa','Kaduna','Kano','Katsina','Kebbi','Sokoto','Zamfara')
        THEN 'North West'
    WHEN state IN ('Abia','Anambra','Ebonyi','Enugu','Imo')
        THEN 'South East'
    WHEN state IN ('Akwa Ibom','Bayelsa','Cross River','Delta','Edo','Rivers')
        THEN 'South South'
    WHEN state IN ('Ekiti','Lagos','Ogun','Ondo','Osun','Oyo')
        THEN 'South West'
END;

-- regional analysis 
-- customers by regions with churn and churn rate
SELECT 
    Region,
    Customers,
    churn,
    ROUND((100 * churn)/Customers,2) AS Churn_rate
FROM (SELECT  
    Region,
    count(DISTINCT customer_id) as Customers,
    count(DISTINCT CASE WHEN customer_churn_status = 'yes' then customer_id END) AS Churn
FROM mtn_churn
GROUP BY region)T
ORDER BY Churn_rate DESC;

-- RUN  A QUICK SCAN OF THE INIDIDUAL STATES AND THEIR CHURN RATE

SELECT 
    region,
    state,
    COUNT(DISTINCT customer_id) AS customers
FROM mtn_churn
-- where region = 'south east'
GROUP BY region, state
order by region, customers DESC
;

----Revenue Analysis
    --  total Revneue
SELECT 
    FORMAT(sum(total_revenue),2) as total_revenue
from mtn_churn;

    -- Revenue per Region

SELECT 
    Region,
    FORMAT(sum(total_revenue), 1) AS Revneue
FROM mtn_churn
group by region
order by sum(total_revenue) DESC;


    -- top 10 states BEST PERFORMING
SELECT 
    State,
    FORMAT(sum(total_revenue), 1) AS Revneue
FROM mtn_churn
group by state
order by sum(total_revenue) DESC
Limit 10;

    -- Bottom 10 states(WORSE PERFORMING STATES)
SELECT 
    State,
    FORMAT(sum(total_revenue), 1) AS Revneue
FROM mtn_churn
group by state
order by sum(total_revenue) ASC
Limit 10;

-- Revenue by mtn Device
--
--
SELECT 
    mtn_device,
    FORMAT(SUM(total_Revenue), 2) as Revenue
from mtn_churn
GROUP BY mtn_device
order by SUM(total_Revenue) DESC;

-- Revenue By Subscription plan
--
--
SELECT
    Subscription_plan,
    FORMAT(sum(total_Revenue), 2) as Revenue
FROM mtn_churn
GROUP BY subscription_plan
order by sum(total_revenue) DESC;

-- Revenue lost from churn customers

SELECT
    FORMAT(SUM(total_revenue), 2) as Revenue_lost
from mtn_churn
WHERE customer_churn_status = 'YES';

    -- REVENUE LOST PER REGION

SELECT region,
    FORMAT(SUM(total_Revenue), 2) AS Revenue_lost
FROM mtn_churn
WHERE customer_churn_status = 'YES'
GROUP BY REGION
ORDER BY sum(total_revenue) DESC;


--  top 5 perfoming customer by revenue and thier churn status

SELECT
    DISTINCT(customer_id) as Customers_ID,
    full_name,
    FORMAT(SUM(total_revenue), 2) as Revenue_from_customer,
    REGION,
    customer_churn_status
FROM mtn_churn
GROUP BY customer_id,full_name, REGION,  customer_churn_status
Order by sum(total_revenue) DESC
LIMIT 5;

select *
    from mtn_churn
where customer_id IN ('cust0405', 'CUST0085', 'CUST0494', 'CUST0365', 'UST0260');


-----REVENUE AND CUSTOMER DISTRIBUTION BY AGE plus churn rate
--
WITH age_grouping as (
    SELECT 
	CASE 
		WHEN AGE <=24 THEN  'Youths(16-24)'
		WHEN Age between 25 and 34 THEN  'Young_adults(25-34)'
		WHEN Age between 35 and 44 THEN  'Adults(35-44)'
		WHEN Age between 45 and 59 THEN  'Middle_Age(45-59)'
		WHEN Age > 59 THEN 'Seniors(60 Above)'
    END AS AGE_GROUPS,
    customer_id,
   total_Revenue AS revenue,
   customer_churn_status as churn
from mtn_churn),
 churn_data AS (
SELECT 
    age_groups,
    COUNT(DISTINCT customer_id) as Distr,
    count(DISTINCT case when lower(churn) = 'Yes' theN customer_id end) as churn,
    FORMAT(SUM(revenue), 2) as Revenue
FROM age_grouping
GROUP BY age_groups
order by SUM(revenue) DESC)
SELECT 
	Age_groups,
    Revenue,
    Distr,
    Churn,
    ROUND((100 * churn) / Distr, 2) AS Churn_rate
FROM churn_data;



-- Devices POPULARITY ACORDING TO REGIONS - PLOT WITH PYTHON
SELECT 
    REGION,
    mtn_device,
    count(*) Distr,
    sum(COUNT(*)) OVER (PARTITION BY MTN_DEVICE) TOTAL_DEVICE_POPULARITY
from mtn_churn
GROUP BY REGION, mtn_device
Order by REGION, Distr DESC;



-- sUBSCRIPTION PLANS
    -- TOP 5 purchases
SELECT
    Subscription_plan,
    COUNT(*) Purchases    
from mtn_churn
group by subscription_plan
ORDER BY PurchaseS DESC
LIMIT 5;
    -- BOTTOM 5 purchases
SELECT
    Subscription_plan,
    COUNT(*) Purchases    
from mtn_churn
group by subscription_plan
ORDER BY PurchaseS ASC
LIMIT 5;
        -- top 5 revenue generation
SELECT
    Subscription_plan,
    FORMAT(sum(total_Revenue), 2) as REVENUE
from mtn_churn
group by subscription_plan
ORDER BY sum(total_Revenue) DESC
LIMIT 5;
    -- BOTTOM 5 revenue
SELECT
    Subscription_plan,
      FORMAT(sum(total_Revenue), 2) as REVENUE  
from mtn_churn
group by subscription_plan
ORDER BY sum(total_Revenue) ASC
LIMIT 5;

--  Which plans are the top spenders buying?    
        -- top 5 plans
SELECT
    subscription_plan,
    count(*) purchases
FROM mtn_churn 
WHERE age > 45
GROUP BY subscription_plan
ORDER BY purchases DESC
LIMIT 5;

--  Which plans are the low spenders buying?    
        -- top 5 plans
SELECT
    subscription_plan,
    count(*) purchases
FROM mtn_churn 
WHERE age <= 24
GROUP BY subscription_plan
ORDER BY purchases DESC
LIMIT 5;

-- Satisfaction rate and churn

SELECT 
    customer_review,
    count(distinct case when customer_churn_status = 'yes' then customer_id end) score
FROM mtn_churn
GROUP BY customer_review
order by score;

-- Churn Reason

SELECT 
   reason_for_churn,
    count(distinct case when customer_churn_status = 'yes' then customer_id end) score
FROM mtn_churn
GROUP BY reason_for_churn
order by score;
