from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import h5py

from image_loader import load_image
    
def extract_fluo(reader, file_list, channel_list):
    """This is the function that takes as argument the filepath to the xls
    file and writes in the file.
    It iterates over the different channels (or the sheets of the file,
    each channel has one sheet.), and reads the image corresponding
    to the time, field of view and channel index. It reads the already
    existing file and makes a copy in which the data will be written in it.

    The first step of calculating the data is to iterate through each
    cell/segment of the mask (so each cell is a submatrix of one value
    in the matrix of the mask).
    For each of these value /cell, the area is extracted as being
    the number of pixels corresponding to this cell/value. 
    (it is known from the microscope settings how to convert
    the pixel in area).
    The total intensity is just the value of the pixel and it is added over
    all the pixels corresonding to the cell/value.
    The mean is then calculated as being the total intensity divided by
    the number of pixels (which here is equal to the area also).
    With the mean it is then possible to calculate the variance of the 
    signal for one cell/value.

    Then, it is checked if the value of the cell (cell number) already
    exists in the first column, if it already exists it continues to
    find the column corresponding to the time index where the values
    should be written. It sets the flag to True such that it does not
    write the cell as new one and adds it at the end of the column

    If the value is not found in the cell number column (new cell or
    first time writing in the file), the flag is False, thus it adds the 
    cell number at the end of the column.
    
    It returns dataframe with extracted data.

    """
    # List of cell properties
    cell_list = []

    for time_index in range(0, reader.sizet):
        # Test if time has a mask
        file = h5py.File(reader.hdfpath, 'r+')
        time_exist = reader.TestTimeExist(time_index, 0, file)
        file.close()

        if not time_exist:
            continue

        mask = reader.LoadMask(time_index, 0)

        for file, channel in zip(file_list, channel_list):
            # check if channel is in list of nd2 channels
            try:
                channel_ix = reader.channel_names.index(file)
                image = reader.LoadImageChannel(time_index, 0, channel_ix)

            # channel is a file
            except ValueError:
                image = load_image(file, ix=time_index)
            
            for val in np.unique(mask):
                # bg is not cell
                if val == 0:
                    continue

                # Calculate stats
                stats = {'Cell': val,
                         'Time': time_index,
                         'Channel': channel}

                stats = {**stats,
                         **cell_statistics(image, mask == val)}
                
                # disregard small cells (likely errors)
                if stats['Area'] < 30:
                    continue
                
                cell_list.append(stats)
    
    # Use Pandas to output dataframe
    df = pd.DataFrame(cell_list)
    df = df.sort_values(['Cell', 'Time'])
    
    return df

def cell_statistics(image, mask):
    """Calculate statistics about cells. Passing None to image will
    create dictionary to zeros, which allows to extract dictionary keys"""
    if image is not None:
        cell_vals = image[mask]
        area = mask.sum()
        tot_intensity = cell_vals.sum()
        mean = tot_intensity/area if area > 0 else 0
        var = np.var(cell_vals)

        # Center of mass
        y,x = mask.nonzero()
        com_x = np.mean(x)
        com_y = np.mean(y)

        # PCA only works for multiple points
        if area > 1:
            pca = PCA().fit(np.array([x,y]).T)
            pc1_x, pc1_y = pca.components_[0,:]
            angle = np.arctan(pc1_y / pc1_x) / (2*np.pi) * 360
            v1, v2 = pca.explained_variance_

            len_maj = 4*np.sqrt(v1)
            len_min = 4*np.sqrt(v2)
        else:
            angle = 0
            len_maj = 1
            len_min = 1

    else:
        mean = 0
        var = np.nan
        tot_intensity = 0
        com_x = np.nan
        com_y = np.nan
        angle = np.nan
        len_maj = np.nan
        len_min = np.nan

    return {'Area': area,
            'Mean': mean,
            'Variance': var,
            'Total Intensity': tot_intensity,
            'Center of Mass X': com_x,
            'Center of Mass Y': com_y,
            'Angle of Major Axis': angle,
            'Length Major Axis': len_maj,
            'Length Minor Axis': len_min}