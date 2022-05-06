import os
import numpy as np
import time
from multiprocessing import Pool

'''
Strength of current wifi: /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I
List of wifi available: /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s
Specific Wifi AP: /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --scan="Fei's home_5G"
'''

# Global Vars
WIFI_APS = ["Fei's home_5G", "sangexxx", "keon", "OHarra-WiFi"]
FINGERPRINTS = {
            "Living room": np.array([0.64, 0.93, 0.517, 0.65]),
            "Yunfei's Bedroom": np.array([0.927, 0.597, 0.377, 0.76]),
            # "Xiao Cai's Bedroom": [],
            "Bathroom": np.array([0.667, 0.66, 0.497, 0.407]),
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
            res = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --scan=\"{}\"".format(wifi_ap)).read()
            res = [i for i in res.split() if len(i) > 0]
            ap_names = wifi_ap.split()
            rssi = list()
            for i in range(len(res)):
                if res[i] == ap_names[-1]:
                    rssi.append(int(res[i+1]))
            if len(rssi) > 0:
                rssis.append(rssi[-1])  # max is closest one, min is the farest, 0 is 2.4GHz, 1 is 5GHz
        return np.mean(rssis) if len(rssis) > 0 else None

    def get_fingerprint(self, n=3):
        print('Collectin FingerPrints...')
        start = time.time()
        fingerprint = dict()

        # iterate over pre-set wifi aps
        for wifi_ap in self.WIFI_APS:
            rssi = self.get_rssi(wifi_ap, n)
            # print("{}: {}".format(wifi_ap, rssi))

            # normalize to [0, 1]
            if rssi is None:
                rssi = -1
            else:
                rssi = round(self.normalize(rssi, 0, 1), 3)

            # set
            fingerprint[wifi_ap] = rssi
        
        # end
        end = time.time()
        print('Collecting time {} s'.format(round(end - start, 3)))
        print(fingerprint)
        return np.array([fingerprint[r] for r in fingerprint])

    def normalize(self, rssi, min_, max_):
        rssi = max(-90, min(-30, rssi)) # clip into range (-90, -30) (poor, perfect)
        return ((rssi + 90) / (60)) * (max_ - min_) + min_

    def scan(self):
        res = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --scan=\"XFINITY\"").read()
        print(res)

    def get_location(self):
        fingerprint = self.get_fingerprint(n=1)
        dists = np.matmul(self.fr_matrix, fingerprint)
        location = self.locations[np.argmax(dists)]
        print("You are located at", location)

if __name__ == '__main__':
    locator = WifiFingerPrint(WIFI_APS, FINGERPRINTS)
    # locator.scan()
    # fingerprint = locator.get_fingerprint(n=5)
    locator.get_location()
