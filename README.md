# Ranking of European teams and leagues using network theory

The code was developed in 2018 as a project in network science and data analysis. Please support it by spreading the news and the link. 

This football ranking is the definitive unbiased team ranking using network science and statistics.

The method ranks teams across leagues. The different strengths of leagues are taken into account automatically by the algorithm. We do not use hidden weights or any other unobjective factors.


Method:

The ranking uses an adapted version of Google's page-rank algorithm. We include all games of the five European top leagues (England, Germany, Spain, Italy, France) plus all their games in the Champions League and Europa League. With that we construct a graph where teams are the nodes of the graph. A win in a game is a directed link from the loser to the winner. Page rank is used to convert into a Markovian network and its steady state gives the respective points for each team. 

What do the points mean? Loosely speaking, positive numbers mean that the team has won more often than lost. Negative numbers mean the team lost more often than won. However, by construction of the page rank algorithm, the strength of the opposite team is important. E.g., a win against a top team counts more than a win against a team at the end of the table. This also implies that the number of games that a team has played is not important. In other words, the method allows to compare teams that have played different number of games (for instance because they do or do not participate in the international leagues.)



For current standings go to 

www.rankofootball.com
