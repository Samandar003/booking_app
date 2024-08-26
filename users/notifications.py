from fcm_django.models import FCMDevice

def send_notification_to_user(user, title, message):
    devices = FCMDevice.objects.filter(user=user)
    devices.send_message(
        title=title,
        body=message,
        icon="icon",  # Optional
        data={"key": "value"}  # Optional
    )