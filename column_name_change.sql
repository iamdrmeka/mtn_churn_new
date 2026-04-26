
ALTER TABLE mtn_churn
RENAME COLUMN `customer tenure in months` TO customer_tenure_months;

ALTER TABLE mtn_churn
RENAME COLUMN `subscription plan` TO subscription_plan;

ALTER TABLE mtn_churn
RENAME COLUMN `unit price` TO unit_price;

ALTER TABLE mtn_churn
RENAME COLUMN `Number of times purchased` TO unit_price;
ALTER TABLE mtn_churn
RENAME COLUMN `Total Revenue` TO total_revenue;

ALTER TABLE mtn_churn
RENAME COLUMN `data usage` TO data_usage;

ALTER TABLE mtn_churn
RENAME COLUMN `customer churn status` TO customer_churn_status;

ALTER TABLE mtn_churn
RENAME COLUMN `reasons for churn` TO reason_for_churn;

ALTER TABLE mtn_churn
RENAME COLUMN `full name` TO full_name;