# Generalist-player-agent

<b>Subject:</b> Assignment 2 of Evolutionary Computing Course - Vrije Universiteit Amsterdam, 2021

<b>Task:</b> Evoman (https://www.youtube.com/watch?v=ZqaMjd1E4ZI) is a video game framework inspired on Megaman. The task is to win over multiple enemies in the game with a single model.

To reproduce our results follow the following steps:
1) run pip install -r requirements.txt
2) run python run_experiments.py to run the experiments again
3) run python LinePlotter.py to plot the lines plots 
4) run python Boxplotter.py to plot the box plot

To run a custom experiment :
1) see config.py and define a new config 
2) run  python train_generalist.py --cfg_name <name of the config defined in config.py>
