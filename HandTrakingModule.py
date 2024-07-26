import cv2
import mediapipe as mp

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.tipIds = [4, 8, 12, 16, 20]

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        
        return img
    
    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []
        
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
                    
        return self.lmList
    
    def fingersUp(self):
        fingers = []
        
        # Thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:  # Check if thumb tip is to the left of the thumb IP joint
            fingers.append(1)  # Thumb is up
        else:
            fingers.append(0)  # Thumb is not up
        
        # Other fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:  # Check if finger tip is above the PIP joint
                fingers.append(1)  # Finger is up
            else:
                fingers.append(0)  # Finger is not up
                
        return fingers

def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break
        
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        
        if lmList:
            fingers = detector.fingersUp()
            print(fingers)  # Print which fingers are up
        
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
