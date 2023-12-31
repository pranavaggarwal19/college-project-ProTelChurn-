# -*- coding: utf-8 -*-
"""project_backend.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MhIXlc0R1nsDbQwG5BdUTtrvJbQ6ky9Z
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from joblib import dump, load

# Load the dataset
df = pd.read_csv('telecom.csv')  # Replace 'telecom.csv' with the actual file path

# Display the first few rows of the dataset to inspect the data
df.head()

# Check for missing values in each column
print("\nMissing Values per Column:")
df.isnull().sum()

# Check data types of columns
print("\nData Types:")
df.dtypes

# Check for unique values and value counts in categorical columns
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
for col in categorical_columns:
    print(f"\nUnique values in '{col}':")
    df[col].value_counts()

# Check for outliers or unusual values in numerical columns
numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
for col in numerical_columns:
    print(f"\nSummary statistics for '{col}':")
    df[col].describe()

# Usage pattern columns to be checked
usage_columns = ['Phone Service', 'Multiple Lines', 'Internet Service', 'Internet Type', 'Avg Monthly GB Download', 'Unlimited Data']

# Convert columns to numeric types
df[usage_columns] = df[usage_columns].apply(pd.to_numeric, errors='coerce')

# Summary statistics for usage pattern columns
df[usage_columns].describe()

# Box plots to visualize outliers
plt.figure(figsize=(10, 6))
df[usage_columns].boxplot()
plt.title('Boxplot of Usage Pattern Fields')
plt.ylabel('Count')
plt.xlabel('Usage Pattern Fields')
plt.xticks(rotation=45)
plt.show()

# Check for any negative values or unreasonable counts
for col in usage_columns:
    negative_values = (df[col] < 0).sum()
    print(f"Negative values in '{col}': {negative_values}")

    # Check for extremely high values (potential outliers)
    extreme_values = (df[col] > df[col].quantile(0.95)).sum()  # Considering top 5% as potential outliers
    print(f"Count of potential outliers in '{col}': {extreme_values}")

# Display the first few rows of the dataset
print("\nSummary Statistics:")
df.describe()

# Check for missing values
print("\nMissing Values per Column:")
df.isnull().sum()

# Check data types of columns
print("\nData Types:")
df.dtypes

# Correlation heatmap for numerical columns
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

# Distribution of usage pattern columns
plt.figure(figsize=(12, 8))
num_cols = len(usage_columns)
for i, col in enumerate(usage_columns, 1):
    plt.subplot((num_cols // 2) + (num_cols % 2), 2, i)
    sns.histplot(df[col], kde=True)
    plt.title(f'Distribution of {col}')
plt.tight_layout()
plt.show()

# Assume 'Churn' is the target variable
X = df.drop('Customer Status', axis=1)  # Features
y = df['Customer Status']  # Target variable

# Additional features 'Churn Category' and 'Churn Reason'
additional_features = ['Churn Category', 'Churn Reason']

# Include additional features in the dataset for further analysis or interpretation
X_additional = df[additional_features]

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Separate numerical and categorical columns
numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

# Preprocessing for numerical features: Scaling with imputation of missing values
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# Preprocessing for categorical features: One-hot encoding with imputation of missing values
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine preprocessing for numerical and categorical features
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LogisticRegression(random_state=42, max_iter=1000))])

# Fit the model
clf.fit(X_train, y_train)

y_train_pred = clf.predict(X_train)

# Evaluate model performance on the training data
train_accuracy = accuracy_score(y_train, y_train_pred)
print(f"Accuracy on training data: {train_accuracy:.2f}")

# Print classification report and confusion matrix for training data
print("\nClassification Report (Training Data):")
print(classification_report(y_train, y_train_pred))

print("\nConfusion Matrix (Training Data):")
print(confusion_matrix(y_train, y_train_pred))

# Further analysis or interpretation using 'Churn Category' and 'Churn Reason'
# Example: Display unique values or perform additional analysis
print("\nUnique values in Churn Category:")
print(X_additional['Churn Category'].unique())

print("\nUnique values in Churn Reason:")
print(X_additional['Churn Reason'].unique())

# Save the trained model
dump(clf, 'saved_model.pkl')

# Load the saved model
saved_model = 'saved_model.pkl'  # Replace 'saved_model.pkl' with the path to your saved model
model = load(saved_model)  # Load the saved model

# Predict on the test set
y_pred = clf.predict(X_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Print classification report and confusion matrix
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))