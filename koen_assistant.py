import csv
import datetime
import pyautogui
import time
import os
import sys
import requests
import pandas as pd
import AUTOTS
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import pygame
from bs4 import beautifulsoup

sys.setrecursionlimit(3000)

def fetch_news(api_key, query, language='en', page_size=5):
    news_url = f'https://newsapi.org/v2/everything'
    
    # Define the parameters for the API request
    params = {
        'apiKey': api_key,
        'q': query,        # Query keyword or topic
        'language': language,
        'pageSize': page_size
    }
    
    # Send the request to the News API
    response = requests.get(news_url, params=params)

    if response.status_code == 200:
        news_data = response.json()
        
        if news_data['totalResults'] > 0:
            articles = news_data['articles']
            print(f"Top {page_size} news articles for '{query}':")
            for i, article in enumerate(articles):
                print(f"{i + 1}. {article['title']}")
                print(f"   Source: {article['source']['name']}")
                print(f"   URL: {article['url']}")
                print()
        else:
            print(f"No news articles found for '{query}'.")
    else:
        print("Error: Unable to retrieve news data.")

def news_data_get():
    news_api_key = '57c13705e2564c38aa458f04652f03ab'  # Replace with your actual News API key
    
    print('What kind of news do you want to read?')
    print()
    print('1 - FTSE')
    print('2 - major news')
    print('3 - Hong Kong')
    print('4 - leave')
    print('Or enter your own ones to search for')
    while True:

        user_news_request = input('Enter: ')
        if user_news_request == '1':
            fetch_news(news_api_key, 'FTSE')
        elif user_news_request == '2':
            fetch_news(news_api_key, 'major news')
        elif user_news_request == '3':
            fetch_news(news_api_key, 'Hong Kong')
        elif user_news_request == '4':
            print('Left News')
            break
        else: 
            fetch_news(news_api_key, user_news_request)

def predict_stock():
    file = input("enter file name for stock prediction")
    csv_directory = '/Users/KoenCheng/Documents/stock_data_prediction_first_try'
    data = pd.read_csv(os.path.join(csv_directory, file))


    model = AUTOTS(
        forecast_length=10,  # Number of periods to forecast into the future
        prediction_interval=0.9,  # confidence
        ensemble='simple',  # how many models combined to do
        model_list="superfast",  # List of models
        max_generations=5,  # Maximum number of generations 
        verbose=3  # detail level
    )

    model = model.fit(data, date_col="Date", value_col="Close")

    forecast = model.predict()

    forecast_values = forecast.forecast

    upper_bounds = forecast.upper_forecast
    lower_bounds = forecast.lower_forecast

    model_params = forecast.model_parameters
    transformation_params = forecast.transformation_parameters
    time_index = range(len(forecast_values))


    print("Forecasted Values:-------------------------------------")
    print(forecast_values)

    print("\nUpper Bounds:")
    print(upper_bounds)

    print("\nLower Bounds:")
    print(lower_bounds)

    # Plot forecasted values
    plt.figure(figsize=(10, 6))
    plt.plot(time_index, forecast_values.values, label='Forecasted Values', color='blue')  # Use .values to extract the 1D array
    plt.fill_between(time_index, lower_bounds.values, upper_bounds.values, color='gray', alpha=0.5, label='Prediction Interval')  # Use .values for bounds
    plt.xlabel('Time Index')
    plt.ylabel('Value')
    plt.title('Time Series Forecast')
    plt.legend()
    plt.grid(True)
    plt.show()

def add_rountine():
    mon = []
    tue = []
    wed = [] 
    thu = []
    fri = []
    sat = []
    sun = []

