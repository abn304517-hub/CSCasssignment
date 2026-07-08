import cv2
import os


class EyeMaskerApp:

    def __init__(self):
        # Initialize video capture
        self.cap = cv2.VideoCapture(0)

        # Load both Face and Eye Haar Cascades
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )

        # Load the image that will replace the purple dots.
        # __file__ makes sure Star.png is loaded from the same folder as this file,
        # even if the program is started from a different folder.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        star_path = os.path.join(script_dir, "Star.png")
        self.eye_img = cv2.imread(star_path, cv2.IMREAD_UNCHANGED)

        if self.face_cascade.empty() or self.eye_cascade.empty():
            raise IOError("Unable to load one or more cascade classifier XML files.")

        if self.eye_img is None:
            raise IOError("Could not load Star.png. Make sure it is in the same folder as eye_mask.py")

    def run(self):
        print("Eye Masker Started.")
        print("Press 'q' to Quit")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame from camera.")
                break

            # Mirror the frame for a natural feel
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )

            for x, y, w, h in faces:

                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]

                # Detect eyes
                eyes = self.eye_cascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.1,
                    minNeighbors=10,
                    minSize=(15, 15)
                )

                for ex, ey, ew, eh in eyes:

                    # Resize football image to eye size
                    overlay = cv2.resize(self.eye_img, (ew, eh))

                    # Select the exact eye area where the image will be placed
                    eye_area = roi_color[ey:ey+eh, ex:ex+ew]

                    # If the image is grayscale, convert it to BGR color
                    if len(overlay.shape) == 2:
                        overlay = cv2.cvtColor(overlay, cv2.COLOR_GRAY2BGR)

                    # If image has transparency, blend it with the webcam frame
                    if overlay.shape[2] == 4:

                        alpha = overlay[:, :, 3] / 255.0

                        for c in range(3):
                            eye_area[:, :, c] = (
                                alpha * overlay[:, :, c] +
                                (1 - alpha) * eye_area[:, :, c]
                            )

                    # If image has no transparency, place it directly over the eye
                    else:
                        eye_area[:] = overlay[:, :, :3]

            # Display the result
            cv2.imshow("Football Eye Mask", frame)

            # Press q to quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = EyeMaskerApp()
    app.run()