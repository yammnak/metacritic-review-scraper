# metacritic-review-scraper

This program scrapes all user reviews for a given game for every platform that the game is available on. This program only works on titles that are classified as a game on metacritic and have game in the url e.g. https://www.metacritic.com/game/playstation-5/elden-ring.

To use the program enter the main page for the game when it asks for the metacritic URL, e.g. https://www.metacritic.com/game/playstation-5/elden-ring
Do not input the user reviews page like, https://www.metacritic.com/game/playstation-5/elden-ring/user-reviews, or else it will crash the program.

The program will save the results in a .csv file in the same directory that the program is located.

The columns for the .csv file are:

date: The date the review was posted
game: The title of the game that the review is written for
platform: The platform for the version of the game that the review is written for
metacritic_score: The score that the user gave the game in their review
review: The text of the user review
thumbs_ups: The number of thumbs ups other users gave the review
total_thumbs: The total number of thumbs ups/downs that other users gave the review
