Major progress #1       Very early attempt         11-10-2024 
I managed to get an OV7670 camera to work with my Arduino UNO. In this screen shot there are multiple images that are supposed to make up a video stream. I was trying to use computer vision to detect the circle on the image.
Obviously this arduino was not going to be powerful enough to do what I needed, but I would estimate I spent around 5 hours to get this far (using a camera with an arduino uno was not easy)
<img width="1652" height="577" alt="Screenshot 2026-07-05 183715" src="https://github.com/user-attachments/assets/7c86aa0b-27bc-49f2-811a-d1bcab5ab0e0" />

Major progress #1.5       Raspberry Pi            12-25-2024
I got a raspberry pi, so I could use a camera with more than 3 fps. This was my first time every using a raspberry pi, or any linux computer so there were many challenges.

Note: During this period I did not have a phone, and I have fully reinstalled my raspberry pi OS, so I don't have much pictures.

Major progress #2         Working camera raspberry pi           3-1-2025
I got the raspberry PI's camera to work. I struggled alot with the operating system version of bookworm vs bullseye. Since I used a raspberry pi 4, and most tutorials new tutorials were for a pi 5 I couldnt find any way to get the camera to work with the latest raspberry pi os. I decided to just use a legacy version, and it worked. I also remember wasting I think 2 full weeks trouble shooting why the camera wouldn't work, and it was because I needed to include sudo.

Major progress #3         First "Functioning" Model             5-28-2025
I had the idea that I should make the robot as cheap as possible, but this ended up in the robot being pretty bad.  
<img width="751" height="372" alt="image" src="https://github.com/user-attachments/assets/b36a0350-1e36-4957-a413-8c7e0987a5fe" />
In this picture it shows the CAD model of the arm. I tried 3D printing my own ball joint (I actually spent so much time on this, I had like 100+ prints), and it's tolerances were either too big and the robot would just fall down, or it would be too tight and the 3D printed parts would be stuck together. 
<img width="512" height="346" alt="image" src="https://github.com/user-attachments/assets/423b0004-5806-4f6d-943e-c65a61dc4238" />
This picture shows the cad model of the base, the 3 rectangular sections are ment to hold the servo. I was also using MG90 servos (cheap tiny servos), and they were not even strong enough to lift the platform.

Major progress #4         Better servo                    7-5-2025

I bought 3 20kg servos, these were much better, and I actually used it in the final project. I also got a phone so I have a video now.
https://github.com/user-attachments/assets/66a18712-17ef-4c83-ba56-ccc3214245ea

Major progress #5          Complete remodle               7-9-2025           

I realized that my top platform was WAY too big, and my entire design was waay too flimsy, so I completely remade the CAD.
https://github.com/user-attachments/assets/3edda55c-6e69-4948-bfae-6c81fb5bd675











