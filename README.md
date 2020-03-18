# Underwater Buoy Detection
The video sequence you are provided has been captured underwater and shows three buoys of differentcolors, namely yellow, orange and green.  They are almost circular in shape and are distinctly colored.  However,conventional segmentation techniques involving color thresholding will not work well in such an environment,since noise and varying light intensities will render any hard-coded thresholds ineffective.

We will “learn” the color distributions of the buoys and use that learned model tosegment  them.   This  project  requires  you  to  obtain  a  tight  segmentation  of  each  buoy  for  the  entire  videosequence by applying a tight contour (in the respective color of the buoy being segmented) around each buoy by performing color  segmentation  using  Gaussian  Mixture  Models  andExpectation Maximization techniques.

## DataSet Download
The dataset can be downloaded from here : 
https://drive.google.com/open?id=14Wxvr-pg9soeCyU0z0-CqdqsU5Q_O9kw

Place the `detectbuoy.avi` in the same folder as the code.

## How to run code
1. Unzip the folder which has the code, input sequences and the datasets.
2. Each of the following code parts needs to be separately run.
3. Run the codes in the following order
        `python data_preparation.py`
        `python trainGMM.py`
    This stores the parameters needed into the parameters file in .npy format
4. For 1D gaussian run 
        `python part2_3.py`
5. For generating histogram plots run 
        `python part3_1.py`
6. To detect buoy in the video frame run 
        `python part3_3.py`


## Results
https://drive.google.com/open?id=1uycS5PXgsG3qKZLo9W1OhZbHLsdWrR07

  <p align="center">
  <img src="https://github.com/ramaprashanth/perception-for-autonomous-robots/blob/master/Underwater%20Buoy%20Detection/result_1.png">
  </p>
