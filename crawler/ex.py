import datetime

delta_hour = 0

while True:
    current_hour = datetime.datetime.now().hour

    if delta_hour != current_hour:
        print("1")

    delta_hour = current_hour