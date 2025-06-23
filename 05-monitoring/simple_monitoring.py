import pandas as pd
import numpy as np
from datetime import datetime, date

print("🚀 Starting Simple ML Monitoring Script...")

try:
    # Load the data
    print("📂 Loading data files...")
    current_data = pd.read_parquet("green_tripdata_2024-03.parquet")
    print(f"✅ Loaded {len(current_data)} records from green_tripdata_2024-03.parquet")
    
    # Convert datetime and filter March 15-31
    print("📅 Filtering data for March 15-31, 2024...")
    current_data['lpep_pickup_datetime'] = pd.to_datetime(current_data['lpep_pickup_datetime'])
    
    start_date = date(2024, 3, 15)
    end_date = date(2024, 3, 31)
    
    filtered_data = current_data[
        current_data['lpep_pickup_datetime'].dt.date.between(start_date, end_date)
    ]
    
    print(f"✅ Filtered to {len(filtered_data)} records for monitoring period")
    
    # Calculate the metrics for Q2
    print("\n📊 Calculating Monitoring Metrics...")
    
    # Metric 1: ColumnQuantileMetric for fare_amount (quantile=0.5)
    fare_quantile_05 = filtered_data['fare_amount'].quantile(0.5)
    print(f"📈 Fare Amount Quantile 0.5 (Median): ${fare_quantile_05:.2f}")
    
    # Metric 2: ColumnMissingValuesMetric for passenger_count
    missing_passenger_count = filtered_data['passenger_count'].isnull().sum()
    total_records = len(filtered_data)
    missing_percentage = (missing_passenger_count / total_records) * 100
    
    print(f"📊 Missing passenger_count values: {missing_passenger_count} out of {total_records}")
    print(f"📊 Missing passenger_count percentage: {missing_percentage:.2f}%")
    
    # Additional useful metrics
    print("\n📋 Additional Metrics:")
    print(f"📊 Fare amount mean: ${filtered_data['fare_amount'].mean():.2f}")
    print(f"📊 Fare amount std: ${filtered_data['fare_amount'].std():.2f}")
    print(f"📊 Fare amount min: ${filtered_data['fare_amount'].min():.2f}")
    print(f"📊 Fare amount max: ${filtered_data['fare_amount'].max():.2f}")
    
    # Find the maximum quantile 0.5 value (for Q3)
    daily_metrics = []
    
    print("\n📅 Calculating daily metrics...")
    for day in pd.date_range(start_date, end_date):
        day_data = filtered_data[filtered_data['lpep_pickup_datetime'].dt.date == day.date()]
        
        if len(day_data) > 0:
            daily_quantile = day_data['fare_amount'].quantile(0.5)
            daily_metrics.append({
                'date': day.date(),
                'samples': len(day_data),
                'fare_quantile_05': daily_quantile
            })
            print(f"  {day.date()}: {len(day_data)} samples, quantile 0.5 = ${daily_quantile:.2f}")
    
    # Find maximum quantile value
    max_quantile = max([m['fare_quantile_05'] for m in daily_metrics])
    
    print("\n🎯 HOMEWORK ANSWERS:")
    print("="*50)
    print(f"Q2 Answer: ColumnQuantileMetric(fare_amount, quantile=0.5) + ColumnMissingValuesMetric(passenger_count)")
    print(f"Q3 Answer: {max_quantile:.1f} (Maximum quantile 0.5 value)")
    print("="*50)
    
    # Create a simple HTML report
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ML Monitoring Report - Simple Version</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f8f9fa; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .metric {{ background: #e3f2fd; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #2196F3; }}
            .value {{ font-size: 28px; font-weight: bold; color: #1976D2; margin: 10px 0; }}
            .answer {{ background: #e8f5e8; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #4CAF50; }}
            h1 {{ color: #333; text-align: center; }}
            h2 {{ color: #555; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f5f5f5; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 ML Monitoring Report</h1>
            <p><strong>Monitoring Period:</strong> March 15-31, 2024</p>
            <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            
            <h2>📊 Key Metrics</h2>
            
            <div class="metric">
                <h3>Fare Amount Quantile 0.5 (Median)</h3>
                <div class="value">${fare_quantile_05:.2f}</div>
                <p>This is the median fare amount across all trips in the monitoring period.</p>
            </div>
            
            <div class="metric">
                <h3>Missing Values - Passenger Count</h3>
                <div class="value">{missing_percentage:.2f}%</div>
                <p>{missing_passenger_count} missing values out of {total_records:,} total records.</p>
            </div>
            
            <div class="metric">
                <h3>Maximum Daily Quantile 0.5</h3>
                <div class="value">${max_quantile:.1f}</div>
                <p>The highest median fare amount observed on any single day.</p>
            </div>
            
            <h2>🎯 Homework Answers</h2>
            
            <div class="answer">
                <h3>Q2: Which metrics to calculate?</h3>
                <p><strong>Answer:</strong> ColumnQuantileMetric for fare_amount (quantile=0.5) + ColumnMissingValuesMetric for passenger_count</p>
            </div>
            
            <div class="answer">
                <h3>Q3: Maximum quantile 0.5 value?</h3>
                <p><strong>Answer:</strong> {max_quantile:.1f}</p>
            </div>
            
            <h2>📈 Daily Breakdown</h2>
            <table>
                <tr>
                    <th>Date</th>
                    <th>Samples</th>
                    <th>Quantile 0.5</th>
                </tr>
    """
    
    for metric in daily_metrics:
        html_content += f"""
                <tr>
                    <td>{metric['date']}</td>
                    <td>{metric['samples']:,}</td>
                    <td>${metric['fare_quantile_05']:.2f}</td>
                </tr>
        """
    
    html_content += """
            </table>
        </div>
    </body>
    </html>
    """
    
    with open("simple_monitoring_report.html", "w") as f:
        f.write(html_content)
    
    print("\n✅ Simple monitoring report saved to: simple_monitoring_report.html")
    print("🎉 Script completed successfully!")
    
except FileNotFoundError as e:
    print(f"❌ File not found: {e}")
    print("💡 Make sure you have 'green_tripdata_2024-03.parquet' in the same directory")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Check that your data file is valid and accessible")
