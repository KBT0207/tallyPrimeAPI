from datetime import datetime, time, timedelta
import time as t  # Avoid conflict with datetime.time

def wait_if_in_range():
    now = datetime.now().time()

    # Define time range: from 11:00 PM to 12:30 AM (next day)
    start_time = time(23, 0)   # 11:00 PM
    end_time = time(0, 30)     # 12:30 AM

    if now >= start_time or now < end_time:
        # Calculate how many seconds to sleep until 12:30 AM
        now_dt = datetime.now()
        target_dt = now_dt.replace(hour=0, minute=30, second=0, microsecond=0)

        # If current time is already past 12:30 AM, wait until next day's 12:30 AM
        if now >= end_time:
            target_dt += timedelta(days=1)

        seconds_to_sleep = (target_dt - now_dt).total_seconds()
        print(f"Sleeping for {seconds_to_sleep:.0f} seconds until 12:30 AM...")
        t.sleep(seconds_to_sleep)
    else:
        print("Current time is outside the range. No need to wait.")


