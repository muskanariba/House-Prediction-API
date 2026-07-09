import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

data = pd.read_csv("house_data.csv")

print(data.head())

# Features (Input)
X = data[["Area"]]

# Target (Output)
y = data["Price"]

# Create model
model = LinearRegression()

# Train model
model.fit(X, y)


# Test the model
sample_area = [[1500]]
predicted_price = model.predict(sample_area)

print(f"\nPredicted price for 1500 sq ft: {predicted_price[0]:.2f}")

# Save model
joblib.dump(model, "model.pkl")
