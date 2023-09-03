import pandas as pd

# Read the CSV file
df = pd.read_csv('documents/data_Zettel.csv')

# Extract columns containing the notions
notions_df = df[['notion 1', 'notion 2', 'notion 3', 'notion 4', 'notion 5', 'notion 6', 'notion 7', 'notion 8']]

# Convert the dataframe into a single series, drop duplicates, and sort
unique_sorted_notions = notions_df.stack().drop_duplicates().sort_values().reset_index(drop=True)

# Save to a new CSV file
unique_sorted_notions.to_csv('documents/notions.csv', index=False, header=['Notions'])
