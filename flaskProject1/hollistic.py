import pandas as pd
import numpy as np
import cv2

import os


import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

# For static images:

def segmentation():
    # import pandas as pd
    import numpy as np
    import cv2

    import os

    import mediapipe as mp
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_holistic = mp.solutions.holistic

    BG_COLOR = (192, 192, 192)  # gray
    MASK_COLOR = (255, 255, 255)  # white

    with mp_holistic.Holistic(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            refine_face_landmarks=True) as holistic:
        #for file in enumerate('./../flaskProject1'):
            image = cv2.imread('./imageToSave.png')
            image_height, image_width, _ = image.shape
            # Convert the BGR image to RGB before processing.
            results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if results.pose_landmarks:
                print(
                    f'RIGHT SHOULDER COORDINATES: ('
                    f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x * image_width}, '
                    f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y * image_height})',
                    f'LEFT SHOULDER COORDINATES: ({results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x * image_width}, '
                    f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y * image_height})'
                    f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x * image_width}, '
                    f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y * image_height})'
                    f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x * image_width}, '
                    f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y * image_height})'
    
                    f'...{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP].x * image_width}'
                )

            annotated_image = image.copy()

            # Body
            x1, y1 = (int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x * image_width),
                      int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y * image_height))
            x2, y2 = (int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x * image_width),
                      int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP].y * image_height))
            color = (0, 255, 0)
            thickness = 2
            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, thickness)
            box_image = image[y1: y1 + (y2 - y1), x1: x1 + (x2 - x1)]
            cv2.imwrite(f'./body.png', box_image)

            # Trousers
            x1, y1 = (int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP].x * image_width),
                      int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP].y * image_height))
            x2, y2 = (int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP].x * image_width),
                      int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE].y * image_height))
            color = (0, 255, 0)
            thickness = 2
            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, thickness)
            box_image = image[y1: y1 + (y2 - y1), x1: x1 + (x2 - x1)]
            cv2.imwrite(f'./trousers.png', box_image)

            # Head
            x1, y1 = (int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].x * image_width),
                      int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].y * image_height))
            x2, y2 = (int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].x * image_width),
                      int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y * image_height))
            color = (0, 255, 0)
            thickness = 2
            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, thickness)
            box_image = image[y1: y1 + (y2 - y1), x1: x1 + (x2 - x1)]
            cv2.imwrite(f'./head.png', box_image)

            # Draw segmentation on the image.
            # To improve segmentation around boundaries, consider applying a joint
            # bilateral filter to "results.segmentation_mask" with "image".
            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
            annotated_image = np.where(condition, annotated_image, bg_image)
            # Draw pose, left and right hands, and face landmarks on the image.
            mp_drawing.draw_landmarks(
                annotated_image,
                results.face_landmarks,
                mp_holistic.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_tesselation_style())
            mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.
                get_default_pose_landmarks_style())

            #cv2.imwrite('./' + str(file) + '.png', annotated_image)
            # Plot pose world landmarks.
            mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_holistic.POSE_CONNECTIONS)