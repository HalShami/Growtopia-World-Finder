# Growtopia-World-Finder
This is was my AP CSP Create Performance Task (got a 5 :D) and then transitioned to be my Sophomore year of High School's summer project basically... (Note for college admission officers, devs can ignore this)

This program is **designed to search for worlds in the game Growtopia**. You can specify the length of the world name, and the number of iterations (worlds to search) you want to perform. 
Depending on which version of the code you run, each iteration can take from 5(basic GUI version with no AI detection) to 15 seconds (OCR version with 3 screenshots to increase accuracy). 
The purpose is to **find worlds that are not locked** with short names as they are highly valued.
The **first version is a CLI version**, the **second version incorporates a GUI** designed with TKinter. 
Keep in mind that there are **2 scripts**, one designed for **1080p** screen users and another for **1440P** users. Also, you **must run Growtopia in full screen mode**.
The Initial Versions rely on the user to monitor the program and look for the empty worlds as it runs through random worlds automatically.
Later versions utilize Neural Networks such as **CNN's and Optical Character Recognition Algorithms to detect worlds that are not locked/taken and save the worlds' names to a .txt file** which can later be accessed by the user.
The program is still in early stages so expect bugs; however, if you would like to contribute to this project or have any feedback feel free to do so.

Known Issues:
False Positives with OCR (30% on average)
False Positives with CNN (over 60% - moved to OCR since using CNN needed too much data and I didn't have the patience to collect it...)
Pause Function (pause the program by pressing 'pause' on your keyboard) is broken in some scripts
Server Latency can break the entire script currently (This is because it is built to play the game as a normal user, does not interact with game files like cheat engines - good for not getting banned, not good to keep script running for a long time) Note: If you know how to make this script interact with the game directly like a cheat engine, please reach out to me to discuss collaborating on this!)

