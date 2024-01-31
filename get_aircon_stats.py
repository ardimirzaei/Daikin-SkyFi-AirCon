# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 21:10:52 2024

@author: ArdiMirzaei
"""

# import numpy as np
from SkyFi import SkyFi
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

load_dotenv()

PASSWORD = os.environ.get("PASSWORD")
AC_IP_ADDRESS = os.environ.get("AC_IP_ADDRESS")

if not os.path.isfile("aircon_historical.csv"):
    pd.DataFrame(
        columns=[
            "timestamp",
            "opmode",
            "units",
            "settemp",
            "fanspeed",
            "fanflags",
            "acmode",
            "tonact",
            "toffact",
            "prog",
            "time",
            "day",
            "roomtemp",
            "outsidetemp",
            "louvre",
            "zone",
            "flt",
            "test",
            "errcode",
            "sensors",
        ]
    ).to_csv("aircon_historical.csv", index=False)

aircon = SkyFi("Daikin", "Celsius", AC_IP_ADDRESS, PASSWORD)
aircon.update()
aircon_values = {
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"): {
        i.split("=")[0]: i.split("=")[1] for i in aircon.current_data
    }
}
df = pd.DataFrame.from_dict(aircon_values, orient="index")

if __name__ == "__main__":

    # df['timestamp'] = df.index
    df.to_csv("aircon_historical.csv", mode="a", index=True, header=False)
    # print("results")
