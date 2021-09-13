# BaggageAI CV Hiring Assesment

To run the code execute the following command

```
python main.py [path to threat image] [path background image] [path to output] [1 optional, if you want to set image rotation to clockwise]
```

for example

```
python main.py threat_images\BAGGAGE_20170523_085803_80428_D.jpg background_images\S0210209058_20180811232942_L-1_1.jpg "Generated Samples"\4.png
```

## Algoritjm

### 1. Getting the Threat Image

- read the threat image
- Binarize the threat image. In this case, since background is white, we will use the thresholding technique to binarize the threat image.
- Detect the contours of the threat image.
- Get the contour with the largest area. This is the contour of the threat.
- Find the x,y,w,h of the Threat.
- Rotate it using afine transform. Scale image to  $\sqrt{1/2}$ times the size of threat to make sure no part of threat is cut off.
- Get the mask of the threat by once again binarizing the threat image.
- Add mask to the threat image as its alpha channel.

#### For Example

This image gets processed

![Alt text](threat_images\BAGGAGE_20170522_113049_80428_A.jpg "Title")

Into this image

![Alt text](examples\rgba.png "Title")

Note the Transparent Backgroud.

## 2. Getting the Background Image

- read the background image
- Binarize the background image. In this case, since the image background is white, we will use the thresholding technique to binarize the background image.
- Detect the contours of the background image.
- Get the contour with the largest area. This is the contour of the background.
- Select a 2 points randomly from the contour. These will be the opposite points where threat will be inserted.

## 3. Inserting Threat into the Background

- split threat into b,g,r,a channels
- Blur a channel for a smooth transition when two images are combined. Here I used median blur
- get the ROI on the background by using the two points selected in the previous step.
- Apply bitwise not operation in the ROI to remove the pixels where threat is to be inserted.
- Apply bitwise and operation to the r,g,b channels of the threat image to add the threat image to the background at the designated ROI.

Into this image

![Alt text](Generated_Samples\4.png "Sample Output")