import pandas as pd
import numpy as np

import cv2
import os


def score(piece, brand):
    grades = pd.read_csv('./notes.csv')
    average = grades.loc[(grades["Brand"] == brand)]

    average = average[piece].values[0]
    return average