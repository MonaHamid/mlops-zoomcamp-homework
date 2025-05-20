✨ MLOps Zoomcamp Homework – Week 1 & 2 Recap
🚀 Finished Week 1 & Week 2 of the MLOps Zoomcamp — and here’s what I’ve learned and built so far:

📦 Week 1: Project Structure + Linear Regression on NYC Yellow Taxi Data
🔧 Setup & Tools
Got hands-on with GitHub Codespaces — like VS Code but in the cloud 💻☁️

Learned how to structure a proper ML project with reusable scripts instead of tangled notebooks

Installed dependencies, created .venv, and used make commands for automation

🛻 Dataset: NYC Yellow Cab Trips (Jan–Feb 2023)
Downloaded January & February 2023 Parquet trip data

Conducted basic EDA and noticed some extreme trip durations ⏱️

Filtered the data to include only reasonable trips (1 to 60 minutes)

🧠 Feature Engineering
Computed duration from timestamps and converted to minutes

Applied one-hot encoding to PULocationID and DOLocationID

Used DictVectorizer to transform categorical features

📈 Modeling
Trained a baseline Linear Regression model

Achieved:

🟢 Train RMSE: ~7.64

🔵 Validation RMSE: ~7.81

Logged model performance and serialized the vectorizer + model

⚙️ Week 2: MLflow Experiment Tracking + Hyperparameter Tuning
🧪 MLflow Autologging
Integrated MLflow autologging with train.py

Tracked parameters, metrics, artifacts, and model structure all from code!

🔍 Hyperparameter Optimization
Tuned RandomForestRegressor with Hyperopt

Defined a search_space for depth, n_estimators, etc.

Logged top n runs and evaluated them

🏁 Model Registry
Promoted the best model to the MLflow Model Registry

Validated the model on March 2023 test data — best test RMSE: 5.59

Registered model: nyc-taxi-rf-model

💡 Key Takeaways
✅ Structure matters — reusable code and clear folders saved tons of time
✅ Outliers skew everything — especially for linear models
✅ MLflow autologging is powerful — no more tracking metrics manually
✅ Experiment tracking + registry = MLOps foundation
