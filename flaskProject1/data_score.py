import pandas as pd
import numpy as np

import cv2
import os


def score(piece, brand):
    grades = pd.read_csv('./notes.csv')
    average = grades[(grades["Brand"] == brand)]
    average = average[piece]
    return (piece, brand, average)