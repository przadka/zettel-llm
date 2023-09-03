import pandas as pd

# Load the CSV file
df = pd.read_csv('documents/data_Zettel.csv')

# Shuffle the dataframe
df = df.sample(frac=1).reset_index(drop=True)

# Calculate the split index based on the 200:1 ratio
split_index = int(df.shape[0] * (200 / 201))

# Split the dataframe
train_df = df[:split_index]
test_df = df[split_index:]

# Save training and test dataframes to separate CSV files
train_df.to_csv('documents/train_data.csv', index=False)
test_df.to_csv('documents/test_data.csv', index=False)
