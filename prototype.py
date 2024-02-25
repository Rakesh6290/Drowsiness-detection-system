import cv2
import dlib
import winsound
import pyttsx3

# Initialize the pyttsx3 text-to-speech library
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Define a function to speak the given audio
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Define the face detector and landmark predictor
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Threshold for eye aspect ratio to detect eye closure
EAR_THRESHOLD = 0.2

# Number of consecutive frames for blink detection
BLINK_CONSEC_FRAMES = 6

def detect_eyes_closed():
    # Open the webcam for capturing video
    cap = cv2.VideoCapture(0)

    # Variables to track eye closure and blinking
    eye_closed_counter = 0
    blink_counter = 0
    beep_duration = 5000  # milliseconds (duration of the beep sound)

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale for easier processing
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_detector(gray_frame)

        for face in faces:
            # Get the landmarks for the face
            landmarks = landmark_predictor(gray_frame, face)

            # Calculate the aspect ratio of both eyes to detect closure
            left_eye_ratio = eye_aspect_ratio([
                (landmarks.part(36).x, landmarks.part(36).y),
                (landmarks.part(37).x, landmarks.part(37).y),
                (landmarks.part(38).x, landmarks.part(38).y),
                (landmarks.part(39).x, landmarks.part(39).y),
                (landmarks.part(40).x, landmarks.part(40).y),
                (landmarks.part(41).x, landmarks.part(41).y)
            ])

            right_eye_ratio = eye_aspect_ratio([
                (landmarks.part(42).x, landmarks.part(42).y),
                (landmarks.part(43).x, landmarks.part(43).y),
                (landmarks.part(44).x, landmarks.part(44).y),
                (landmarks.part(45).x, landmarks.part(45).y),
                (landmarks.part(46).x, landmarks.part(46).y),
                (landmarks.part(47).x, landmarks.part(47).y)
            ])

            # Calculate the average eye aspect ratio for both eyes
            #eye_avg_ratio = (left_eye_ratio + right_eye_ratio) / 2.0

            # Check for eye closure or blinking
            if (left_eye_ratio < EAR_THRESHOLD) and (right_eye_ratio < EAR_THRESHOLD):
                eye_closed_counter += 1

                # Check for eye blinking
                if eye_closed_counter >= BLINK_CONSEC_FRAMES:
                    blink_counter += 1

                    if blink_counter == 1:
                        print("Blink detected!")
                    elif blink_counter >= 5:
                        print("Drowsiness detected! Wake up!")
                        #speak("Drowsiness detected! Wake up!")
                        # Play an alert sound
                        winsound.Beep(1000, beep_duration)

            else:
                # Reset counters if eyes are open
                eye_closed_counter = 0
                blink_counter = 0

            # Display the status (eyes open or closed) on the video frame
            cv2.putText(frame, f"Eyes Closed: {blink_counter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Show the video frame with the eye status
        cv2.imshow("Eye Closure Detection", frame)

        # Check if the user pressed 'q' to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Function to calculate the eye aspect ratio given the eye landmarks
def eye_aspect_ratio(eye_points):
    # Compute the euclidean distances between the two sets of vertical eye landmarks (x, y)-coordinates
    A = dist(eye_points[1], eye_points[5])
    B = dist(eye_points[2], eye_points[4])

    # Compute the euclidean distance between the horizontal eye landmark (x, y)-coordinates
    C = dist(eye_points[0], eye_points[3])

    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    return ear

# Function to calculate the euclidean distance between two points
def dist(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

if __name__ == "__main__":
    # Call the main function to start eye closure detection
    detect_eyes_closed()
