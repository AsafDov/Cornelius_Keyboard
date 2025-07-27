# Cornelius V1 Keyboard
My design of a very **efficient**, and **ergonomic** hand wired keyboard based on the Corne split keyboard.

![PXL_20250727_100216035](https://github.com/user-attachments/assets/1a63e829-4573-4db3-a2f9-da3f96406727)
![PXL_20250727_101542543](https://github.com/user-attachments/assets/c3f040ea-eadd-419c-bd09-d0640608e113)

---

# About the Project 
The modern keyboard is hardly an ergonomic/efficient solution for our modern times. 
The layout and structure is retained as an hommage for the old typewriter. While preserving historical artifacts and concepts is usually a good cultural idea. It is not smart for the sake of progress. 
Specifically in the case of the old typewrite:
</br>
<img width="506" height="421" alt="TypeWriter" src="https://github.com/user-attachments/assets/da6025ba-5aaf-4763-836f-252130492dc8" />
</br>

1. The characters were staggered, so as to prevent hammer overlap. Today there is no need for that, because there are hammers. Its all digital. No reason to stagger and bend the fingers this way and that.
2. The layout intentially makes little sense, so as to prevent jamming by stratigically placing frequently used character combinations farther apart.
This is definitly not a requisite anymore, but a hinder of progress.

To that end, the keyboard community has decided on attacking this inefficiency in two main paths. Changing the physical keyboard configuration, and changing the layout itself.

## Changing the 'QWERTY' layout:
- On 1936, Dr August Dvorak submitted a pattent for a more efficient layout nowadays called the `DVORAK`. This layout places the most frequently used characters on the home row, reducing finger pain and enhancing typing capabilitied.
- In 2006, `COLEMAK` was created. This layout is a supposed to make the `DVORAK` layout more accessible and easier to trasition to for `QWERTY` users.
- Nowadays with the AI revolution, one deveoper had used genetics algorithms and ML models to analyze hand movement and optimised to reduced finger fatigue while increasing efficiency. This layout desinged as a solution by the AI research is called `HALMAK`

## Changing the keyboard configuration
First of all, people realize one does not need to stagger the characters anymore with digital keyboards, so they unstaggered them, giving us keyboards like the [planck by scotto](https://olkb.com/collections/planck) by olkb.
Then they realized we dont need to bend our rists together when typing, causing long term injury. So they split the keyboards, giving us keyboards like the [ForScience keyboard](https://github.com/diimdeep/awesome-split-keyboards/blob/master/img/ForScience.jpg)
Then they realized that maybe the want to keep the stagger, but int the more natural **vertical** axis. Giving us the [Corne by Foostan](https://github.com/foostan/crkbd).

Looking at these keybaords one might notice that some keys are missing. This is due to the ability to layer keyboards on top of each other (digitally), utilizing keys to transfer between layouts, just as the SHIFT key changes the entire character layout to be capitalized. For me the ability to layer layouts was the huge selling point to build one of those. So I did. 
I have to admit I have not used tried a new layout, but am leaning towards DVORAK or HALMAK. 

For now, I will showcase my work and recent journey into building my own best producive and ergonomic keyboard - 

---

# THE CORNELIUS V1
### Features
1. 42 programmable keys
2. 10 degree tilt between keyboard sides
3. Utelizes the RP2040 MCU
4. Has a screen to indicate the corrent layer
5. Also has a mouse configuration
6. Utelizes JanLunge's POG for firmware programming
7. RP2040-zero is swappable quickly if burned. No soldering required.

### Versions I built before the Cornelius V1
After building my first macropad, [posted on my website](https://www.asafslaboratory.com/?p=416) I started building full keyboards.

#### 1. REDOX 2
Back in 2022 I found [this youtube video](https://www.youtube.com/watch?v=Cwkf7HFcUkY&list=LL&index=162&t=321s&ab_channel=Shiftux) by Shiftux which ignited my passion for split keyboards. Here was the initial result:
![IMG_20220803_204759](https://github.com/user-attachments/assets/691f5f37-5480-4b8d-94fc-09781fe83794)

I took apart an old keybaord birthday present for the switches and put it together. After seeing it worked I have decided to pivot to a smaller form factor keybaord, which led me to the my next try

#### 2. REDOX 2.2
I wanted to make the keeb smaller and encorporate a big scroller wheel next to the thumb so I designed and built this:
![20230714_192518-EDIT](https://github.com/user-attachments/assets/22aae594-69f4-4320-affc-abb382b69106)

#### 3. Choco REDOX
Next I wanted a lower profile using Gateron low profile switches, so I designed and built this:
![20230825_115939](https://github.com/user-attachments/assets/21c1f35c-0db1-4b83-9eda-88e6c5e54850)

I had used this keyboard for a long time, until I decided to go smaller, towards the Corne, and leave the split keyboard world. 
The split keyboards are a delight, but aren't easy to carry around without a proper case. 

That brings me to the CORNELIUS V1. Which is really useful and fun.

### Current layout of the Cornelius 1
 I keep changing the layout from time to time, trying to find the best one for me, but here it is for now, using JanLunge's [POG](https://github.com/JanLunge/pog):
#### BASE LAYER:
<img width="833" height="304" alt="image" src="https://github.com/user-attachments/assets/f685f47d-6469-4656-92b5-3186e1002344" />

#### NAVIGATION LAYER:
<img width="833" height="304" alt="image" src="https://github.com/user-attachments/assets/d602049c-6659-47e4-bfb2-bd02c570a205" />

#### SYMBOL LAYER:
<img width="833" height="304" alt="image" src="https://github.com/user-attachments/assets/d2c284a8-049d-4659-88ad-ebb24d6a971c" />

---

# Build it yourself

## Components
1. RP2040-Zero
2. 0.96" OLED I2C Display
3. Gateron Low Profile 2.0 Mechanical Switch
4. Low porfile PBT Cherry MX keycaps
5. 3d printed case
6. m2.5 Screws
7. m2.5 Spacers
8. 1N4148 Diods
9. Rubber Feet

TODO - Rest of guide

