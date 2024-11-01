# Gimp+Python scanned pages pre-OCR processing

This add-on to GIMP image processor allows user to do batch processing of scans done by a photo camera or mobile phone to prepare it for OCR and PDF collating.
The main task is to equalize the lightness and contrast across the page, as the picture may be done in poor illumination conditions and may be partly underexposed.

The Procedure

First, the color image is converted into grayscale to save time and resources for color mode switching and color channel handling. There are five ways in GIMP of how to turn Red, Green, Blue values into one shade of Gray, they produce slightly varying result depending on the source image colors.

The normalization approach is based on a correction mask that averages values of pixels across segments of the image. In the underexposed areas the average will tend to be lower than in well-exposed. Gaussian Blur function does the job of averaging. Size of segment to blur is provided by user and should be based on size of image and letters. Normally you should not see any letters or rows of text, but if you overexpand the blur area, underexposed segments will not get normalized.

The blurred correction mask laying on top of original image is then set to LAYER_MODE_DIVIDE, normalizing the values of the pixels with a local average. Two layers are then merged into one.

Last adjustment is contrast (up) and layers (down), based on user input on the form (default values suggested)
Sharpening is not working in GIMP via Python on my PC for some reason, so I commented it out. You may try your luck.
Resulting files are saved in user-provided folder.

The code is extensively commented, so you can easily experiment with it adding more features.

Paste the python file into the GIMP Plugin folder (see GIMP-Edit-Preferences-Folders-Plugins, e.g. C:\Users\Home\AppData\Roaming\GIMP\2.10\plug-ins), GIMP will register it and show it in GIMP-Filter-Enhance menu.

Menu interface:

![menu_gimp](https://github.com/user-attachments/assets/7d92b629-4ca6-4749-a305-ae4d461ceed0)
