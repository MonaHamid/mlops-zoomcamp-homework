# mlops-zoomcamp-homework

inished Week 1 of the MLOps Zoomcamp!

Here’s a quick recap of what I learned and built so far:

🔧 Setup & Tools

Tried out GitHub Codespaces (it felt like VS Code in the cloud – pretty cool once I figured it out 😅)

Learned how to structure a proper ML project — folders, scripts, data… not just a bunch of notebooks anymore!

🛻 NYC Taxi Dataset (Yellow Cabs)

Downloaded January & February 2023 trip data

Did basic EDA and noticed some long-duration outliers 🧐

Filtered the data to keep trips between 1 and 60 mins

🧠 Feature Engineering

Computed trip duration in minutes

One-hot encoded pickup and dropoff locations

Turned the data into a dictionary-based feature matrix

📈 Modeling

Trained a baseline Linear Regression model

Got an RMSE of 7.64 on train, and 7.81 on validation

Learned that even basic models can perform decently if your features are clean

💡 What clicked for me

The way you structure your project makes it way easier to debug and scale later

Outliers really mess with your model, even in a simple regression

One-hot encoding + DictVectorizer = magic when working with categorical IDs

📌 Next up: model packaging, experiment tracking, and deployment — can’t wait to break things and learn more 🔥
