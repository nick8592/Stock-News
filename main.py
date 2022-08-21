import requests
import json
import datetime
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "173JAKX6IS89KDOV"
NEWS_API_KEY = "cf104ea061374f96af15bb4e4226edaf"
TWILIO_SID = "ACf6182316b77bff0c353731f9e92c8cfa"
TWILO_AUTH_TOKEN = "45c845d41fc6bedb324a6c708d11e7fb"

YOUR_PHONE_NUMBER = "+123456789"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
#TODO 2. - Get the day before yesterday's closing stock price
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = stock_response.json()
# data = json.dumps(data, indent=4)
time_series_data = data['Time Series (Daily)']
time_series_data_list = [value for (key, value) in time_series_data.items()]
first_closing_price = float(time_series_data_list[0]['4. close'])
second_closing_price = float(time_series_data_list[1]['4. close'])
# print(data)
# print(time_series_data)
# print(time_series_data_list)
print(first_closing_price, second_closing_price)

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
price_difference = first_closing_price - second_closing_price
up_down = None
if price_difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
print(price_difference)

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
difference_in_percentage = round((price_difference / (first_closing_price + second_closing_price)) * 100)
print(difference_in_percentage)

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
if abs(difference_in_percentage) > 5:
    news_params = {
        "q": COMPANY_NAME,
        "from": datetime.date.today(),
        "sortBy": "popularity",
        "apiKey": NEWS_API_KEY
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()['articles']


#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]
    print(three_articles)


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{difference_in_percentage}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

#TODO 9. - Send each article as a separate message via Twilio. 
    client = Client(TWILIO_SID, TWILO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_= "+15167306982",
            to=YOUR_PHONE_NUMBER
        )


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

