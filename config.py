from dataclasses import dataclass, field
from typing import List
@dataclass
class config():
    #all parameters here
    experiment_name: str
    enemy_id: List[int]
    run: int = 10 
    ngens: int = 15
    n_hidden_neurons: int = 10
    viz_game: bool = True 
    npop: int = 20
    cxpb: float = 0.6
    mutpb: float = 0.2
    ind_mutpb: float = 0.3
    mutation_step: float = 1

#final configs
group478m = config(experiment_name='4_7_8_0.2m', enemy_id=[4,7,8], run=10, 
                      ngens=50, npop=40, 
                      cxpb=0.9, mutpb=0.2)

group478nm = config(experiment_name='4_7_8_0m', enemy_id=[4,7,8], run=10, 
                      ngens=50, npop=40, 
                      cxpb=0.9, mutpb=0)

group245678m = config(experiment_name='group245678_mutpb0.2_npop40_ngens50', 
                      enemy_id=[2,4,5,6,7,8], run=10, 
                      npop=40, ngens=50, 
                      cxpb=0.9, mutpb=0.2)
group245678nm = config(experiment_name='2_4_5_6_7_8_0m', 
                      enemy_id=[2,4,5,6,7,8], run=10, 
                      npop=40, ngens=50, 
                      cxpb=0.9, mutpb=0.2)