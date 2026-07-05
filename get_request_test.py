from threading import Thread
import time
import uvicorn as uv
import requests
from blue_archive_characters_api import server
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
def test_get_server():
    print("Server started")
    try:
        resp = requests.post(f'http://127.0.0.1:8000/students/gacha-simulate', json={"simulations": 500, "pyroxene": 24000, "rate_up": 0.007, "rate_up_3_star": 0.03, "pity_threshold": 100, "spark_threshold": 200})
        if resp.status_code == 200:
            df = pd.json_normalize(resp.json())
            print(df)
        else:
            print(resp.status_code)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    
    t = Thread(target=uv.run, args=(server,), kwargs={'host': '127.0.0.1', 'port': 8000}, daemon=True)
    t.start()
    time.sleep(5)
    test_get_server()