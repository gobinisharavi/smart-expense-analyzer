import csv
from collections import defaultdict


def load_expenses(filename):
    expenses = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['Amount'] = float(row['Amount'])
            expenses.append(row)
    return expenses


def total_spending(expenses):
    return sum(e['Amount'] for e in expenses)

def spending_by_category(expenses):
    category_totals = defaultdict(float)
    for e in expenses:
        category_totals[e['Category']] += e['Amount']
    return dict(category_totals)

def top_expense(expenses):
    return max(expenses, key=lambda e: e['Amount'])

def monthly_summary(expenses):
    monthly = defaultdict(float)
    for e in expenses:
        month = e['Date'][:7]  # YYYY-MM
        monthly[month] += e['Amount']
    return dict(monthly)

def flag_high_expenses(expenses, threshold=500):
    return [e for e in expenses if e['Amount'] > threshold]


def generate_insights(expenses):
    insights = []
    by_category = spending_by_category(expenses)
    total = total_spending(expenses)

    top_cat = max(by_category, key=by_category.get)
    top_pct = (by_category[top_cat] / total) * 100
    insights.append(f"📌 '{top_cat}' is your highest spending category ({top_pct:.1f}% of total).")

    flagged = flag_high_expenses(expenses)
    if flagged:
        insights.append(f"⚠️  {len(flagged)} transaction(s) exceeded ₹500 — review for budget control.")

    monthly = monthly_summary(expenses)
    peak_month = max(monthly, key=monthly.get)
    insights.append(f"📅 Highest spending month: {peak_month} (₹{monthly[peak_month]:.2f})")

    if by_category.get('Food', 0) > total * 0.3:
        insights.append("🍔 Food expenses exceed 30% of total. Consider meal planning to reduce costs.")

    return insights


def print_report(expenses):
    print("=" * 50)
    print("       SMART EXPENSE ANALYZER REPORT")
    print("=" * 50)

    print(f"\n💰 Total Spending: ₹{total_spending(expenses):.2f}")

    print("\n📊 Spending by Category:")
    for cat, amt in sorted(spending_by_category(expenses).items(), key=lambda x: -x[1]):
        print(f"   {cat:<20} ₹{amt:.2f}")

    top = top_expense(expenses)
    print(f"\n🔺 Highest Single Expense: ₹{top['Amount']:.2f} on {top['Date']} ({top['Description']})")

    print("\n📅 Monthly Summary:")
    for month, amt in sorted(monthly_summary(expenses).items()):
        print(f"   {month}   ₹{amt:.2f}")

    print("\n🤖 AI-Generated Insights:")
    for insight in generate_insights(expenses):
        print(f"   {insight}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    expenses = load_expenses("sample_data.csv")
    print_report(expenses)
