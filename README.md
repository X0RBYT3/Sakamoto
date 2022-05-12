<div id="top"></div>

[![Python][python-shield]][python-url]
[![Issues][issues-shield]][issues-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![MIT License][license-shield]][license-url]
[![Black][black-shield]][black-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Nekurone/Sakamoto">
    <img src="https://i.kym-cdn.com/photos/images/newsfeed/000/708/396/3d6.gif" alt="Logo">
  </a>
<h1 align="center">Sakamoto</h1>

  <p align="center">
    A Discord Bot with no particular aim, currently has a handful of neat features, with more being added regularly.
    <br />
    <br />
    <a href="http://tiny.cc/qthruz">
       <img src="https://www.svgrepo.com/show/353655/discord-icon.svg",alt=invite, height=100, width=100>
      <br></br>
      <strong>Invite</strong>
    </a>
    <br />
    ---------------------------------------
    <br />
    <a href="#about-the-project"><strong>View Demo</strong></a>
    ·
    <a href="https://github.com/Nekurone/Sakamoto/issues">Report Bug</a>
    ·
    <a href="https://github.com/Nekurone/Sakamoto/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](http://tiny.cc/qthruz)

 A Discord Bot with no particular aim, currently has a handful of neat features, with more being added regularly. Has a **strong** focus on end user UX thanks to Discord's Interactions.

Use `/help` to get started!

<p align="right">(<a href="#top">back to top</a>)</p>




<h2 align="center">Keep an eye on this space for updates!</h2>


<!-- GETTING STARTED -->
## Getting Started
To use the _live_ version of this bot on your server, invite Sakamoto from [This Invite Link](http://tiny.cc/qthruz), If you wish to customise this bot, or contribute to it, you'll need to fork this project, please see below for instructions on installation and running a local version of this bot.

### Prerequisites

**REQUIRES PYTHON 3.9+ TO RUN**

I literally cannot stress this enough.

If you need to update or install Python, go to https://www.python.org/downloads/

## Quickstart


**Install Requirements:**
``` sh
$ git clone https://github.com/Nekurone/Sakamoto.git
$ cd Sakamoto
$ pip3 install -r requirements.txt
```
This _should_ install all requirements.  
Next, we need our Bot's token. [See here for how to get your Bot Token](https://discordpy.readthedocs.io/en/stable/discord.html)
We will place this within secrets.env which sits in `src/core`. (alternatively, use your favourite text editor to do this step)
``` sh
$ cd src
$ nano core/secrets.env
# Remember, Nano is Ctrl+O to save and Ctrl+X to quit
```
The format we're looking for here is `export TOKEN=[YOUR-TOKEN-HERE]`

<!-- USAGE EXAMPLES -->
## Usage

Now, we can run the bot.
``` sh
$ python3 main.py
```

To edit the prefix, go into `core/config.py` and edit `PREFIX = "!"`

`main.py` Has a number of arguments that can be used from the terminal, which are useful for debugging and running the bot. 
### Args
| Arg | Long | Example | Result | Options | Default |
|:--|:--|:--|--|--|--|
|-p|--prefix|--prefix "?"|Bot runs with ? as a prefix, overriding config| Any valid prefix | Whatever is set in `core/config`
|-l|--logging|--logging DEBUG|Sets the level of logging|Options are: CRITICAL, ERROR, WARNING, INFO, and DEBUG | WARNING

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap
### Features 


| Feature | Description             |Started | Finished | Contributors |
|:--------|:------------------------|:------:|:--------:|:------------:|
|Admin    |Owner only commands      |✅      |✅        | [Nekurone](https://github.com/Nekurone)|
|Info     |Information About the Bot|✅      |✅        | [Nekurone](https://github.com/Nekurone)|
|Games    |Small Games to Play      |✅      |❌        | [Nekurone](https://github.com/Nekurone), [timoreo22](https://github.com/timoreo22)|
|Economhy |A currency system :)     |❌      |❌        | N/A | 
|Help     |A Help Interactive Menu  |❌      |❌        | N/A |

See [Here](/../../issues?q=is%3Aissue+is%3Aopen+label%3ACommands%2FCogs++label%3Aenhancement) For all proposed Features.
<!-- If that's not disgusting idk what is -->

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

**Sakamoto uses the black formatter**

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

For any queries pertaining to the code, running the bot, or anything of the sorts, add me on Discord: `Florence#5005`

Alternatively, join my [Programming Discord](https://discord.gg/y4nK5XWs)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [timoreo22](https://github.com/timoreo22) - Tweaks and Features 
* [The Great Folks of Lazy Devs](https://discord.gg/y4nK5XWs) - Emotional Support
* [Nichijou Discord](https://discord.gg/nichijou) - Image Sourcing

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Nekurone/Sakamoto.svg?style=for-the-badge
[contributors-url]: https://github.com/Nekurone/Sakamoto/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Nekurone/Sakamoto.svg?style=for-the-badge
[forks-url]: https://github.com/Nekurone/Sakamoto/network/members
[stars-shield]: https://img.shields.io/github/stars/Nekurone/Sakamoto.svg?style=for-the-badge
[stars-url]: https://github.com/Nekurone/Sakamoto/stargazers
[issues-shield]: https://img.shields.io/github/issues/Nekurone/Sakamoto.svg?style=for-the-badge
[issues-url]: https://github.com/Nekurone/Sakamoto/issues
[license-shield]: https://img.shields.io/github/license/Nekurone/Sakamoto.svg?style=for-the-badge
[license-url]: https://github.com/Nekurone/Sakamoto/blob/master/LICENSE.txt
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[black-url]: https://github.com/psf/black/
[python-shield]: https://img.shields.io/badge/Uses-Python-yellow?style=for-the-badge
[python-url]: https://www.python.org/downloads/

[product-screenshot]: https://i.imgur.com/4vCqkuv.gif
