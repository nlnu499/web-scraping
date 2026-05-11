import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue"

headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")


tables = soup.find_all("table", class_="wikitable")


table = tables[0]

rows = table.find_all("tr")

data = []

for row in rows[1:]:
    cols = row.find_all("td")

   
    if len(cols) >= 4:
        try:
            rank = cols[0].get_text(strip=True)
            name = cols[1].get_text(strip=True)
            industry = cols[2].get_text(strip=True)

            revenue = cols[3].get_text(strip=True).replace(",", "")
            profit = cols[4].get_text(strip=True).replace(",", "") if len(cols) > 4 else "0"
            employees = cols[5].get_text(strip=True).replace(",", "") if len(cols) > 5 else "0"
            headquarters = cols[6].get_text(strip=True) if len(cols) > 6 else "Unknown"

            data.append([rank, name, industry, revenue, profit, employees, headquarters])

        except:
            continue


df = pd.DataFrame(data, columns=[
    "Rank", "Name", "Industry", "Revenue", "Profit", "Employees", "Headquarters"
])


df = df.replace(r"\[\d+\]", "", regex=True)

df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")

df = df.dropna(subset=["Revenue"])


print("\nShape:", df.shape)
print(df.head(10))


if not df.empty:

    highest = df.loc[df["Revenue"].idxmax()]

    print("\nHighest Revenue Company:")
    print(highest["Name"])
    print("Revenue:", highest["Revenue"])

    print("\nTop Industries:")
    print(df["Industry"].value_counts().head(5))

else:
    print("No data scraped — check table index")


df.to_csv("largest_companies.csv", index=False)

print("\nDone - CSV saved")