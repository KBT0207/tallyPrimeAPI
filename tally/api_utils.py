
import re
import json
import os
import glob
import time  # for sleep and timing
from datetime import date, time as dt_time  # rename to avoid conflict
from typing import Tuple
import pandas as pd
import re
import pyautogui as pg
import subprocess



def get_api_date_and_time(file: str) -> Tuple[date, dt_time]:
    try:
        base = file.rsplit("_", 1)[0]
        parts = base.split("_")[-6:]
        day, month, year, hour, minute, sec = map(int, parts)
        return date(year, month, day), dt_time(hour, minute, sec)
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid filename format: {file}") from e

def get_latest_file(base_dir: str) -> str:
    today = date.today()
    json_files = glob.glob(os.path.join(base_dir, '**', '*.json'), recursive=True)

    latest_file = None
    latest_time = dt_time(0, 0, 0)

    for file in json_files:
        try:
            d, t = get_api_date_and_time(file)
            if d == today and t > latest_time:
                latest_time = t
                latest_file = file
        except ValueError:
            continue

    return latest_file

def rename_latest_file(base_dir: str, material_centre: str, report_type: str, today) -> str:
    latest_file = get_latest_file(base_dir)

    if not latest_file:
        print("No files found for today.")
        return None

    file_dir, file_name = os.path.split(latest_file)
    _, file_extension = os.path.splitext(file_name)

    renamed_file = os.path.join(file_dir, f"{material_centre}_{report_type}_{today}{file_extension}")

    try:
        if os.path.exists(renamed_file):
            os.remove(renamed_file)
            print(f"Deleted existing file: {renamed_file}")

        start_time = time.time()
        os.rename(latest_file, renamed_file)
        rename_duration = time.time() - start_time
        print(f"Rename operation took {rename_duration:.6f} seconds.")

        # Confirm file exists using for-loop (up to 5 seconds)
        for _ in range(5):
            if os.path.exists(renamed_file):
                print(f"File renamed from {latest_file} to {renamed_file}")
                print("Completed")
                return renamed_file
            time.sleep(1)

        print("Rename failed or file not found after renaming.")
        return None

    except Exception as e:
        print(f"Error during rename: {e}")
        return None
    


def json_data_convert_amount_in_string(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        content = content.replace('\\u0004', '')
        content = content.replace('\\r\\n', '')
        content = re.sub(r'("Amount":\s*)([^"\s][^,\n\r]*)', r'\1"\2"', content)
        content = re.sub(r'("BIll Amount":\s*)([^"\s][^,\n\r]*)', r'\1"\2"', content)
        content = re.sub(r'("Rate Of Exchange":\s*)([^"\s][^,\n\r]*)', r'\1"\2"', content)
        content = re.sub(r'("Rate of Exchange":\s*)([^"\s][^,\n\r]*)', r'\1"\2"', content)
        content = re.sub(r',\s*"Item Group":\s*"Not Applicable"', '', content)

        content = re.sub(r'("OS Balance":\s*)([^"\s][^,\n\r]*)', r'\1"\2"', content)
        content = re.sub(r'("Bill Amount":\s*)([^"\s][^,\n\r]*)', r'\1"\2"', content)
        content = re.sub(r'("Due Amount":\s*)([^"\s][^,\n\r]*)', r'\1"\2"', content)


        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data

    except FileNotFoundError:
        print(f" File '{file}' not found.")
    except json.JSONDecodeError:
        print(f" Failed to decode JSON from '{file}'.")
    except Exception as e:
        print(f" Unexpected error: {e}")
    finally:
        print(f"Finished processing file: {file}")


fcy_comp = ["FCY Freshnova", "FCY Frexotic", "FCY KBE", "FCY KBEIPL", "FCY Orbit", "FCY KBAIPL"]

curr = {
    'Phaltan KBEIPL':'INR',
    'Phaltan NA KBE':'INR',
    'Phaltan A KBE': "INR",
    "Thane Fab Fresh": "INR",
    "Thane KBEIPL": "INR",
    "Nagar KBEIPL": "INR",
    "Vashi KBEIPL": "INR",
    "Gujarat KBEIPL": "INR",
    "Cargo KBEIPL": "INR",
    "Thane KBE": "INR",
    "Vashi KBE": "INR",
    "Nagar NA KBE": "INR",
    "Nagar A KBE": "INR",
    "Gujarat KBE": "INR",
    "MP KBE": "INR",
    "JDS KBE": "INR",
    "Cargo KBE": "INR",
    "Thane Orbit": "INR",
    "Gujarat Orbit": "INR",
    "Thane Frexotic": "INR",
    "Gujarat KBAIPL": "INR",
    "Thane KBAIPL": "INR",
    "MP KBAIPL": "INR",
    "MP KBFMSPL": "INR",
    "MP F&VPL": "INR",
    "MP KBFV&FPL": "INR",
    "MP KBVPL": "INR",
    "Thane KBAFPL": "INR",
    "UK KB Veg": "GBP",
    "USA KB Fruits": "USD",
    "Thane Aamrica": "INR",
    "Thane Freshnova": "INR",
    "Thane KB Fresh": "INR",
    "Thane Perfect Produce": "INR",
    "Thane Indifruit": "INR",
}

symbol_to_currency = {
    'AU$': 'AUD',
    "A$":"AUD",
    'CAD': 'CAD',
    '£': 'GBP',
    '€': 'EUR',
    '$': 'USD' 
}


def extract_all_postal_codes(text):
    if not isinstance(text, str):
        return []
    text = text.upper()
    patterns = [
        r'\b\d{6}\b',  # India
        r'\b\d{5}(?:-\d{4})?\b',  # US
        r'\b[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}\b',  # UK
        r'\b[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z] ?\d[ABCEGHJ-NPRSTV-Z]\d\b',  # Canada
        r'\b\d{5}\b',  # Germany, etc.
        r'\b\d{4}\b',  # Australia, etc.
    ]
    combined = '|'.join(patterns)
    return [match.strip() for match in re.findall(combined, text) if match.strip()]




def clean_string(value):
    if pd.isna(value):
        return value
    if isinstance(value, str):
        value = value.replace("_x000D_", "")
        value = re.sub(r'[\t\r\n]', ' ', value)
        value = value.replace("'", "''")
        value = value.encode('ascii', errors='ignore').decode()
        value = re.sub(r'\s+', ' ', value)
        value = value.lstrip("-/=%@#^&*()!@#$%^&*()_+-=[]{}|\\;:'\",.<>/?`~")
        value = value.strip()
    return value



def move_all_items(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dst_path = os.path.join(destination, item)

        try:
            os.rename(src_path, dst_path)
            print(f"Moved: {src_path} → {dst_path}")
        except Exception as e:
            print(f"Failed to move {src_path}: {e}")


def select_all_data():
    pg.hotkey('ctrl', 'home')
    time.sleep(1)
    vbs_script = (
        'Set WshShell = WScript.CreateObject("WScript.Shell")\n'
        'WScript.Sleep 3000\n'
        'WshShell.SendKeys "^+{END}"\n'
    )

    vbs_path = os.path.join(os.getcwd(), "send_ctrl_shift_end.vbs")

    with open(vbs_path, "w", encoding="utf-8") as f:
        f.write(vbs_script)

    subprocess.run(["wscript", vbs_path], check=True)


