# <p align="center">CurseForge Downloader 2023</p>

### Update: Since i started using the Prism Launcher for minecraft, i will no longer work on this project. I may update it to finish the TODO, when i can.

### Version: 1.6 / Requires Python 3.x (Or Higher)

Download Modpacks From CurseForge
<br>
$\color{red}\text{⟁}$ Script Can Stop Working In The Future Due To Hosts Changing Things

Tested With "Colony A New Odyssey - STABLE-1.0.7", Out Of 176 Mods, All Were Handled Correctly 🥳🥳🥳
<br>
<br>

Linux Compatibility: ~100% (Was Made In Linux)
<br>
Windows Compatibility: Unknown
<br>
<br>

## How To Install
1. Download `CSDownloader.py` (And `requirements.txt`) From The Repo Tree (Will Be Put As Releases In The Future)
2. Run `pip install -r requirements.txt` (While In The Same Folder As The File)
3. Run `python CSDownloader.py ./<path-to-modpack>` And Wait!
   <br>(The Script Will Put Everything In The "overrides" Folder It Will Make Next To The ZIP File;
   <br>Script Can Be Run From Anywhere Now)

<br>

## Features
   1. Detailed Mode (SLOW - Default):
      <br>Gives Detailed Output Of What The Script Is Doing
      <br>![DetailedMode](https://github.com/StellarSt0rm/CurseForgeDownloader2023/blob/b2ab628dab5f163cb7f609a015f3b2c408b4e312/README-RES/DetailedM.png)
      <br>
      <br>
   2. Threaded Mode (FAST - Bad For Slow Computers):
      <br>Goes BLAZINGLY FAST 🚀 ; Good For BIG Modpacks
      <br>$\color{red}\text{⟁}$ Fast Is Relative To How Big The Modpack Is, But It's Faster Than Detailed Mode
      <br>
      <br>Usage: `python CSDownloader.py -t <num / or "max">`
      <br>"max" Will Set The Max To '30', But You Can Specify A Larger Number (Not Recommended)
      <br>![ThreadedMode](https://github.com/StellarSt0rm/CurseForgeDownloader2023/blob/b2ab628dab5f163cb7f609a015f3b2c408b4e312/README-RES/ThreadedM.png)
      <br>
      <br>
   4. No Color:
      <br>Removes All Color, Except Bold
      <br>Usage: `python CSDownloader.py -n`
   
<br>

## TODO:
   1. Add `-u <url>` To Download Modpacks Directly (Without Needing The Zip Already Downloaded)
      
    ?. Polish GUI "Mode"

<br>

---
Made By $\color{magenta}\text{StellarSt0rm}$ -- $\color{green}\text{2023}$
