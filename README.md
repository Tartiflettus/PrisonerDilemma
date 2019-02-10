# PrisonerDilemma
A 1D cellular automaton to study strategies in the prisoner's dilemma

## Explanations

The neighborhood is of size 4. It does not include the cell itself.
A cell computes what it gain (payoff) by playing the prisoner's dilemma with its neighbors.
A cell will take the state of the one on its neighborhood with the highest payoff.

This evolution function is said to be "Darwinian".

Yellow is for collaborators
Red is for traitors.
The space is toric.

## how to use
You can edit the width, the height (time axis) of the grid.
You can set a collaborator percentage at the start, and hit init.

You can set the temptation percentage to a value between 0 and 100.
0 means traitors are rewarded as much as collaborators.
100 means traiters are rewarded twice as much as collaborators.
