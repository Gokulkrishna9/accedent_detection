import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
class VideoPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Accident Detection")
        self.master.geometry("800x600")
        # Create a label for the title
        self.title_label = tk.Label(self.master, text="Accident Detection", font=("TkDefaultFont", 28, "bold"))
        self.title_label.pack()
        # Setting up the video player
        self.cap = None
        self.subtractor = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=20)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.org = (40, 50)
        self.fontScale = 0.8
        self.color = (0, 0, 255)
        self.thickness = 2
        self.res = 1
        self.arcount = 0
        self.count = -1

        self.upload_button = tk.Button(self.master, text="Upload", command=self.upload_video,font=("TkDefaultFont", 12, "bold"))
        self.upload_button.pack(side="left")
        # Setting up the GUI
        self.play_button = tk.Button(self.master, text="Play", command=self.play_video,font=("TkDefaultFont", 12, "bold"))
        self.play_button.pack(side="left")



        self.master.mainloop()

    def upload_video(self):
        file_path = filedialog.askopenfilename()
        self.cap = cv2.VideoCapture(file_path)

    def play_video(self):
        if self.cap is None:
            print("Please upload a video first.")
            return

        while True:
            res, frame = self.cap.read()
            if res:
                mask = self.subtractor.apply(frame)
                contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                flag = 0

                for cnts in contours:
                    (x, y, w, h) = cv2.boundingRect(cnts)
                    if w * h > 1000:
                        if flag == 1:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                        else:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

                    if w * h > 10000:
                        area = w * h
                        self.arcount += 1
                        if self.arcount > 35:
                            flag = 1

                if flag == 1:
                    frame = cv2.putText(frame, "Accident ; ", self.org, self.font, self.fontScale, self.color, self.thickness, cv2.LINE_AA, False)

                cv2.imshow("Accident detection", frame)
                self.count += 1

                if cv2.waitKey(33) & 0xff == 27:
                    break
            else:
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)