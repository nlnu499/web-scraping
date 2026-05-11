import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", class_="wikitable")
rows = table.find_all("tr")

data = []

for row in rows[1:]:
    cols = row.find_all("td")

    if len(cols) < 6:
        continue

    name = cols[0].get_text(strip=True).split("[")[0]
    industry = cols[1].get_text(strip=True).split("[")[0]
    revenue = cols[2].get_text(strip=True).replace(",", "")
    profit = cols[3].get_text(strip=True).replace(",", "")
    employees = cols[4].get_text(strip=True).replace(",", "")
    headquarters = cols[5].get_text(strip=True).split("[")[0]

    data.append([name, industry, revenue, profit, employees, headquarters])

df = pd.DataFrame(data, columns=[
    "Name", "Industry", "Revenue", "Profit", "Employees", "Headquarters"
])

df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
df["Employees"] = pd.to_numeric(df["Employees"], errors="coerce")

df = df.dropna()
df = df.drop_duplicates()

df.to_csv("largest_companies.csv", index=False)

print(df.head(10))
print("CSV file saved as companies.csv")