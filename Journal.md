# Major Progress Log

---

## Major progress #1 — Very early attempt — 11-10-2024

I managed to get an OV7670 camera to work with my Arduino UNO. In this screenshot there are multiple images that are supposed to make up a video stream. I was trying to use computer vision to detect the circle on the image.  
Obviously this Arduino was not going to be powerful enough to do what I needed, but I would estimate I spent around 5 hours to get this far (using a camera with an Arduino UNO was not easy).

<img width="1652" height="577" alt="Screenshot 2026-07-05 183715" src="https://github.com/user-attachments/assets/7c86aa0b-27bc-49f2-811a-d1bcab5ab0e0" />

---

## Major progress #1.5 — Raspberry Pi — 12-25-2024

I got a Raspberry Pi, so I could use a camera with more than 3 FPS. This was my first time ever using a Raspberry Pi, or any Linux computer so there were many challenges.

Note: During this period I did not have a phone, and I have fully reinstalled my Raspberry Pi OS, so I don't have much pictures.

---

## Major progress #2 — Working camera Raspberry Pi — 3-1-2025

I got the Raspberry Pi's camera to work. I struggled a lot with the operating system version of Bookworm vs Bullseye. Since I used a Raspberry Pi 4, and most tutorials were for a Pi 5 I couldn't find any way to get the camera to work with the latest Raspberry Pi OS. I decided to just use a legacy version, and it worked. I also remember wasting I think 2 full weeks troubleshooting why the camera wouldn't work, and it was because I needed to include sudo.

---

## Major progress #3 — First "Functioning" Model — 5-28-2025

I had the idea that I should make the robot as cheap as possible, but this ended up in the robot being pretty bad.

<img width="751" height="372" alt="image" src="https://github.com/user-attachments/assets/b36a0350-1e36-4957-a413-8c7e0987a5fe" />

In this picture it shows the CAD model of the arm. I tried 3D printing my own ball joint (I actually spent so much time on this, I had like 100+ prints), and its tolerances were either too big and the robot would just fall down, or it would be too tight and the 3D printed parts would be stuck together.

<img width="512" height="346" alt="image" src="https://github.com/user-attachments/assets/423b0004-5806-4f6d-943e-c65a61dc4238" />

This picture shows the CAD model of the base, the 3 rectangular sections are meant to hold the servo. I was also using MG90 servos (cheap tiny servos), and they were not even strong enough to lift the platform.

---

## Major progress #4 — Better servo — 7-5-2025

[![Watch the video](https://i.sstatic.net/Vp2cE.png)](https://github.com/user-attachments/assets/66a18712-17ef-4c83-ba56-ccc3214245ea)

---

## Major progress #5 — Complete remodel — 7-9-2025

[![Watch the video](https://i.sstatic.net/Vp2cE.png)](https://github.com/user-attachments/assets/3edda55c-6e69-4948-bfae-6c81fb5bd675)

---

## Major progress #6 — Inverse kinematics — 7-15-2025

I implemented the inverse kinematics into the robot. I actually had experience working with inverse kinematics (from a pen plotter project), but the inverse kinematics for this robot was much much more complex. Luckily this 3-RRS mechanism is somewhat common, and I was able to find a very good website solving the inverse kinematics: https://www.george-yuanji-wang.xyz/blog/3rrs

---

## Major progress #7 — Actually good design — 7-20-2025

[![Watch the video](https://i.sstatic.net/Vp2cE.png)](https://github.com/user-attachments/assets/80a28c44-ffd9-41d4-be03-82f9cb3cf3cc)

---

## Major progress #8 — OpenCV and computer vision — 8-16-2025

I started tuning the computer vision. The main strategy was to have the ball be bright green, and have a black and white background. I spent a very long time blindly adjusting HSV values, but not surprisingly that did not work well. Then I had a breakthrough where I displayed the min and max ranges of the HSV values, and the real HSV values that the camera was detecting. This allowed me to pinpoint the values that needed adjusting, and I could finally detect the ball.

<img width="5712" height="4284" alt="IMG_0760_(2)" src="https://github.com/user-attachments/assets/f966e7a4-45c0-4545-ac4b-47b03b45001a" />

---

## Major progress #10 — PID — 8-25-2025

[![Watch the video](https://i.sstatic.net/Vp2cE.png)](https://github.com/user-attachments/assets/ee772e6e-aaa9-4394-bfa0-724793c38a50)

This was actually my first time tuning PID, so I made a pretty simple but devastating mistake where the error/offset was always positive. This made it so that no matter how I tuned it, it would still be unstable. In the end I managed to tune the PID so that it can balance the ball.

Mission success.
