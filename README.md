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
## How the Algorithm works

Spotify has several different metrics it measures for each song on it's API. For instance, if we wanted to see the statistics for the song "Waiting on the World to Change" by John Mayer, we find the following:
```python
[{'danceability': 0.514,
  'energy': 0.73,
  'key': 1,
  'loudness': -5.934,
  'mode': 1,
  'speechiness': 0.0598,
  'acousticness': 0.00146,
  'instrumentalness': 9.54e-05,
  'liveness': 0.0897,
  'valence': 0.334,
  'tempo': 171.005,
  'type': 'audio_features',
  'id': '0VjIjW4GlUZAMYd2vXMi3b',
  'uri': 'spotify:track:0VjIjW4GlUZAMYd2vXMi3b',
  'track_href': 'https://api.spotify.com/v1/tracks/0VjIjW4GlUZAMYd2vXMi3b',
  'analysis_url': 'https://api.spotify.com/v1/audio-analysis/0VjIjW4GlUZAMYd2vXMi3b',
  'duration_ms': 200040,
  'time_signature': 4}]
```
However, movie scenes obviously do not have these same metrics, because they do not have any musicality that can be measured, only dialogue. To bridge the gap between movie and song, we must provide to a model some sort of medium that both movie and songs share. Luckily, both have some form of text. For songs, it is the lyrics, and for movies it is the screenplay text. 

With this in mind, we can now develop an idea of what the inputs and outputs of our model should be. The input of our model should be some sort of text, whether that be lyrics or screenplay. The output should be a given set of Spotify metrics. We can train our model using song lyrics as input variables and their respective Spotify Metrics as target variables. From there, we can apply this model to given screenplays to predict what the Spotify metrics *would* be given the text composition of that scene. Now that we have metrics for both songs and screenplays, we can compare the two to see which songs are most alligned to a selected scene's screenplay. 

### Model Details

We implemented the above model infastructure using a `tensorflow.keras` neural network. Prior to actually inputing the text into the model, it must be vectorized, using the tensorflow `TextVectorization` function, which returns a vector that represents the words contained within a given song or screenplay in a tokenized form. Once this is complete, we can feed this tokenized vector into our neural network. An outline of our model's structure is shown below.
![A depection of our neural network's structure](project\static\assets\model_arch.png)

Let's highlight a couple of key features of this model.

#### Embedding Layer
The embedding layer takes an input of a vector representing a tokenized string and converts it into a vector in $$n$$ dimensional space. We chose $$n = 60$$. This enables our model to visualize where each of our texts might lie in this space, and thus determine connections and patterns between them to output to subsequent layers of our model.

#### Dropout Layer

## Limitations
- Number of movie scripts being analyzed is limited
- Creating a custom Spotify playlist involves having acccess to and managing a user's Spotify account, and this could raise privacy issues.
    - Spotify playlist creation functionality is currently disabled. Songs are individually embedded into the website.
- Types of movie scripts are variable and not all aspects (i.e. stage direction) are included in each script
- ML algorithm is trained primarily on English songs
- Soundtrack limited to 3 songs only (for now)
