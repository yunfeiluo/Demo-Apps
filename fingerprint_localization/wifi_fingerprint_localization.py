import os
import sys
import numpy as np
import time
from multiprocessing import Pool
import subprocess

'''
Strength of current wifi: /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I
List of wifi available: /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s
Specific Wifi AP: /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --scan="Fei's home_5G"

Bluetooth: system_profiler SPBluetoothDataType
'''

# Global Vars
WIFI_APS = ["Fei's home_5G", "sangexxx", "keon", "OHarra-WiFi"]
FINGERPRINTS = {
            "Living room: Center": np.array([0.6364, 0.8815, 0.5217, 0.6134]),
            "Living room: Green Sofa": np.array([0.6566, 0.8204, 0.54, 0.5466]), 
            "Living room: Yellow Sofa": np.array([0.6966, 1.0, 0.5233, 0.5666]),
            "Yunfei's Bedroom: Bed": np.array([0.927, 0.597, 0.377, 0.76]),
            "Yunfei's Bedroom: Yunfei's Table": np.array([1.0, 0.7533, 0.4283, 0.7364]), 
            "Bathroom: Toilet": np.array([0.667, 0.66, 0.497, 0.407]),
            "Bathroom: Dressing Table": np.array([0.7636, 0.6632, 0.4567, 0.43]),
            "Kitchen": np.array([0.457, 0.583, 0.433, 0.29]),
            "Dining Area": np.array([0.517, 0.72, 0.46, 0.433])
        }

class WifiFingerPrint:
    def __init__(self, wifi_aps, fingerprints):

        self.WIFI_APS = wifi_aps

        self.FINGERPRINTS = fingerprints
        self.locations = [i for i in fingerprints]
        prints = [fingerprints[i] for i in fingerprints]

        self.fr_matrix = np.zeros((len(fingerprints), len(wifi_aps)))
        for i in range(len(fingerprints)):
            self.fr_matrix[i] = prints[i]

    def get_rssi(self, wifi_ap, n):
        print('Collecting', wifi_ap)
        rssis = list()
        for i in range(n):
            # res = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --scan=\"{}\"".format(wifi_ap)).read()
            res = subprocess.check_output("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --scan=\"{}\"".format(wifi_ap), shell=True)
            res = res.decode("utf-8")
            # print("res", res)
            res = [i for i in res.split() if len(i) > 0]
            ap_names = wifi_ap.split()
            rssi = list()
            for i in range(len(res)):
                if res[i] == ap_names[-1]:
                    rssi.append(int(res[i+1]))
            if len(rssi) > 0:
                rssis.append(rssi[-1])  # max is closest one, min is the farest, 0 is 2.4GHz, 1 is 5GHz
        # print(rssis)
        return np.mean(rssis) if len(rssis) > 0 else None
    
    def normalize(self, rssi, min_, max_):
        rssi = max(-90, min(-30, rssi)) # clip into range (-90, -30) (poor, perfect)
        return ((rssi + 90) / (60)) * (max_ - min_) + min_
    
    def retrieve_currect_finger_print(self, n=1):
        res = dict()
        for i in range(n):
            aps = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s").read()
            aps = [i for i in aps.split() if len(i) > 0]
            for j in range(len(aps)):
                name = aps[j]
                # special case
                if aps[j] == 'home_5G':
                    name = "Fei's home_5G"
                
                # regular case
                if name in self.WIFI_APS:
                    if res.get(name) is None:
                        res[name] = [round(self.normalize(int(aps[j+1]), 0, 1), 3)]
                    else:
                        res[name].append(round(self.normalize(int(aps[j+1]), 0, 1), 3))
        for name in res:
            res[name] = np.mean(res[name])
        return res
    
    def get_fingerprint(self, n=1):
        print('Collecting FingerPrints...')
        start = time.time()

        fingerprint = self.retrieve_currect_finger_print(n=n)
        
        # end
        end = time.time()
        print('Collecting time {} s'.format(round(end - start, 3)))
        print("Current Finger Print:", fingerprint)
        res_fp = list()
        for r in self.WIFI_APS:
            res_fp.append(fingerprint[r] if fingerprint.get(r) is not None else -1)
        print("Formatted FingerPrint", res_fp)
        return np.array(res_fp)

    def get_location(self):
        fingerprint = self.get_fingerprint(n=1)
        inds = [i for i in range(len(fingerprint)) if fingerprint[i] > -1] # filter out missing rssi
        dists = np.linalg.norm(self.fr_matrix[:, inds] - fingerprint[inds], axis=1, ord=2)
        # print('Distance', dists)
        location = self.locations[np.argmin(dists)]
        print("===============================\n")
        print("You are located at: {}\n".format(location))
        print("===============================")

if __name__ == '__main__':
    command = sys.argv[1]
    locator = WifiFingerPrint(WIFI_APS, FINGERPRINTS)

    if command == "collect":
        fingerprint = locator.get_fingerprint(n=5)
    elif command == "locate":
        locator.get_location()
    else:
        print("Unknown Command:", command)
        exit()
