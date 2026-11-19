# TracePay

### Every rupee. Better understood.

TracePay is a Python-based transaction intelligence dashboard that helps users understand their spending habits by organizing transactions, visualizing expenses, and identifying patterns that may need attention.

Instead of manually reviewing a long list of transactions, users can explore their spending, search transactions, and review potentially important patterns in one place.

## Features

### 1. Overview Dashboard
- Displays total spending and income.
- Shows the total number of transactions.
- Displays transactions that may need review.
- Visualizes spending across different categories.
- Shows recent transactions.

### 2. Transaction Explorer
- Search transactions using merchant names or descriptions.
- Filter transactions by category.
- Filter transactions by Debit or Credit.
- View transaction details in an organized table.
- Download filtered transactions as a CSV file.

### 3. Smart Review
- **Possible Duplicates:** Identifies transactions with the same date, description, amount, and type.
- **Unusually Large Transactions:** Highlights debit transactions that are more than 2.5 times the median debit amount.
- **Recurring Merchants:** Identifies merchants appearing across multiple calendar months.

Smart Review helps users decide which transactions to check more closely. It does not automatically determine whether a transaction is incorrect.

## Demo Data

TracePay includes a sample transaction dataset for demonstration purposes. The sample data uses fictional transactions and dates so users can explore the dashboard, charts, categorization, and Smart Review features without uploading their own financial data.

Users can explore all dashboard features using the sample dataset or upload their own CSV file in the required format.

## How It Works

1. The user uploads a CSV file or uses the sample transactions provided in the application.
2. TracePay checks and cleans the transaction data.
3. Transactions are categorized using merchant names and predefined keywords.
4. Python calculates spending, income, and transaction patterns.
5. The results are displayed through metrics, tables, charts, and review suggestions.

## Technology Used

| Technology | Purpose |
|---|---|
| Python | Main programming language and application logic |
| Streamlit | Building the interactive dashboard |
| Pandas | Cleaning, organizing, and analyzing transaction data |
| Plotly | Creating spending visualizations |

## Transaction Categories

TracePay automatically categorizes transactions into:

- Food
- Shopping
- Transport
- Subscriptions
- Bills
- Healthcare
- Income
- Other

Categories are assigned using keywords found in the transaction description.

## CSV File Format

To upload your own transactions, the CSV file must contain the following columns:

| Column | Description |
|---|---|
| Date | Transaction date |
| Description | Merchant name or transaction description |
| Amount | Transaction amount |
| Type | Debit or Credit |

### Example

```csv
Date,Description,Amount,Type
2026-11-01,Swiggy,450,Debit
2026-11-02,Uber,280,Debit
2026-11-03,Salary,25000,Credit
2026-11-04,Netflix,649,Debit
```
## Project Repository

Source code and project documentation:

https://github.com/maitreyeephadke-tech/TracePay
