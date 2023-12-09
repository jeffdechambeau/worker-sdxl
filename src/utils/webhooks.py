import requests


def send_webhook_notification(webhook_url, data):
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        print(f"Webhook notification sent successfully: {response.text}")
    except requests.RequestException as e:
        print(f"Failed to send webhook notification: {e}")
