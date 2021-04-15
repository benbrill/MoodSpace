# PIC16B-Project
```
. . .
. . .
. . .
```

# Project Proposal

## Abstract:
In 2-4 sentences, describe what problem the project addresses, and the overall approach you will use to solve that problem.

We want to create a website that looks at scenes of a movie or play and creates a customized soundtrack for that scene based on your own Spotify music tastes.

## Planned Deliverables:
Concisely what you are going to create and what capabilities it will have. Are you making a webapp? A Python package for others to use? Code that creates a novel data set? Etc. Please consider two scenarios:
“Full success.” What will your deliverable be if everything works out for you exactly as you plan?
“Partial success.” What useful deliverable will you be able to offer even if things don’t 100% work out? For example, maybe you aren’t able to get that webapp together, but you can still create a code repository that showcases the machine learning pipeline needed to use to support the app. Have a contingency plan!
## Resources Required:
Access to Spotify API
Access to movie scripts through IMDBs API

## Tools/Skills Required:
We will need access to multiple web APIs–Spotify music data and movie scripts. We will need to manipulate large data sets and perform sentiment analysis to characterize the overall mood of the scene. We will also need to conduct sentiment analysis on Spotify songs in order to determine their 'mood'. As Spotify already collects song features based on their "Acousticness" and "danceability", We would use these features, along with NLP on the song lyrics, to characterize a song's mood.
We will then match the mood score of the song to the scene in the movie to determine if it is consistent. Finally, we will create a stylized webpage to display our findings.
## Risks:
What are two things that could potentially stop you from achieving the full deliverable above? Maybe it turns out that the data doesn’t exist and you need change plan? Or maybe your idea requires more computational power than is available to you? What particular risks might be applicable for your project?
## Ethics:
All projects we undertake involve decisions about whose interests matter; which problems are important; and which tradeoffs are considered acceptable. Take some time to reflect on the potential impacts of your product on its users and the broader world. If you can see potential biases or harms from your work, describe some of the ways in which you will work to mitigate them. Remember that even relatively simple ideas can have unexpected and impactful biases. Here’s a nice introductory video for thinking about these questions, and here’s one that goes into somewhat more detail. Here are some relevant examples:
Will your recipe recommender app privilege the cuisines of some cultures above others? For example, peanut butter and tomato might seem an odd combination in the context of European cuisine, but is common in many traditional dishes of the African diaspora. A similar set of questions applies to recommendation systems related to style or beauty.
What data set will your sentiment analysis be trained on? What languages will be included? Will diverse dialects be included, or only the “standard” version of the target language? Who would be excluded by such a choice, and how will you communicate about your limitations?
Will your facial recognition system work well well on all faces, or will it systematically underperform on certain marginalized subgroups? (see the videos above for examples of this.)
## Tentative Timeline:
Week 2: Data acquisition and prepping pipeline
Week 4: Data analysis: Spotify Sentiment Analysis, Movie Script Sentiment Analysis
Week 6: Full pipeline set up
