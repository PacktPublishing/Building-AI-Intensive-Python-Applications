# pip3 install pandas==1.5.3
import pandas as pd

# Create a DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [24, 27, 22, 32, 29],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
}

df = pd.DataFrame(data)

# Display the DataFrame
print("DataFrame:")
print(df)

# Select a column
print("\nAges:")
print(df['Age'])

# Filter data
print("\nPeople older than 25:")
print(df[df['Age'] > 25])

# Calculate average age
average_age = df['Age'].mean()
print("\nAverage Age:")
print(average_age)