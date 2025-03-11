import pandas as pd

# Read the Excel file
df = pd.read_excel('finalFinancialLiteracyAppDatabaseCredit.xlsx', engine='openpyxl')

# Convert to pipe-delimited CSV
df.to_csv('finalFinancialLiteracyAppDatabaseCredit.csv', sep='|', index=False)

df = pd.read_excel('finalFinancialLiteracyAppDatabaseLoans.xlsx', engine='openpyxl')

# Convert to pipe-delimited CSV
df.to_csv('finalFinancialLiteracyAppDatabaseLoans.csv', sep='|', index=False)