def fetch_current_weather(location, weather_api_key):
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}'
    
    # Send the request to the API
    response = requests.get(weather_url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        weather_data = response.json()
        temperature_celsius = weather_data['main']['temp'] - 273.15
        # Extract and display relevant weather data from the JSON response
        print(f"City: {weather_data['name']}")
        print(f"Temperature: {temperature_celsius:.2f}°C")  # Format temperature with two decimal places
        print(f"Conditions: {weather_data['weather'][0]['description']}")
        print('---' * 20)
        print()
    else:
        print(f"Error: Unable to retrieve current weather data for {location}.")

def fetch_daily_weather_forecast(location, weather_api_key):
    forecast_url = f'https://api.openweathermap.org/data/2.5/forecast/daily?q={location}&cnt=7&appid={weather_api_key}'
    
    # Send the request to the API for the daily weather forecast (7 days)
    response = requests.get(forecast_url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        forecast_data = response.json()
        
        print("\nDaily Weather Forecast:")
        for forecast in forecast_data['list']:
            forecast_date = forecast['dt']
            forecast_temperature = forecast['temp']['day'] - 273.15
            forecast_conditions = forecast['weather'][0]['description']
            print(f"Date: {forecast_date}, Temperature: {forecast_temperature:.2f}°C, Conditions: {forecast_conditions}")
    else:
        print(f"Error: Unable to retrieve daily weather forecast data for {location}.")

def weather_data_get():
    weather_api_key = 'b54c0a0d43522f54f3bcb474facfa5cb'

    # Specify the locations (Reading, UK and Hong Kong)
    locations = ['Reading,uk', 'HongKong']
    for location in locations:
        fetch_current_weather(location, weather_api_key)
        fetch_daily_weather_forecast(location, weather_api_key)

def annoying():
    for i in range(20):
        pyautogui.moveTo(1159, 59)
        time.sleep(0.1)
        pyautogui.click()

def perform_action_login_LSE():
    #click on google
    pyautogui.moveTo(943, 947)
    pyautogui.click()
    print('working')
    #click on add tab
    pyautogui.moveTo(1408, 65)
    pyautogui.click()
    #click on bookmark
    pyautogui.moveTo(306, 134)
    pyautogui.click()
    #click on login
    time.sleep(5)
    pyautogui.moveTo(1288, 268)
    pyautogui.click()
    #login
    time.sleep(1)
    pyautogui.moveTo(412, 494) #username
    pyautogui.click()

    pyautogui.write('Koen.yyrtc')
    
    pyautogui.moveTo(504, 614) #password
    pyautogui.click()
    pyautogui.write('S601365g')
    
    pyautogui.moveTo(363, 677) #login button
    pyautogui.click()
    
    time.sleep(2)
    pyautogui.moveTo(1288, 268) #profile
    pyautogui.click()
 
    pyautogui.moveTo(627, 494) #trading portfolio
    pyautogui.click()
    
    time.sleep(2)
    pyautogui.moveTo(805, 789) #trading simulator
    pyautogui.click()
    pyautogui.click()
    
    time.sleep(1)
    pyautogui.scroll(-8) #scroll down

def clear_terminal():
    os.system('clear')

def whatsapp_sender():
    send_user_request = input('enter what you want to send: ')
    send_times = int(input('enter how many times do you want to send: '))
    print('OK, please go to your WhatsApp tab now.')
    time.sleep(7)
    for i in range(1, send_times):
        pyautogui.write(send_user_request)
        pyautogui.press('enter')
    print('success')

def send_email(subject, message, from_email, to_email, smtp_server, smtp_port, username, password):
    
    try:
        # Create an SMTP connection
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(username, password)

        # Compose the email
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Send the email
        smtp.sendmail(from_email, to_email, msg.as_string())
        smtp.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Email sending failed: {str(e)}")

def record_transaction():
    transaction_type = input("Enter transaction type (income/expense): ")
    amount = float(input("Enter the amount: "))
    category = input("Enter category: ")
    
    # Get the current balance
    current_balance = get_current_balance()
    
    if transaction_type.lower() == 'income':
        current_balance += amount
    elif transaction_type.lower() == 'expense':
        current_balance -= amount

    # Save the transaction
    with open('expenses.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([transaction_type, amount, category, current_balance])
    
    print(f"Transaction recorded. Current balance: {current_balance}")

def get_current_balance():
    current_balance = 0
    try:
        with open('expenses.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    current_balance = float(row[3])  # The balance is in the fourth column
    except FileNotFoundError:
        pass  # If the file doesn't exist, return 0
    return current_balance

def tell_joke():
    with open('jokes.txt', 'r') as file:
        jokes = file.read().splitlines()
    
    # Shuffle the order of jokes
    random.shuffle(jokes)
    
    for joke in jokes:
        print(joke)
        save = input("Save this joke? (yes/no): ")
        if save.lower() == 'yes':
            save_joke(joke)
            break

def save_joke(joke):
    with open('saved_jokes.txt', 'a') as file:
        file.write(joke + '\n')

def translate(text, target_language, source_language='auto'):

    #translator = Translator()

    # Perform the translation
    #translated = translator.translate(text, src=source_language, dest=target_language)

    #return translated.text
    return 0

def web_scrap():
    try: 
        web_scrap_url = input('enter url: ')
        html = requests.get(web_scrap_url)
        html.encoding = 'URF-8'
        sp = beautifulsoup(html.text, 'lxml')
        print(sp.title)
        print(sp.title.text)
        print(sp.h1)
        print(sp.p)

        web_scrap_input = int(input('do you want to search for something: '))
        if web_scrap_input == 1:
            web_scrap_search = input('enter target: ')
            sp.find_all(web_scrap_search)
        else:
            print()
    except ValueError:
        print('invalid input, please try again.')
        
activity_data = []

scores = {
    "pushup": 1,
    "rt": 1, #russian twists
    "1ap": 10, #1 arm pushup
    "pullup": 5,
    "studying": 100,
    "squat": 2,
    "hg": -800,  # Hardcore Gaming
    "ms": -200   # Mindless Scrolling
}

try:
    with open("total_score.csv", "r") as score_file:
        total_score_str = score_file.read()
        total_score_str = total_score_str.strip()  # Remove leading/trailing whitespace, including newline
        if total_score_str:  # Check if the string is not empty
            total_score = float(total_score_str)  # Use float instead of int
        else:
            total_score = 0
except FileNotFoundError:
    total_score = 0
print('file done')
def add_activity(activity, length):
    global total_score
    if activity == "view":
        print(f"Current Total Score: {total_score}")
    elif activity in scores:
        score = scores[activity] * length
        total_score += score
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        activity_data.append([timestamp, activity, length, score, total_score])
        print(f"Added {activity} for {length} hours. Score: {score}. Total Score: {total_score}. In {timestamp}.")
        
        # Save the data to a CSV file
        with open("activity_data.csv", "a", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Write activity data
            csv_writer.writerows(activity_data)
        
        # Save the updated total score to the CSV file
        with open("total_score.csv", "w", newline="") as score_file:
            score_writer = csv.writer(score_file)
            score_writer.writerow([total_score])
    else:
        print("Invalid activity!")


try:
    print('enter 1 to use pygame window')
    print('enter 2 to use normal versions')
    choice = int(input('enter: '))
    if choice == 1:
        pygame.init()
        # Create a Pygame window
        window_width = 800
        window_height = 600
        screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Your Pygame Window")

        # Set up a font for rendering text
        font = pygame.font.Font(None, 36)  

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #running = False
                    print('pygame window down')

            # Clear the screen
            screen.fill((255, 255, 255))  # Set background color (white)

            # Render and display text on the screen
            text = font.render('Options:', True, (0, 0, 0))  # Text, anti-aliased, color (black)
            screen.blit(text, (10, 10))  # Position of the text
            options = [
                'type login to login to LSE',
                'type clear to clear terminal',
                'type weather to receive information about the weather',
                'type add to add activity',
                'type predict to predict stock',
                'type news to receive news',
                'type send to send WhatsApp',
                'type email to send emails from here',
                'type record to record spendings',
                'type joke to get one'
            ]

            for i, option in enumerate(options):
                option_text = font.render(option, True, (0, 0, 0))
                screen.blit(option_text, (10, 50 + i * 40))  
        pygame.display.update()

    elif choice == 2:
        while True:
            print('options:')
            print()
            print('type login to login to LSE')
            print('type clear to clear terminal')
            print('type weather to recieve imformation about the weather')
            print('type add to add activity')
            print('type predict to predict stock')
            print('type news to recieve news')
            print('type send to send whatsapp')
            print('type email to send emails from here')
            print('type record to record spendings')
            print('type joke to get one')
            print('type ws to start web scraping')
            print()

        

            try:
                action = input("Enter what you want to do: ")
            
                if action.lower() == "exit":
                    running = False
                elif action.lower() == 'login':
                    perform_action_login_LSE()
                elif action.lower() == 'annoying':
                    annoying()
                elif action.lower() == 'clear':
                    clear_terminal()
                elif action.lower() == 'weather':
                    weather_data_get()
                elif action.lower() == 'add':
                    length_act = float(input("Enter length of action: "))  
                    add_activity(action, length_act)
                    print()
                elif action.lower() == 'predict':
                    predict_stock()
                elif action.lower() == 'news':
                    print('fetching')
                    news_data_get()
                elif action.lower() == 'send':
                    whatsapp_sender()
                elif action.lower() == 'email':
                    from_email = input('enter your email: ')
                    to_email = input("enter which email do you want to send it to: ")
                    subject = input("Your Subject: ")
                    message = input("Your message: ")
                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587
                    username = from_email
                    password = input("enter your gmail password")
                    send_email(subject, message, from_email, to_email, smtp_server, smtp_port, username, password)
                elif action.lower() == 'record':
                    record_transaction()
                elif action.lower() == 'joke':
                    tell_joke()
                elif action.lower() == 'tra':
                    while True:
                        print('type 1 to translate from French to English')
                        print('type 2 to translate from English to French')
                        trans_input = input('enter: ')
                        if trans_input == '1':
                            source_text_fe = input('enter what you want to translate: ')
                            target_language_fe = 'en'  
                            translated_text_fe = translate(source_text_fe, target_language_fe)
                            print(f"Translated text: {translated_text_fe}")
                        elif trans_input == '2':
                            source_text_ef = input('enter what you want to translate: ')
                            target_language_ef = 'fra'  
                            translated_text_ef = translate(source_text_ef, target_language_ef)
                            print(f"Translated text: {translated_text_ef}")
                elif action.lower() == 'ws':
                    web_scrap()
                else:
                    print('input not valid, please try again')
            except ValueError:
                print("input not valid (ValueError), you literally made this program yet you still don't know how to use it...")
except ValueError:
    print('Invalid Value')
