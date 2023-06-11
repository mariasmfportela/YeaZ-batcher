from matplotlib import cm
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

def DefineColormap(Ncolors):
    """
    Define a new colormap by assigning 10 values of the jet colormap
    such that there are only colors for the values 0-10 and the values >10
    will be treated with a modulo operation (updatedata function)
    """
    jet = cm.get_cmap('jet', Ncolors)
    colors = []
    for i in range(0,Ncolors):
        if i==0 : 
            # set background transparency to 0
            temp = list(jet(i))
            temp[3]= 0.0
            colors.append(tuple(temp))

        else:
            colors.append(jet(i))

    colormap = ListedColormap(colors)
    return colormap

def SaveMask(image, mask, output_path):
    '''
    Overlays mask on original image and saves the result
    NOTE: ensure output_path is a valid image file
    '''
    fig, ax = plt.subplots(1,1)
    ax.axis('off')

    ax.imshow(image, interpolation= 'None', origin = 'upper', cmap = 'gray_r'), 
    ax.imshow((mask%10+1)*(mask != 0), origin = 'upper', interpolation = 'None', alpha = 0.2, cmap = DefineColormap(30))
    
    plt.savefig(output_path, bbox_inches='tight', pad_inches = 0)
    plt.close()