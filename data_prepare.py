import pandas as pd

# Step 1: Load your dataset (the one you generated)
df = pd.read_csv("website_dataset.csv")

# Step 2: Fix inconsistent labels
df['label'] = df['score'].apply(lambda s: 0 if s > 50 else 1)

# Step 3: (Optional) Check how many scam vs legit
print(df['label'].value_counts())

# Step 4: Save the fixed dataset
df.to_csv("dataset_fixed.csv", index=False)

print("✅ Dataset labels fixed and saved as dataset_fixed.csv")
