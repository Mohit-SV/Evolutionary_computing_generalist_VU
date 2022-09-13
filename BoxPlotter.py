import sys
sys.path.insert(0, 'evoman')
from environment import Environment
from child_controller import player_controller

import os
import numpy as np
import matplotlib.pyplot as plt
import config as C

os.environ["SDL_VIDEODRIVER"] = "dummy"

def get_run_number(filename):
    return int(filename.split('.')[0].split('_')[-1][-1])


def write_dict_of_lists_to_file(cfg_object, name, dict_of_lists):
    f = open(cfg_object.experiment_name+'/'+'table_'+name+'.txt', 'w')
    for run_no, per_enemy_scores in dict_of_lists.items():
        line = str(run_no)+','+','.join(map(str, per_enemy_scores))
        f.write(line+'\n')
    f.close()
         

def generateBoxPlot(cfg, my_dict):
    plt.title("Box Plot: Individual Gains of the EAs")
    plt.ylabel("Individual Gain")
    plt.xlabel("Evolutionary Algorithm")
    plt.boxplot(my_dict.values())
    plt.xticks([x for x in range(1,len(my_dict)+1)], my_dict.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.4)
    plt.savefig(cfg.experiment_name+'/'+'box_plot.png')
    plt.close()
    
def get_box_plot_values(cfg_object):
    
    if not os.path.exists(cfg_object.experiment_name):
        os.makedirs(cfg_object.experiment_name)

    directory = cfg_object.experiment_name+'/'+'best/'

    per_run_playerlife_metrics = {}
    per_run_gain_metrics = {}
    per_run_enemylife_metrics = {}

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            bsol = np.loadtxt(filepath)
            print( f'\n RUNNING SAVED BEST SOLUTION 5 TIMES FOR {filepath}\n')
            gains_per_enemy = []
            player_life_per_enemy = []
            enemy_life_per_enemy = []
            for id in range(1,9):
                # initializes simulation in individual evolution mode, for single static enemy.
                env = Environment(experiment_name=cfg_object.experiment_name,
                    enemies=[id],
                    playermode="ai",
                    player_controller=player_controller(cfg_object.n_hidden_neurons),
                    enemymode="static",
                    level=2,
                    speed="fastest",
                    randomini='yes')
            
                gain = []
                player_life = []
                enemy_life = []
                for test in range(1,6):
                    #Test this specific individiual 5 times
                    f,p,e,_ = env.play(np.array(bsol))
                    gain.append(p-e)
                    player_life.append(p)
                    enemy_life.append(e)
                
                avg_gain = round(float(sum(gain) / len(gain)), 2)
                avg_player_life = round(float(sum(player_life) / len(player_life)), 2)
                avg_enemy_life = round(float(sum(enemy_life) / len(enemy_life)), 2)


                gains_per_enemy.append(avg_gain)
                player_life_per_enemy.append(avg_player_life)
                enemy_life_per_enemy.append(avg_enemy_life)
                
        
        #Add RUN number to mean fitness dict
        run_no = get_run_number(filename)

        per_run_gain_metrics[run_no] = gains_per_enemy
        per_run_playerlife_metrics[run_no] = player_life_per_enemy
        per_run_enemylife_metrics[run_no] = enemy_life_per_enemy
        
    write_dict_of_lists_to_file(cfg_object, 'gains', per_run_gain_metrics)
    write_dict_of_lists_to_file(cfg_object, 'playerlife', per_run_playerlife_metrics)
    write_dict_of_lists_to_file(cfg_object, 'enemylife', per_run_enemylife_metrics)
    return per_run_playerlife_metrics, per_run_enemylife_metrics, per_run_gain_metrics

    
if __name__ == "__main__":
    cfg_gains_dict = {}
    cfg_names = ['group478m',
                 'group478nm',
                 'group245678m',
                 'group245678nm'] 

    
    for cfg in cfg_names:
        cfg_object = getattr(C, cfg)
        
        best_run_gain_dict = get_box_plot_values(cfg_object)
        per_run_gain_metrics= np.array(list(best_run_gain_dict[2].values()))
        per_run_gain_metrics = per_run_gain_metrics.T
        per_run_gain_metrics = {idx+1:list(row) for idx, row in enumerate(per_run_gain_metrics)} 
        generateBoxPlot(cfg_object, per_run_gain_metrics)



