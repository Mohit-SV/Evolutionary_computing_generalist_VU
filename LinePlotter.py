import matplotlib.pyplot as plt
import os
from collections import defaultdict
import statistics as sts
import config as C


def generate2inone(first_dict, second_dict, colour='b', label='Mean'):
    x = list(first_dict.keys()) 
    y_first = [sts.mean(mean_or_max) for mean_or_max in first_dict.values()]
    y_second = [sts.mean(mean_or_max) for mean_or_max in second_dict.values()]
    yerr_first = [sts.stdev(mean_or_max) for mean_or_max in first_dict.values()]
    yerr_second = [sts.stdev(mean_or_max) for mean_or_max in second_dict.values()]

    ax1 = plt.subplot(121)
    ax1.set_title("EA 1 (with mutation)")
    ax1.set_ylabel("Fitness", fontsize=11)
    ax1.set_xlabel("Generation", fontsize=11)
    ax1.errorbar(x,y_first,yerr=yerr_first,color=colour,label=label,capsize=3,fmt='-o')
    ax1.set_xlim([-0.5,len(first_dict)-0.5])
    ax1.set_ylim([-50,150])
    ax1.legend(loc='lower center')

    ax2 = plt.subplot(122)
    ax2.set_title("EA 2 (no mutation)")
    ax2.set_ylabel("Fitness", fontsize=11)
    ax2.set_xlabel("Generation", fontsize=11)
    ax2.errorbar(x,y_second,yerr=yerr_second,color=colour,label=label,capsize=3,fmt='-o')
    ax2.set_xlim([-0.5,len(second_dict)-0.5])
    ax2.set_ylim([-50,150])
    ax2.legend(loc='lower center')


def get_max_min_dicts(cfg):
    mean_gen_dict = defaultdict(list)
    max_gen_dict = defaultdict(list)
    directory = cfg.experiment_name+'/runs/'
    for filename in os.listdir(directory):    
        if filename.endswith(".txt"):
            f = open(directory+'/'+filename, 'r')
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip().split(',')
                mean_gen_dict[int(line[0])].append(round(float(line[2]), 2))
                max_gen_dict[int(line[0])].append(round(float(line[1]), 2))
    return mean_gen_dict, max_gen_dict


def generateLinePlot(gen_dict, colour='b', label='Mean'):
    plt.title("Fitnesses vs Generations")
    plt.ylabel("Fitness")
    plt.xlabel("Generation")
    plt.xlim([-0.5,len(gen_dict)-0.5])
    x=list(gen_dict.keys())
    y=[sts.mean(mean_or_max) for mean_or_max in gen_dict.values()]
    yerr=[sts.stdev(mean_or_max) for mean_or_max in gen_dict.values()]
    plt.ylim([-50,150])
    plt.errorbar(x,y,yerr=yerr,color=colour,label=label,capsize=3,fmt='-o')
    plt.legend(loc="lower right")


def generateLinePlots(cfg, out_dir='./'):
    mean_gen_dict = defaultdict(list)
    max_gen_dict = defaultdict(list)
    directory = cfg.experiment_name+'/runs/'
    for filename in os.listdir(directory):    
        if filename.endswith(".txt"):
            f = open(directory+'/'+filename, 'r')
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip().split(',')
                mean_gen_dict[int(line[0])].append(round(float(line[2]), 2))
                max_gen_dict[int(line[0])].append(round(float(line[1]), 2))
                
    generateLinePlot(max_gen_dict, colour='r', label = 'Max')
    generateLinePlot(mean_gen_dict, colour='b', label = 'Mean')
    plt.savefig(f'{cfg.experiment_name}/line_plot.png', bbox_inches='tight')
    plt.close()


def compare_2_eas(cfgs, enemy):
    cfg1, cfg2 = getattr(C, cfgs[0]), getattr(C, cfgs[1])
    ea1_means, ea1_maxs = get_max_min_dicts(cfg1)
    ea2_means, ea2_maxs = get_max_min_dicts(cfg2)
    fig = plt.figure(figsize=(10,4))
    generate2inone(ea1_means, ea2_means, colour='r', label = 'Mean')
    generate2inone(ea1_maxs, ea2_maxs, colour='b', label='Max')
    plt.savefig(enemy+'.png')


compare_2_eas(['group478m', 'group478nm'], 'group478')
compare_2_eas(['group245678m', 'group245678nm'], 'group245678')






