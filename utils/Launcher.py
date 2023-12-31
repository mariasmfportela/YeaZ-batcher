from segment import segment
import Reader as nd
import neural_network as nn
import skimage

def LaunchPrediction(im, mic_type, pretrained_weights=None):
    """It launches the neural neutwork on the current image and creates 
    an hdf file with the prediction for the time T and corresponding FOV. 
    """
    im = skimage.exposure.equalize_adapthist(im)
    im = im*1.0;	
    pred = nn.prediction(im, mic_type, pretrained_weights)
    return pred

def ThresholdPred(thvalue, pred):
    """Thresholds prediction with value"""
    if thvalue == None:
        thresholdedmask = nn.threshold(pred)
    else:
        thresholdedmask = nn.threshold(pred, thvalue)
    return thresholdedmask

def LaunchInstanceSegmentation(reader, image_type, fov_indices=[0], time_value1=0, time_value2=0, thr_val=None, min_seed_dist=5, path_to_weights=None):
    """
    """
    # cannot have both path_to_weights and image_type supplied
    if (image_type is not None) and (path_to_weights is not None):
        print("image_type and path_to_weights cannot be both supplied.")
        return
    

    # check if correct imaging value
    if (image_type not in ['bf', 'pc']) and (path_to_weights is None):
        print("Wrong imaging type value ('{}')!".format(image_type),
              "imaging type must be either 'bf' or 'pc'")
        return

    # check range_of_frames constraint
    if time_value1 > time_value2 :
        print("Error", 'Invalid Time Constraints')
        return
    
    # displays that the neural network is running
    print('Running the neural network...')
    
    for fov_ind in fov_indices:

        #iterates over the time indices in the range
        for t in range(time_value1, time_value2+1):         
            print('--------- Segmenting field of view:',fov_ind,'Time point:',t)

            #calls the neural network for time t and selected fov
            im = reader.LoadOneImage(t, fov_ind)

            try:
                pred = LaunchPrediction(im, image_type, pretrained_weights=path_to_weights)
            except ValueError:
                print('Error! ',
                      'The neural network weight files could not '
                      'be found. \nMake sure to download them from '
                      'the link in the readme and put them into '
                      'the folder unet, or specify a path to a custom weights file with -w argument.')
                return

            thresh = ThresholdPred(thr_val, pred)
            seg = segment(thresh, pred, min_seed_dist)
            reader.SaveMask(t, fov_ind, seg)
            print('--------- Finished segmenting.')
            
            # apply tracker if wanted and if not at first time
            temp_mask = reader.CellCorrespondence(t, fov_ind)
            reader.SaveMask(t, fov_ind, temp_mask)
            
def launch_nn(image_path, mask_path, image_type, channel = 0, fov = [0], range_of_frames = [0,0], threshold = None, min_seed_dist = 5, path_to_weights = None):
    '''
    Equivalent to "Launch_NN_command_line.py" on one image
    image_type must be either "bf" for brightfield, or "pc" for phase contrast
    '''
    if '.h5' in mask_path:
        mask_path = mask_path.replace('.h5','')

    reader = nd.Reader("", mask_path, image_path, channel)

    LaunchInstanceSegmentation(reader, image_type, fov, range_of_frames[0], range_of_frames[1], threshold, min_seed_dist, path_to_weights)
