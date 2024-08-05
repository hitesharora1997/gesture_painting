import cv2
import numpy as np
import mediapipe as mp
from collections import deque

class GesturePainting:
    def __init__(self):
        self.white_points = [deque(maxlen=1024)]
        self.green_points = [deque(maxlen=1024)]
        self.red_points = [deque(maxlen=1024)]
        self.black_points = [deque(maxlen=1024)]

        self.white_idx = 0
        self.green_idx = 0
        self.red_idx = 0
        self.black_idx = 0

        self.color_palette = [(255, 255, 255), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
        self.current_color_index = 0

        self.canvas_width = 600
        self.canvas_height = 471
        self.paint_canvas = np.zeros((self.canvas_height, self.canvas_width, 3), dtype=np.uint8) + 255

        self.init_canvas()

        # Initialize mediapipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

    def init_canvas(self):
        self.paint_canvas = cv2.rectangle(self.paint_canvas, (40, 1), (140, 65), (0, 0, 0), 2)
        self.paint_canvas = cv2.rectangle(self.paint_canvas, (160, 1), (255, 65), (255, 255, 255), 2)
        self.paint_canvas = cv2.rectangle(self.paint_canvas, (275, 1), (370, 65), (0, 255, 0), 2)
        self.paint_canvas = cv2.rectangle(self.paint_canvas, (390, 1), (485, 65), (0, 0, 255), 2)
        self.paint_canvas = cv2.rectangle(self.paint_canvas, (505, 1), (600, 65), (0, 0, 0), 2)
        cv2.putText(self.paint_canvas, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paint_canvas, "WHITE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paint_canvas, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paint_canvas, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paint_canvas, "BLACK", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    def select_color(self, x, y):
        if 40 <= x <= 140 and y <= 65:
            self.clear_canvas()
        elif 160 <= x <= 255 and y <= 65:
            self.current_color_index = 0
        elif 275 <= x <= 370 and y <= 65:
            self.current_color_index = 1
        elif 390 <= x <= 485 and y <= 65:
            self.current_color_index = 2
        elif 505 <= x <= 600 and y <= 65:
            self.current_color_index = 3

    def clear_canvas(self):
        self.white_points = [deque(maxlen=1024)]
        self.green_points = [deque(maxlen=1024)]
        self.red_points = [deque(maxlen=1024)]
        self.black_points = [deque(maxlen=1024)]
        self.white_idx = 0
        self.green_idx = 0
        self.red_idx = 0
        self.black_idx = 0
        self.paint_canvas[67:, :, :] = 255

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.canvas_width, self.canvas_height))

        frame = cv2.rectangle(frame, (40, 1), (140, 65), (0, 0, 0), 2)
        frame = cv2.rectangle(frame, (160, 1), (255, 65), (255, 255, 255), 2)
        frame = cv2.rectangle(frame, (275, 1), (370, 65), (0, 255, 0), 2)
        frame = cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), 2)
        frame = cv2.rectangle(frame, (505, 1), (600, 65), (0, 0, 0), 2)
        cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "WHITE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "BLACK", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        result = self.hands.process(frame_rgb)

        if result.multi_hand_landmarks:
            landmarks = []
            for hand_landmarks in result.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    lmx = int(lm.x * self.canvas_width)
                    lmy = int(lm.y * self.canvas_height)
                    landmarks.append([lmx, lmy])

                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            forefinger_pos = (landmarks[8][0], landmarks[8][1])
            finger_tip = forefinger_pos
            dot_radius = 8

            cv2.circle(frame, finger_tip, dot_radius, (0, 255, 0), -1)
            cv2.circle(self.paint_canvas, finger_tip, dot_radius, (0, 255, 0), -1)

            thumb_tip = (landmarks[4][0], landmarks[4][1])

            if (thumb_tip[1] - finger_tip[1] < 30):
                self.white_points.append(deque(maxlen=512))
                self.white_idx += 1
                self.green_points.append(deque(maxlen=512))
                self.green_idx += 1
                self.red_points.append(deque(maxlen=512))
                self.red_idx += 1
                self.black_points.append(deque(maxlen=512))
                self.black_idx += 1

            elif finger_tip[1] <= 65:
                self.select_color(finger_tip[0], finger_tip[1])
            else:
                if self.current_color_index == 0:
                    self.white_points[self.white_idx].appendleft(finger_tip)
                elif self.current_color_index == 1:
                    self.green_points[self.green_idx].appendleft(finger_tip)
                elif self.current_color_index == 2:
                    self.red_points[self.red_idx].appendleft(finger_tip)
                elif self.current_color_index == 3:
                    self.black_points[self.black_idx].appendleft(finger_tip)
        else:
            self.white_points.append(deque(maxlen=512))
            self.white_idx += 1
            self.green_points.append(deque(maxlen=512))
            self.green_idx += 1
            self.red_points.append(deque(maxlen=512))
            self.red_idx += 1
            self.black_points.append(deque(maxlen=512))
            self.black_idx += 1

        point_groups = [self.white_points, self.green_points, self.red_points, self.black_points]
        for i in range(len(point_groups)):
            for j in range(len(point_groups[i])):
                for k in range(1, len(point_groups[i][j])):
                    if point_groups[i][j][k - 1] is None or point_groups[i][j][k] is None:
                        continue
                    pt1 = (int(point_groups[i][j][k - 1][0] * (frame.shape[1] / self.canvas_width)),
                           int(point_groups[i][j][k - 1][1] * (frame.shape[0] / self.canvas_height)))
                    pt2 = (int(point_groups[i][j][k][0] * (frame.shape[1] / self.canvas_width)),
                           int(point_groups[i][j][k][1] * (frame.shape[0] / self.canvas_height)))
                    cv2.line(frame, pt1, pt2, self.color_palette[i], 2)
                    cv2.line(self.paint_canvas, point_groups[i][j][k - 1], point_groups[i][j][k], self.color_palette[i], 2)

        return frame

    def run(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture image.")
                break

            frame = cv2.flip(frame, 1)
            processed_frame = self.process_frame(frame)

            cv2.imshow('Frame', processed_frame)
            cv2.imshow('Paint', self.paint_canvas)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    GesturePainting().run()
