import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from typing import Optional
from datetime import datetime
from pydantic.main import BaseModel


# tak chcę przechowywać ten obiekt w bazie danych
class WeatherInterface(Model):
    __keyspace__ = 'weather_station'
    # uuid = columns.UUID(primary_key=True, default=uuid.uuid1)  # uuid.uuid1 -> timestamp
    # json = {"danePogodowe": {"temperatura": {"DS12B20": 15,  "DHT11": 16,   "BME280": 15},   "wilgotnosc": {
    #     "DHT11": 100, "BME280": 200},  "cisnienie": {"BME280": 1000 }, "wysokoscnpm": {"BME280": 100}}}
    created_date = columns.DateTime(primary_key=True)
    temp_Ds12B20 = columns.Float()
    temp_dht11 = columns.Float()
    temp_bme280 = columns.Float()
    humidity_dht11 = columns.Float()
    humidity_bme280 = columns.Float()
    pressure_bme280 = columns.Float()
    altitude_bme280 = columns.Float()


# GET - mogę zamodelować jak będzie wyglądać output na podstawie WeatherInterface
class WeatherItem(BaseModel):
    created_date: Optional[datetime]
    temp_Ds12B20: float
    temp_dht11: float
    temp_bme280: float
    humidity_dht11: float
    humidity_bme280: float
    pressure_bme280: float
    altitude_bme280: float
