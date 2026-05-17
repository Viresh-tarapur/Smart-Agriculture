import serial
import pynmea2
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

serial_port = 'COM3'

class GPSData(BaseModel):
    latitude: float
    longitude: float

def read_gps():
    try:
        ser = serial.Serial(serial_port, baudrate=9600, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None, None

    # Note: This is blocking. In a high-concurrency app, this should be in a thread or async.
    # For a direct migration, we keep the logic similar but wrap it.
    try:
        # We only try to read for a short time to avoid hanging the route forever if no data
        for _ in range(10): 
            line = ser.readline().decode('ascii', errors='replace')
            if line.startswith('$GPGGA'):
                msg = pynmea2.parse(line)
                ser.close()
                return msg.latitude, msg.longitude
    except Exception as e:
        print(f"Error reading GPS data: {e}")
    
    if ser.is_open:
        ser.close()
    return None, None

@router.get("/location", response_model=GPSData)
async def get_location():
    latitude, longitude = read_gps()
    if latitude is None or longitude is None:
        raise HTTPException(status_code=500, detail="Unable to read GPS data")
    return {"latitude": latitude, "longitude": longitude}
