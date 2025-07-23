import pandas as pd
import matplotlib.pyplot as plt
#  # Optional: Better theme


url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
df = pd.read_csv(url)

print(df.shape)
print(df.columns)
df.head()

df.rename(columns={
    "ObservationDate": "Date",
    "Country/Region": "Country"
}, inplace=True)

df['Date'] = pd.to_datetime(df['Date'])
df.fillna(0, inplace=True)  # Replace NaNs with 0

country_df = df.groupby(['Country', 'Date'])[['Confirmed', 'Deaths', 'Recovered']].sum().reset_index()
country_df.head()

india = country_df[country_df['Country'] == 'India']
india.set_index('Date', inplace=True)

print("India COVID Summary:")
print(india.tail())

# Daily new cases
india['Daily Confirmed'] = india['Confirmed'].diff().fillna(0)
india['Daily Deaths'] = india['Deaths'].diff().fillna(0)
india['Daily Recovered'] = india['Recovered'].diff().fillna(0)

latest = df[df['Date'] == df['Date'].max()]
summary = latest.groupby('Country')[['Confirmed', 'Deaths', 'Recovered']].sum().sort_values(by='Confirmed', ascending=False)
print(summary.head(10))  # Top 10 countries by confirmed cases

summary['Death Rate (%)'] = (summary['Deaths'] / summary['Confirmed']) * 100
summary['Recovery Rate (%)'] = (summary['Recovered'] / summary['Confirmed']) * 100
print(summary[['Death Rate (%)', 'Recovery Rate (%)']].head(10))

plt.figure(figsize=(10,5))
plt.plot(india.index, india['Daily Confirmed'], color='blue', label='Daily New Cases')
plt.title("Daily New COVID-19 Cases in India")
plt.xlabel("Date")
plt.ylabel("Cases")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,5))
plt.plot(india.index, india['Confirmed'], label='Confirmed', color='orange')
plt.plot(india.index, india['Recovered'], label='Recovered', color='green')
plt.plot(india.index, india['Deaths'], label='Deaths', color='red')
plt.title("COVID-19 Cumulative Cases in India")
plt.xlabel("Date")
plt.ylabel("Number of Cases")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

