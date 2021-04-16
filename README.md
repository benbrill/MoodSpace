# PIC16B-Project Proposal
```
X . .
. X .
. . O
```

## Abstract

Often times, people don't like the soundtrack selections in movies. Well we have a solution for that! We want to create a website that looks at scenes of a movie or play and creates a customized soundtrack for that scene based on your own Spotify music tastes.

Intitally, we will offer a select few famous scenes from movies that we conduct sentiment analysis on. From there we will cross reference our results to a user's own music preferences on their Spotify account to generate a unique song for the scence customized to the users preferences.

## Planned Deliverables

For a "fully successful" project, we would like to have a nice looking web app that a user can easily interface with, with a place for a user to log-in to their Spotify account, select a scene for matching, and outputs a song corresponding to the mood of the scene and the user's music taste.

As "reach" goals, we would like to add additional scenes for the user to choose from or provide a space for a user to input their own scene from a movie for sentiment analysis and song matching. In addition, some sort of mechanism to overlay the user's song choice over the movie scene of their choosing (probably one of our predefined scenes) so they can see their custom soundtrack in action.

A "partially successful" project should still hold the original intent of the project intact: to generate a custom song choice for a movie scence. However, it may not have a full web-app, front-end deployment and may just run as a python script.

It is also important to note that our sentiment analysis might not provide fruitful results, thus requiring us to pivot our project objectives. Luckily, the Spotify API has many potential applications and uses that we can exploit to successfully pivot our projects focus

## Resources Required

We will need access to Spotify API through a Spotify developer account, access to movie scripts, establish a connection to a web server (for our purposes, we will be using Heroku), and access song lyrics through Genius Lyrics (Access to Genius API for song lyrics).

The packages we will need are:

- flask_oauthlib (to authenticate user account)
- gunicorn (web server)
- spotipy (our main connection to the Spotify API)
- Flask (the web app)
- Flask-Session
- beautifulsoup4 (for parsing lyrics)
- python-dotenv~=0.15.0

This github repository will allow us to parse scripts provided at these script sources:

- IMSDb
- Dailyscript
- Awesomefilm
- Weeklyscript
- Scriptsavanat
- Screenplays online
- Scripts for you

The script for parsing the movie scripts come from this paper: Linguistic analysis of differences in portrayal of movie characters, in: Proceedings of Association for Computational Linguistics, Vancouver, Canada, 2017 and the code can be found here:

[Script Parser](https://github.com/usc-sail/mica-text-script-parser)


## Tools/Skills Required

We will need access to multiple web APIs-Spotify music data and movie scripts. We will need to manipulate large data sets and perform sentiment analysis to characterize the overall mood of the scene. We will also need to conduct sentiment analysis on Spotify songs in order to determine their 'mood'. As Spotify already collects song features based on their "Acousticness" and "danceability", We would use these features, along with NLP on the song lyrics, to characterize a song's mood.

We will then match the mood score of the song to the scene in the movie to determine if it is consistent. Finally, we will create a stylized webpage to display our findings.

## Risks

What are two things that could potentially stop you from achieving the full deliverable above? Maybe it turns out that the data doesn't exist and you need change plan? Or maybe your idea requires more computational power than is available to you? What particular risks might be applicable for your project?

With any machine learning pipeline, there's always the risk that whatever model we try to implement will just end up not being very effective at trying to predict what we want. In particular, we need to make sure that we have the flexibility to re-evaluate after our exploratory data analysis where we attempt to analyze sentiment of movie scripts and put that together with the Spotify songs.

We

## Ethics

All projects we undertake involve decisions about whose interests matter; which problems are important; and which tradeoffs are considered acceptable. Take some time to reflect on the potential impacts of your product on its users and the broader world. If you can see potential biases or harms from your work, describe some of the ways in which you will work to mitigate them. Remember that even relatively simple ideas can have unexpected and impactful biases. Here's a nice introductory video for thinking about these questions, and here's one that goes into somewhat more detail. Here are some relevant examples:

Will your recipe recommender app privilege the cuisines of some cultures above others? For example, peanut butter and tomato might seem an odd combination in the context of European cuisine, but is common in many traditional dishes of the African diaspora. A similar set of questions applies to recommendation systems related to style or beauty.

What data set will your sentiment analysis be trained on? What languages will be included? Will diverse dialects be included, or only the "standard" version of the target language? Who would be excluded by such a choice, and how will you communicate about your limitations?

Will your facial recognition system work well well on all faces, or will it systematically underperform on certain marginalized subgroups? (see the videos above for examples of this.)

Though this project may seem innocent on the surface (what could go wrong with matching songs to famous movie scences?), there are several ethical challenges we may encounter and seek to overcome. 

We will have to utilize natural language processing in order to parse through noteable movie scences and obtain a general sentiment on that scene. We will likely train this sentiment analysis on English at first, particularly a western diallect common in many Hollywood produced films. However, doing this would ommit films primarily shot in a language other than English, for instance, Bollywood films which rely heavily on their musical scores and soundtracks. The intention behind this is not to willingly ommit foriegn film scences fro our project, but to first train our model on a language we are most familiar with -- English -- to first see that it actually works and then hopefully apply our methods to work on films in other languages.

Our project will initially only be of use to users who have a Spotify account. Though Spotify offers both a premium and free version of their music library, we acknowledge that not all users may have the resources to have access to make a Spotify account and thus would not be able to use our project. In addition, we also realize that users who pay for a premium Spotify account might get more intuitive and useful results than those that do not, as these users are likely to use the streaming service more often and to build a larger pile of data on the API from which we can access. In order to solve these problems in the future, we hope to add more music services and perhaps a method to input your playlists or music tastes for our a project to work on. 

## Tentative Timeline

Week 2: Data acquisition and prepping pipeline

Week 4: Data analysis: Spotify Sentiment Analysis, Movie Script Sentiment Analysis. Work within a local Jupyter notebook as a proof-of-concept/exploratory data analysis. See how effective a model can be for our idea, and evaluate

Week 6: Full pipeline set up

Week 8: How to mesh the results from the machine learning pipeline with user input in the frontend?
