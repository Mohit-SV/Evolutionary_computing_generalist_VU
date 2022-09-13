Evoman is a video game playing framework inspired on Megaman.

A demo can be found here:  https://www.youtube.com/watch?v=ZqaMjd1E4ZI

To reproduce our results follow the following steps:
1) run pip install -r requirements.txt
2) run python run_experiments.py to run the experiments again
3) run python LinePlotter.py to plot the lines plots 
4) run python Boxplotter.py to plot the box plot

To run a custom experiment :
see config.py and define a new config 
run  python train_specialist.py --cfg_name <name of the config defined in config.py>
