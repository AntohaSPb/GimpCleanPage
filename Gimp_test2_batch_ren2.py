#!/usr/bin/env python
# GIMP plugin that clears photos with text pages
# Source - BW or Color image, output - Grayscale image
# Written by Anton Ivanov of PLAVMAYAK.RU team
# Contacts: anton.b.ivanov@gmail.com
# Distributed under an MIT License

from gimpfu import *
import os
import re
import sys


def python_fu_page_cleanse_option_batch (srcPath, tgtPath, fformat, fileLim, mode, bradius, bright, contr, lolev, gamm, higlev, sradius, amount, sthresh, qualjpeg):
    # error tracing
    # sys.stderr = open('C:/python-fu-output.txt','a')
    # sys.stdout = sys.stderr # So that they both go to the same file
    pdb.gimp_message_set_handler(MESSAGE_BOX)
    # get open images for test
    open_images, image_ids = pdb.gimp_image_list()
    # all open images shall be closed before plugin is executed
    if open_images > 0:
        pdb.gimp_message ("Close open Images & Rerun")
    else:
        # list all of the files in source & target directories
        allFileList = os.listdir(srcPath)
        existingList = os.listdir(tgtPath)
        # empty file list arrays
        srcFileList = []
        tgtFileList = []
        # Find all of the jpeg files in the list & make new file names
        slashfformat = "\\" + fformat
        xform = re.compile(slashfformat, re.IGNORECASE)
        for fname in allFileList:
            fnameLow = fname.lower()
            if fnameLow.count(fformat) > 0:
                srcFileList.append(fname)
                tgtFileList.append(xform.sub('.jpg',fname))
            else:
                pdb.gimp_message ("Source files not found")
        # Dictionary - source & target file names
        tgtFileDict = dict(zip(srcFileList, tgtFileList))
        # Loop on jpegs, open each & save as new jpeg
        fileCnt = 0
        for srcFile in srcFileList:
            # increment counter
            fileCnt = fileCnt + 1
            # prepare file names
            tgtFile = os.path.join(tgtPath, tgtFileDict[srcFile])
            srcFile = os.path.join(srcPath, srcFile)
            # load file and select the drawable
            if fformat == ".jpg" or fformat == ".jpeg":
                image = pdb.file_jpeg_load(srcFile, srcFile)    
            else:
                image = pdb.file_tiff_load(srcFile, srcFile)
            drawable = image.active_drawable
            # get the color mode of image 
            pixmode = pdb.gimp_image_base_type (image)
            # if it is a full colour image...
            if pixmode == 0:
                # desaturate with a given mode
                pdb.gimp_desaturate_full (drawable, mode)
            # unsharp mask filter    
            pdb.plug_in_unsharp_mask (image, drawable, sradius, amount, sthresh) 
            # creare correction layer from visible one
            NewLayer = pdb.gimp_layer_new_from_visible (image, image, "BlurLayer")
            # insert corr layer
            pdb.gimp_image_insert_layer (image, NewLayer, None , 1)
            # bring it to front
            pdb.gimp_image_raise_item_to_top (image, NewLayer)
            # apply Gaussian blur that averages more white paper with less black text
            pdb.plug_in_gauss_iir (image, NewLayer, bradius, True, True)
            # set correction layer to DIVIDE mode
            NewLayer.mode = LAYER_MODE_DIVIDE
            # merge layers
            pdb.gimp_image_flatten (image)
            # get the only active layer
            UpdLayer = pdb.gimp_image_get_active_layer (image)
            # take text down and paper up, and then bring them all equally down  
            pdb.gimp_brightness_contrast (UpdLayer, bright, contr)
            # drawable, item corrected, in_lo, in_hi, clamp_in, gamma (0.1-10), out_lo, out_hi, clamp_out
            pdb.gimp_drawable_levels (UpdLayer, 0, lolev, higlev, False, gamm, 0, 1, False)
            # unsharp mask filter    
            # pdb.plug_in_unsharp_mask (image, UpdLayer, sradius, amount, sthresh)            
            # save it
            pdb.file_jpeg_save (image, UpdLayer, tgtFile, tgtFile, qualjpeg, 1, 0, 0, "SCANCLEAN", 0, 0, 0, 0)
            # pdb.gimp_file_save (image, UpdLayer, tgtFile, tgtFile, run_mode=RUN_NONINTERACTIVE)
            # clear image
            pdb.gimp_image_delete(image)
            if fileCnt == fileLim : break
# -------------------------------------------------------------------------------
register(
    "python_fu_page_cleanse_option_batch",
    "Scanned page batch cleansing...",
    "Run page cleanse with options",
    "Anton Ivanov",
    "PLAVMAYAK.RU",
    "2023",
    "Batch cleanse scanned pages",
    "", 
    # image type not declared
    [
        (PF_DIRNAME, "srcPath", "Source Directory: ", "" ),
        (PF_DIRNAME, "tgtPath", "Target Directory: ", "" ),
        (PF_RADIO, "fformat", "Select input format: ", ".jpg",
            (
                 ("JPEG", ".jpeg"),
                 ("JPG", ".jpg"),
                 ("TIFF", ".tif"),
            ),
        ),
        (PF_SLIDER, "fileLim", "Files to Process ", 1, (1, 1000, 1)),
        (PF_RADIO, "mode", "Desauration: Mode ", DESATURATE_VALUE,
            (
                 ("Lightness", DESATURATE_LIGHTNESS),
                 ("Luminosity", DESATURATE_LUMA),
                 ("Average", DESATURATE_AVERAGE),
                 ("Luminance", DESATURATE_LUMINANCE),
                 ("Average", DESATURATE_VALUE),
            ),
        ),
        (PF_SLIDER, "bradius", "Blur: Radius ", 160.0, (10, 300, 5)),
        (PF_SLIDER, "bright", "Brightness: Adjust ", -40.0, ( -90, 90, 1)),
        (PF_SLIDER, "contr", "Contrast: Adjust ", 41.0, ( -90, 90, 1)),
        (PF_SLIDER, "lolev", "Levels: Lows ", 0, ( 0, 1, 0.02)),
        (PF_SLIDER, "gamm", "Levels: Gamma ", 0.3, ( 0.1, 2, 0.02)),
        (PF_SLIDER, "higlev", "Levels: Highs ", 1, ( 0, 1, 0.02)),
        (PF_SLIDER, "sradius", "Sharpen: Radius ", 1.3, (0, 10, 0.1)),
        (PF_SLIDER, "amount", "Sharpen: Amount ", 1.0, (0, 5, 0.1)),
        (PF_SLIDER, "sthresh", "Sharpen: Threshold ", 0, (0, 1, 0.01)),
        (PF_SLIDER, "qualjpeg", "Save: JPEG quality ", 0.9, (0.5, 1, 0.01)),     
    ],
    [],
    python_fu_page_cleanse_option_batch, menu="<Image>/Filters/Enhance")

main()