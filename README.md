
<!-- HEADER -->
<p align="center"><img alt="Sakamoto Pic" src="https://i.imgur.com/mLQ3T06.png" height=300 width=200></p>
<h1 align="center">Sakamoto: The Discord Bot</h1>

<!-- BADGES -->
<p align="center">
  <a href="https://forthebadge.com" target="_blank">
    <img src="https://forthebadge.com/images/badges/built-with-love.svg" alt="Build with <3" height="35"/>
  </a>
  &nbsp;
  <a href="https://forthebadge.com" target="_blank">
    <img src="https://forthebadge.com/images/badges/made-with-python.svg" alt="Made with python" height="35" />
  </a>
  &nbsp;
  <a href="https://forthebadge.com" target="_blank">
    <img src="https://forthebadge.com/images/badges/powered-by-coffee.svg" height="35"/>
  </a>

<p align="center">
  <a
  href="https://github.com/psf/black"
   target="_blank">
      <img
        src="https://img.shields.io/badge/code%20style-black-000000.svg"
        alt="Code style: black" height="20" />
  </a>
<a href="http://makeapullrequest.com" target="_blank"><img src="https://img.shields.io/badge/PRs-welcome-bcentergreen.svg?style=shields" height="20"/>&nbsp;</a>  

<!-- ABSTRACT -->

<p align="center">A Discord Bot designed to incorporate elements of my previous bots: Shinobu and Flobot. Originally designed for the server Lazy Devs, soon to be Public bot.</p>

<!-- Quickstart-->
## Quickstart 
Requires the **Latest** version of [discord.py](https://github.com/Rapptz/discord.py), which _should_ be installed via pip, but it's always a good idea to check.  

**Install Requirements:**
``` sh
$ git clone https://github.com/Nekurone/Sakamoto.git
$ cd src
$ pip3 install -r requirements.txt
```
This _should_ install all requirements.  
Next, we need our Bot's token. [See here for how to get your Bot Token](https://discordpy.readthedocs.io/en/stable/discord.html)
We will place this within secrets.env which sits in `src/core`. (alternatively, use your favourite text editor to do this step)
``` sh
# remember to cd into src if not already there
$ nano core/secrets.env
# Remember, Nano is Ctrl+O to save and Ctrl+X to quit
```
The format we're looking for here is `export TOKEN=[YOUR-TOKEN-HERE]`

Now, we can run the bot. 
``` sh 
$ python3 main.py
```

To edit the prefix, go into `core/config.py` and edit `PREFIX = "!"`

## Current Features and their Status 
**Legend:**  
✅ - **At a point where I'm happy with it**  
🟡 - **In progress**  
❌ - **Not working / Needs major work**  


| Feature | Status |
|:---- | :----: |
|Bot Owner Commands | ✅ |
|Stats | 🟡 |

<h2 align="center">Keep an eye on this space for updates!</h2>
