import telebot
import cv2
import time
import requests

# Initialize the Telegram bot
bot = telebot.TeleBot("6843529361:AAEEPwP36laT-Hc8nO3CQHcuwg80tIqQOH8")
CHAT_ID = "1484998700"

last_alert_time = 0

# Function to fetch IP-based location
def get_current_location():
    try:
        # First try with ipinfo.io
        response = requests.get('https://ipinfo.io/json', timeout=5)
        data = response.json()
        coords = data['loc']  # Example: "17.3850,78.4867"
        city = data.get('city', 'Unknown')
        region = data.get('region', 'Unknown')
        country = data.get('country', 'Unknown')
        return coords, f"{city}, {region}, {country}"
    except Exception as e:
        print(f"Error getting location: {e}")
        return "0,0", "Unknown Location"

# Function to send a Telegram alert with image and location
def send_telegram_alert(frame, message):
    print("telegram alert started")
    global last_alert_time
    current_time = time.time()

    if current_time - last_alert_time >= 60:
        try:
            # ✅ Get IP-based location
            coords, readable_location = get_current_location()
            location_url = f"https://www.google.com/maps?q={coords}"
            message_with_location = (
                f"{message}\n\n"
                f"📍 *Location*: {readable_location}\n"
                f"🔗 [View on Map]({location_url})"
            )

            # ✅ Save and send the frame as image
            cv2.imwrite("alert.jpg", frame)
            with open("alert.jpg", 'rb') as photo:
                bot.send_photo(
                    CHAT_ID,
                    photo,
                    caption=f"🚨 *ALERT* 🚨\n{message_with_location}",
                    parse_mode="Markdown"
                )

            # ✅ Optional: Additional text message
            bot.send_message(
                CHAT_ID,
                f"{message} Please take necessary precautions immediately!"
            )

            last_alert_time = current_time
            print(f"Telegram alert sent with location: {readable_location}")
        except Exception as e:
            print(f"Error sending Telegram alert: {e}")
    else:
        print("Waiting to send next alert. Time since last alert:", int(current_time - last_alert_time), "seconds")

