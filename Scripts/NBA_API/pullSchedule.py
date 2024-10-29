import schedule
import time

# function to run every day at 6:00am
def job():
    # run the main.py script
    os.system('python3 main.py regularSeasonDailyPull.config')

# schedule every day at 6:00am
# from the following link: https://stackoverflow.com/questions/43670224/python-to-run-a-piece-of-code-at-a-defined-time-every-day#:~:text=you%20can%20make%20use%20of%20crontab%20linux%20utility%2C,enter%20like%20this%2C%20for%20eecuting%20at%202.30pm%20daily
schedule.every().day.at("06:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)