# Demo-Apps
This repository collects the small programs I've made. The applications' fields varies (e.g. localization, computer vision, daily tools, and basic computation, etc.). The descriptions of each of these demo applications are presented in the following. They are open source and free to try them out. Any comments or ideas are welcome! Have fun! 

---

## Cat Similarity
- Made in May 2023. Calculate similarity between cats/kitties. Find your cat/kitty among the cat population!
- Leveraging pretrained [Vision Transformer](https://github.com/lukemelas/PyTorch-Pretrained-ViT), followed by calculating cosine similarity between embeddings. (require manually crop of image for best performance).
- This program was used to assist us when targeting our first kitty! We then have a new family member from [Mirumkitty](https://www.mirumkitty.com/). 

---

## Make Random Choice
- Made in Jan 2023. Help with decision making like rolling a Dice
- Block choosing from same set of items in 4 hours
- Based on [Gumnbel Trick Sampling](https://arxiv.org/abs/2110.01515#:~:text=The%20Gumbel%2Dmax%20trick%20is,its%20unnormalized%20(log%2D)probabilities.)
- If there are difficulties in making from several choices, then let the program do it :)

---

## Hand Gesture Recognition
- Made in Apr 2022. Was one of the ideas for the final project of course CS654/690W on the topic of Internet of Things (IoT) at UMass Amherst. 
- Function(s): Detect hand gestures with one of the current best practices in literature, and project the result in a normalized space. 
- Under folder [hand_gesture_recognition](https://github.com/yunfeiluo/Demo-Apps/tree/main/hand_gesture_recognition)  
- Run the code by "python3 -m demo num_frame" where "num_frame" is the total number of frames that will be captured by the camera.  
- Using [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html) as backbone method. 

---

## Fingerprint Localization
- Made in Mar 2022. Was one of the ideas for the final project of course CS654/690W on the topic of Internet of Things (IoT) at UMass Amherst.  
- Function(s): Wifi based in-door localization. Fingerprint is collected from signals from 4 routers (1 in my room, 1 in living room, 2 from my apartment building).  
- Under folder [fingerprint_localization](https://github.com/yunfeiluo/Demo-Apps/tree/main/fingerprint_localization)
- Run "python3 -m wifi_fingerprint_localization locate" to see current location  
- Run "python3 -m wifi_fingerprint_localization collect" to collect fingerprint at current location

---

## HackUmass VI auto_music
- Created on Oct 2018. Was the team project in the HackUmass VI
- Function(s): Generating music based on the recorded audio analysis
- Under folder [auto_generative_piano_music](https://github.com/yunfeiluo/Demo-Apps/tree/main/auto_generative_piano_music)

