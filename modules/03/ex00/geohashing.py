import sys

import antigravity


def geohashing():
    if len(sys.argv) == 4:
        try:
            latitude = float(sys.argv[1])
            longitude = float(sys.argv[2])
            date = (sys.argv[3])
        except Exception as e:
            print(f"Error occurred :{e}")

        antigravity.geohash(latitude, longitude, date.encode())
    else:
        print(f"Usage: python3 {sys.argv[0]} latitude logitude date")

if __name__ == "__main__":
    geohashing()
