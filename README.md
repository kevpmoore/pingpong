# Pong
I created Pong because after a [brief] look around, I failed to find a league that worked using a scoring system based on a players relative skill to the other league opponents. So I learnt about the Elo rating system. There are a number of advantages and a few disadvantages to this system that you can read about [here](https://en.wikipedia.org/wiki/Elo_rating_system).. but ultimately it seemed like a fun math thing to work on too and at the time at work we had a special love for table tennis.

Eventually I added historical graph data so you can see players skill progression over a rolling period of 3 weeks as well as a half baked backend for a knockout tournament mode based on seeded league rankings.

It also has slack integration, which would display some cool messages based on who was playing and what league position they were in after a game had been played. Sometimes referencing other league players if the points gap had been closed, with the idea that it would spur people on and get them playing more games.

The front-end is written in D3 + Angular + Bootstrap, while the backend is django with a SQLite database. Its not the cleanest code.. but it works.
