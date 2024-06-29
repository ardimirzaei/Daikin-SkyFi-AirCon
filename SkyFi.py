# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 20:03:17 2024

@author: ArdiMirzaei
"""

import time
import requests


class SkyFi:
    """Representation of a demo climate device."""

    def __init__(self, name, unit_of_measurement, host, password):
        """Initialize the climate device."""
        self._name = name
        self._unit_of_measurement = unit_of_measurement
        self._host = host
        self._password = password
        self._fan_list = ["", "Low", "Medium", "High"]
        self._operation_list = ["Off", "Auto", "Heat", "Cool", "Dry"]
        self._operation_dict = {
            0: "Off",
            1: "Auto",
            2: "Heat",
            8: "Cool",
            16: "Dry",
        }
        self._operation_mode = {
            "Off": 0,
            "Auto": 1,
            "Heat": 2,
            "Cool": 8,
            "Dry": 16,
        }
        self._zones_numbers = {
            1: 8,
            2: 7,
            4: 6,
            8: 5,
            16: 4,
            32: 3,
            64: 2,
            128: 1,
        }
        self._zone_names = {
            1: "Theatre",
            2: "Gym",
            3: "Family",
            4: "Beds",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
        }
        self._current_temperature = 21.0
        self._target_temperature = 21.0
        self._current_fan_mode = self._fan_list[1]
        self._current_operation = self._operation_list[0]

    def update(self):
        payload = f"/ac.cgi?pass={self._password}"
        data = self.doQuery(payload)
        self.set_props(data)
        # return(self.current_data)

    def set_props(self, data):
        plist = {}
        lst = data.split("&")
        for x in lst:
            v = x.split("=")
            plist[v[0]] = v[1]

        self.current_data = lst
        self._operation_mode = int(plist["opmode"])
        self._current_temperature = float(plist["roomtemp"])
        self._target_temperature = float(plist["settemp"])
        # if int(plist['opmode']) == 0:
        #     self._current_operation = self._operation_list[0]
        # else:
        #     self._current_operation = self._operation_dict[
        #         find_the_base_numbers(int(plist['acmode']), list(self._operation_dict.keys()))
        #         ]
        self._current_fan_mode = self._fan_list[int(plist["fanspeed"])]
        self._zones = [
            self._zone_names[i]
            for i in [
                self._zones_numbers[i]
                for i in find_the_base_numbers(
                    target_number=int(plist["zone"]),
                    numbers=list(self._zones_numbers),
                    results=[],
                )
            ]
        ]

    def doQuery(self, payload):
        """send query to SkyFi"""
        data = None
        retry_count = 5
        while retry_count > 0:
            retry_count = retry_count - 1
            try:
                # conn = http.client.HTTPConnection(self._host, 2000)
                # conn.request("GET", payload)
                # resp = conn.getresponse()
                # data = resp.read().decode()
                # conn.close()
                url = f"http://{self._host}:2000{payload}"
                # print(url)
                resp = requests.get(url)
                data = resp.text
                # print(data)
                retry_count = 0
            except Exception as ex:
                if retry_count == 0:
                    print(
                        "Query: {} failed {}: {}".format(
                            self._name, payload, ex
                        )
                    )
                # conn.close()
                time.sleep(2)
        return data

    def set_values(self, toggle_power):
        base_template = f"/set.cgi?pass={self._password}"

        base_template += "&p=1" if toggle_power else "&p=0"

        data = self.doQuery(base_template)
        self.set_props(data)
        # print(base_template)


# Other Functions


def find_the_base_numbers(target_number, numbers, results=[]):
    for i, number in enumerate(reversed(numbers)):

        res = target_number - number
        # print(res)
        if res > 0:
            results.append(number)
            # print(numbers[:-1])
            find_the_base_numbers(res, numbers[:-1], results)
            break
        elif res == 0:
            results.append(number)
            break
        else:
            find_the_base_numbers(target_number, numbers[:-1], results)
            break

    return results


if __name__ == "__main__":
    # app.run(debug=True, use_reloader=False)
    aircon = SkyFi("Daikin", "Celsius", "192.168.1.2", 123456)
    # aircon.update()
    # aircon.set_values(toggle_power = 0)
