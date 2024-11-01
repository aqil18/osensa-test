# Setup
# There is an api that produces all stations in map bound
# We must make n api calls over x min to gather all samples
import os
import argparse
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Function to fetch all monitoring stations within the specified bounds
async def fetch_stations(lat1, lng1, lat2, lng2):
    latlng = f"{lat1},{lng1},{lat2},{lng2}"

    ## Using client session to create disposable http session
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.waqi.info/map/bounds/?token={TOKEN}&networks=all&latlng={latlng}") as response:
            if response.status == 200:
                data = await response.json()
                if data["status"] == "ok":
                    return data["data"]
                else:
                    print(f"Error fetching stations: {data['message']}")
                    return []
            else:
                print(f"HTTP Error: {response.status}")
                return []

# Function to fetch real-time PM2.5 data for a specific station
async def get_pm25(session, station):
    async with session.get(f"https://api.waqi.info/feed/@{station['uid']}/?token={TOKEN}") as response:
        
        if response.status == 200:
            data = await response.json()

            if data["status"] == "ok":
                iaqi = data["data"]["iaqi"]
                return 0 if "pm25" not in iaqi else iaqi["pm25"]["v"]
            else:
                print(f"Error fetching data for station {station['city']['name']}: {data['message']}")
                return None
        else:
            print(f"HTTP Error: {response.status}")
            return None

# Main function
async def main(lat1, lng1, lat2, lng2, sampling_period, sampling_rate):
    stations = await fetch_stations(lat1, lng1, lat2, lng2)
    all_pm25_values = []

    async with aiohttp.ClientSession() as session:
        for _ in range(sampling_period):
            await asyncio.gather(
                
                for station in stations:
                    pm25 = get_pm25(session, station)
                    print(f"Station: {stations[idx]['city']['name']}, PM2.5: {pm25}")

                *[get_pm25(session, station) for station in stations]

            )

            for idx, pm25 in enumerate(pm25_values):
                if pm25 is not None:
                    print(f"Station: {stations[idx]['city']['name']}, PM2.5: {pm25}")
                    all_pm25_values.append(pm25)

            await asyncio.sleep(60 / sampling_rate)  # Wait based on the sampling rate

    if all_pm25_values:
        overall_average_pm25 = sum(all_pm25_values) / len(all_pm25_values)
        print(f"\nOverall PM2.5 average over {sampling_period} minutes: {overall_average_pm25:.2f}")
    else:
        print("No PM2.5 data collected.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate average PM2.5 for stations within specified bounds.")
    parser.add_argument("lat1", type=float, help="Latitude 1")
    parser.add_argument("lng1", type=float, help="Longitude 1")
    parser.add_argument("lat2", type=float, help="Latitude 2")
    parser.add_argument("lng2", type=float, help="Longitude 2")
    parser.add_argument("--sampling_period", type=int, default=5, help="Sampling period in minutes (default: 5)")
    parser.add_argument("--sampling_rate", type=int, default=1, help="Sampling rate in samples per minute (default: 1)")

    args = parser.parse_args()
    asyncio.run(main(args.lat1, args.lng1, args.lat2, args.lng2, args.sampling_period, args.sampling_rate))
