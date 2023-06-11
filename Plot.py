import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
import seaborn as sns
import numpy as np

def barplot_aggregate(df, x_label, y_label, ax, colours, points_alpha=0):
    '''
    Plot dataframe as a barplot, aggregating data from different replicates
    '''
    sns.set(style="white")
    sns.barplot(df, x = x_label, y = y_label, linewidth=2, palette = colours, ax=ax)
    sns.stripplot(df, x = x_label, y = y_label, hue = 'Replicate', jitter = 0.1, size = 2, 
                  dodge = True, legend = None, ax=ax, alpha = points_alpha, linewidth=0.5, edgecolor='black')
    
    dotplot_colours = np.repeat(colours, df['Replicate'].nunique())
    for collection, colour in zip(ax.collections, dotplot_colours):
        collection.set_facecolor(colour)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha='right', rotation_mode='anchor')
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    return 0

def barplot(df, x_label, y_label, ax, colours, points_alpha=0):
    '''
    Plot dataframe as a barplot
    '''
    sns.set(style="white")
    sns.barplot(df, x = x_label, y = y_label, linewidth=2, palette = colours, ax=ax)
    sns.stripplot(df, x = x_label, y = y_label, linewidth = 0.5, edgecolor = 'black', alpha=points_alpha, 
                  jitter = 0.1, size = 2, legend = None, ax=ax)
    
    for collection, colour in zip(ax.collections, colours):
        collection.set_facecolor(colour)
    
    ax.set_xticklabels(ax.get_xticklabels(),rotation=30)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    return 0

def boxplot_aggregate(df, x_label, y_label, ax, colours):
    '''
    Plot dataframe as a boxplot, aggregating data from different replicates
    '''
    sns.boxplot(df, x = x_label, y = y_label, hue = "Replicate", ax = ax, fliersize = 2, saturation = 1)
    
    boxplot_colours = np.repeat(colours, df['Replicate'].nunique())
    box_patches = [p for p in ax.patches if isinstance(p, PathPatch)]
    for patch, colour in zip(box_patches, boxplot_colours):
        patch.set_facecolor(colour)
    
    ax.legend([],[], frameon=False)
    ax.set_xticklabels(ax.get_xticklabels(),rotation=30)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    
    return 0