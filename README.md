# MoodSpace - A Spotify Soundtrack Generator by Kendall Arata, Ben Brill, and Michael Ting

## Overview:

MoodSpace is a webapp that not only generates a comprehensive take on a user’s Spotify music tastes, but it also creates a customized playlist of songs to a user’s favorite movie. Using machine learning to pair song and movie moods, our Soundtrack Generator is able to analyze and curate a customized soundtrack playlist to the mood of your favorite film. 

Our app is designed for active Spotify users and movie lovers looking to discover how their music tastes match their favorite movies. To try it, see directions below.

## Directions for serving locally

1. Clone this repository to your local drive
2. Create a virtual enviornment within the repository
    1. install `vituralenv` following [these](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) instructions
    2. Create a virtual enviornment for the repository by running the following in the command line:
    ```
    python3 -m venv env
    ```
3. Download necessary packages to virtual enviornment by running in the command line:
```
pip install -r requirements.txt
```
4. Serve app locally by running the following in the command line
```
python app.py
```

## Limitations

- Number of movie scripts being analyzed is limited
- Creating a custom Spotify playlist involves having acccess to and managing a user's Spotify account, and this could raise privacy issues.
    - Spotify playlist creation functionality is currently disabled. Songs are individually embedded into the website.
- Types of movie scripts are variable and not all aspects (i.e. stage direction) are included in each script
- ML algorithm is trained primarily on English songs
- Soundtrack limited to 3 songs only (for now)
