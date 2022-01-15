import pathlib
from typing import Optional

import uvicorn
from fastapi import FastAPI
from datetime import datetime
from cassandra.cqlengine.management import sync_table
from app.models import WeatherItem, WeatherInterface
from typing import List

from app import (
    config,
    db,
)

app = FastAPI()
settings = config.get_settings()

BASE_DIR = pathlib.Path(__file__).resolve().parent

DB_SESSION = None


@app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(WeatherInterface)


@app.get("/")
def read_index(q: Optional[str] = None):
    return {"hello": "world"}


# curl -X POST -H "Content-Type: application/json" --data '{"elapsed_time": 6245, "timestamp": [2020, 7, 26, 12, 2,
# 21, 6, 208], "wind_direction_raw": 108, "wind_speed_raw": 5, "message_id": 666, "rain_amount_raw": "0"}'
# http://192.168.1.151:9494/station f'/2.5/weather?q={query}&appid={api_key_}&units={units}' def _report_url(query:
# str, api_key_: Optional[str], units: str) -> str: return ( f'https://api.openweathermap.org/data'
# f'/2.5/weather?q={query}&appid={api_key_}&units={units}' )


# ?elapsed_time=6245&timestamp=2020,7,26,12,2,21,6,208&wind_direction_raw=108&wind_speed_raw=5&message_id=666&rain_amount_raw=0"
# {
#     "elapsed_time":6245,
#     "timestamp":[2020,7,26,12,2,21,6,208],
#     "wind_direction_raw":108,
#     "wind_speed_raw":5,
#     "message_id":666,
#     "rain_amount_raw":0
# }
@app.post("/station")
async def create_item(item: WeatherItem):
    data = {
        'created_date': datetime.now(),
        'temp_Ds12B20': round(item.temp_Ds12B20, 2),
        'temp_dht11': round(item.temp_dht11, 2),
        'temp_bme280': round(item.temp_bme280, 2),
        'humidity_dht11': round(item.humidity_dht11, 2),
        'humidity_bme280': round(item.humidity_bme280, 2),
        'pressure_bme280': round(item.pressure_bme280, 2),
        'altitude_bme280': round(item.altitude_bme280, 2)
    }
    obj = WeatherInterface.objects.create(**data)  # NoSQL -> cassandra -> DataStax AstraDB
    return obj


@app.get("/history")  # /?q=this is awesome
def list_inference():
    q = WeatherInterface.objects.all()
    return list(q)


def main() -> None:
    on_startup()
    uvicorn.run(app)


# uvicorn main:app --host 192.168.1.151 --port 9494
if __name__ == '__main__':
    main()
