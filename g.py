import cv2
import numpy as np
import mediapipe as mp
from tkinter import Tk, filedialog, messagebox, StringVar
from tkinter import ttk
import os
import threading


class VirtualBackgroundApp:
    def __init__(self, root):
        """
        Initialize the application with the Tkinter root window.
        """
        self.root = root
        self.root.title("🎥 Virtual Background Recorder")
        self.root.geometry("400x320")  # Set the window size
        self.root.resizable(False, False)  # Disable resizing of the window

        # Initialize instance variables
        self.bg_path = ""  # Path for the background media (image or video)
        self.output_path = "output_virtual_background.avi"  # Output video file name
        self.mode_var = StringVar(value="virtual")  # Default mode is "virtual" background

        self.setup_gui()  # Call to set up the GUI components

    def setup_gui(self):
        """
        Setup the graphical user interface with widgets and layout.
        """
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 11))  # Set font style for labels
        style.configure("TButton", font=("Segoe UI", 10))  # Set font style for buttons
        style.configure("TRadiobutton", font=("Segoe UI", 10))  # Set font style for radio buttons

        padding = {"padx": 10, "pady": 5}  # Padding for widgets to make it neat

        # Create and place GUI components
        ttk.Label(self.root, text="Select Background Mode:").grid(row=0, column=0, columnspan=2, **padding)

        # Radiobuttons for selecting background mode
        ttk.Radiobutton(self.root, text="Virtual Background", variable=self.mode_var, value="virtual",
                        command=self.toggle_bg_picker).grid(row=1, column=0, sticky="w", **padding)
        ttk.Radiobutton(self.root, text="Blur Background", variable=self.mode_var, value="blur",
                        command=self.toggle_bg_picker).grid(row=2, column=0, sticky="w", **padding)

        # Button to pick background image or video
        self.bg_button = ttk.Button(self.root, text="Pick Background", command=self.pick_background)
        self.bg_button.grid(row=3, column=0, columnspan=2, **padding)

        # Button to preview the webcam feed
        ttk.Button(self.root, text="Preview Webcam", command=self.preview_webcam).grid(row=4, column=0, columnspan=2, **padding)

        # Button to start recording
        ttk.Button(self.root, text="Start Recording", command=self.start_recording_thread).grid(row=5, column=0,
                                                                                                columnspan=2, **padding)

        # Label to show the current status
        self.status_label = ttk.Label(self.root, text="Status: Waiting...", foreground="blue")
        self.status_label.grid(row=6, column=0, columnspan=2, **padding)

    def toggle_bg_picker(self):
        """
        Toggle background picker button depending on selected background mode.
        Disable background selection if blur mode is selected.
        """
        if self.mode_var.get() == "blur":
            self.bg_button.state(["disabled"])  # Disable background picker for blur mode
            self.bg_path = ""
            self.status_label.config(text="Status: Blur mode selected")
        else:
            self.bg_button.state(["!disabled"])  # Enable background picker for virtual mode
            self.status_label.config(text="Status: Please select a background")

    def pick_background(self):
        """
        Open a file dialog to select a background media (image or video).
        """
        file_path = filedialog.askopenfilename(
            title="Select Background Image or Video",
            filetypes=[("Media files", "*.jpg *.jpeg *.png *.mp4 *.avi *.mov")]
        )
        if file_path:
            self.bg_path = file_path  # Set the background file path
            self.status_label.config(text=f"Selected: {os.path.basename(file_path)}")

    def start_recording_thread(self):
        """
        Start the video recording in a separate thread to avoid blocking the main GUI thread.
        """
        thread = threading.Thread(target=self.record_video)
        thread.start()

    def preview_webcam(self):
        """
        Preview the webcam feed in a separate window. Close the preview by pressing 'q'.
        """
        cap = cv2.VideoCapture(0)  # Open the webcam
        if not cap.isOpened():
            messagebox.showerror("Error", "Webcam not detected.")
            return
        self.status_label.config(text="Status: Previewing webcam. Press 'q' to close.")
        while True:
            ret, frame = cap.read()  # Read a frame from the webcam
            if not ret:
                break
            frame = cv2.flip(frame, 1)  # Flip the frame horizontally
            cv2.imshow("Webcam Preview", frame)  # Show the preview in a window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break  # Exit preview loop on pressing 'q'
        cap.release()
        cv2.destroyAllWindows()  # Close the webcam preview window
        self.status_label.config(text="Status: Webcam preview closed.")

    def record_video(self):
        """
        Record video with virtual or blurred background and save it to output file.
        """
        self.status_label.config(text="Recording started. Press 'q' to stop.")
        cap = cv2.VideoCapture(0)  # Open the webcam for video capture

        # Set FPS and resolution for video recording
        desired_fps = 60  # Adjust FPS as needed
        cap.set(cv2.CAP_PROP_FPS, desired_fps)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set width of the captured frame
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set height of the captured frame

        ret, frame = cap.read()  # Read the first frame from the webcam
        if not ret:
            self.status_label.config(text="Error: Could not read webcam.")
            return

        h, w = frame.shape[:2]  # Get the height and width of the frame

        # Setup output video writer with the desired resolution and FPS
        out = cv2.VideoWriter(self.output_path, cv2.VideoWriter_fourcc(*'XVID'), desired_fps, (w, h))

        # Initialize MediaPipe Selfie Segmentation model
        mp_selfie_segmentation = mp.solutions.selfie_segmentation
        selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

        use_blur = (self.mode_var.get() == "blur")  # Check if blur mode is selected

        if not use_blur:
            if not self.bg_path:
                messagebox.showwarning("No Background", "Please select a background file.")
                cap.release()
                return
            is_video = self.bg_path.lower().endswith(('.mp4', '.avi', '.mov'))  # Check if the background is a video
            if is_video:
                bg_cap = cv2.VideoCapture(self.bg_path)  # Open background video
            else:
                bg_image = cv2.imread(self.bg_path)  # Load background image

        while True:
            ret, frame = cap.read()  # Read a frame from the webcam
            if not ret:
                break

            frame = cv2.flip(frame, 1)  # Flip the frame horizontally
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB
            result = selfie_segmentation.process(rgb)  # Process the frame for segmentation
            mask = np.stack((result.segmentation_mask,) * 3, axis=-1) > 0.6  # Create a mask based on segmentation result

            if use_blur:
                blurred = cv2.GaussianBlur(frame, (55, 55), 0)  # Apply Gaussian blur to the background
                output_frame = np.where(mask, frame, blurred)  # Combine the original frame with the blurred background
            else:
                if is_video:
                    ret_bg, bg_frame = bg_cap.read()  # Read the next frame from the background video
                    if not ret_bg:
                        bg_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop the background video if end is reached
                        ret_bg, bg_frame = bg_cap.read()
                    background = cv2.resize(bg_frame, (w, h))  # Resize the background to match webcam resolution
                else:
                    background = cv2.resize(bg_image, (w, h))  # Resize the background image to match webcam resolution
                output_frame = np.where(mask, frame, background)  # Combine the frame with the background

            # Display the final video with the background effect
            cv2.imshow("Virtual Background", output_frame)
            out.write(cv2.convertScaleAbs(output_frame))  # Write the frame to output video file
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break  # Stop recording on pressing 'q'

        cap.release()
        out.release()  # Release the video writer object
        if not use_blur and 'bg_cap' in locals():
            bg_cap.release()  # Release background video capture if used
        cv2.destroyAllWindows()  # Close all OpenCV windows
        self.status_label.config(text=f"Recording saved to {self.output_path}")  # Update status label with the file path


# Run the app
if __name__ == "__main__":
    root = Tk()  # Create the Tkinter root window
    app = VirtualBackgroundApp(root)  # Initialize the app
    root.mainloop()  # Start the Tkinter main event loop
