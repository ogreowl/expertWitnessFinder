import pandas as pd

# Load the CSV file that was previously generated
df = pd.read_csv('experts.csv')

# Add a new column called 'modifier' and set all values to 1
df['modifier'] = 1

# Save the updated DataFrame to a new CSV file
df.to_csv('with_modifier.csv', index=False)

print("Modifier column added and saved to 'experts_with_modifier.csv'.")