
# Module 5: Monitoring - Homework

The goal of this homework is to familiarize users with monitoring for ML batch services, using PostgreSQL database to store metrics and Grafana to visualize them.

---

### ✅ Q1. Prepare the dataset

Start with `baseline_model_nyc_taxi_data.ipynb`. Download the **March 2024 Green Taxi** data.  
We will use this data to simulate a production usage of a taxi trip duration prediction service.

> **What is the shape of the downloaded data? How many rows are there?**

✅ **Answer:**  
**72044**

---

### ✅ Q2. Metric

Let’s expand the number of data quality metrics we’d like to monitor!  
Please add **one metric of your choice** and a **quantile value for the `fare_amount` column** (`quantile=0.5`).

> **What metric did you choose?**

✅ **Answer:**  
- `ColumnQuantileMetric(column_name='fare_amount', quantile=0.5)`  
- `DatasetCorrelationsMetric()`

The `ColumnQuantileMetric` helps monitor the **median fare amount**, while the `DatasetCorrelationsMetric` tracks the **correlation structure** between features, which is useful for spotting unusual shifts in relationships across variables.

---

### ✅ Q3. Monitoring

Let’s start monitoring. Run expanded monitoring for a new batch of data (**March 2024**).

> **What is the maximum value of metric quantile = 0.5 on the `fare_amount` column during March 2024 (calculated daily)?**

✅ **Answer:**  
**14.8**

---

### ✅ Q4. Dashboard

Finally, let’s add panels with new added metrics to the dashboard.  
After we customize the dashboard let's save a dashboard config, so that we can access it later.

> **Where to place a dashboard config file?**

✅ **Answer:**  
**project_folder/dashboards (05-monitoring/dashboards)**

