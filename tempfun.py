from __future__ import print_function
import logging
import SimpleITK as sitk
import radiomics
from radiomics import featureextractor
import cv2
import numpy as np 
import cv2
import tocsv
import time
import warnings


tocsv.write2csv(3202,120)