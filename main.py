import requests
from twilio.rest import Client

STOCK_NAME = "NKE"
COMPANY_NAME = "Nike Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "TL3S50KODF1BTNJH"
NEWS_API_KEY = "e269a25c300b4b28b5daeef2c53e11ba"
TWILIO_SID = "ACe213dccca9b789431bbbcced7be811fd"
TWILIO_AUTH_TOKEN = "1fbb95d3187e9fb4e148d43efccc848d"  # Corrected variable name

# Get stock data
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]

# Sort the data by date to ensure correct order
sorted_data = sorted(data.items(), key=lambda x: x[0], reverse=True)
data_list = [value for (key, value) in sorted_data]

# Get yesterday's and the day before yesterday's closing stock price
yesterday_data = data_list[0]
day_before_yesterday_data = data_list[1]

yesterday_closing_price = yesterday_data["4. close"]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

# Calculate the percentage difference
difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
diff_percent = (difference / float(day_before_yesterday_closing_price)) * 100

# Check if the difference is greater than 5%
if diff_percent > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    # Format articles for SMS
    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    # Send SMS for each article
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+18445360661",  # Replace with your Twilio number
            to="+17044412275",    # Replace with your phone number
        )
