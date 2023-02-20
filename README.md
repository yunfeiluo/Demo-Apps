# Demo-Apps
This repository collects the small programs I've made. The application fields varies (e.g. localization, computer vision, and basic computation, etc.). The descriptions of each of these demo applications are presented in the following. They are open source and free to try them out. Any comments or ideas are welcome! Have fun! 

---

## Hand Gesture Recognition
- Made in 2022. Was one of the ideas for the final project of course CS654/690W on the topic of Internet of Things (IoT) at UMass Amherst. 
- Function(s): Detect hand gestures with one of the current best practices in literature, and project the result in a normalized space. 
- Under folder [hand_gesture_recognition](https://github.com/yunfeiluo/Demo-Apps/tree/main/hand_gesture_recognition)  
- Run the code by "python3 -m demo num_frame" where "num_frame" is the total number of frames that will be captured by the camera.  

---

## Fingerprint Localization
- Made in 2022. Was one of the ideas for the final project of course CS654/690W on the topic of Internet of Things (IoT) at UMass Amherst.  
- Function(s): Wifi based in-door localization. Fingerprint is collected from signals from 4 routers (1 in my room, 1 in living room, 2 from my apartment building).  
- Under folder [fingerprint_localization](https://github.com/yunfeiluo/Demo-Apps/tree/main/fingerprint_localization)
- Run "python3 -m wifi_fingerprint_localization locate" to see current location  
- Run "python3 -m wifi_fingerprint_localization collect" to collect fingerprint at current location

---

## HackUmass VI auto_music
- Created on Oct 2018. Was the team project in the HackUmass VI
- Generating music based on the recorded audio analysis
