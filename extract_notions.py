import pandas as pd

# Read the CSV file
df = pd.read_csv('documents/data_Zettel.csv')

# Extract columns containing the notions
notions_df = df[['notion_1', 'notion_2', 'notion_3', 'notion_4', 'notion_5', 'notion_6', 'notion_7', 'notion_8']]

# Convert the dataframe into a single series, drop duplicates, and sort
unique_sorted_notions = notions_df.stack().drop_duplicates().sort_values().reset_index(drop=True)

# Save to a new CSV file
unique_sorted_notions.to_csv('documents/notions.csv', index=False, header=['Notions'])
