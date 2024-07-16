import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageOps, ImageDraw
from tkinter import filedialog
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, ttk, scrolledtext
import pyodbc
import speech_recognition as sr
import pyttsx3
import wave
import pyaudio
import randomquestionfull
import random
from datetime import datetime
from threading import Thread
import time
import queue
import threading
import os
import sys
import fitz
import base64
import tkinter.messagebox as messagebox
import tempfile

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_machine_serial():
    if sys.platform == 'win32':
        serial_cmd = 'wmic bios get serialnumber'
    elif sys.platform == 'darwin':
        serial_cmd = 'ioreg -l | grep IOPlatformSerialNumber'
    else:
        raise NotImplementedError("Serial number retrieval not supported on this platform.")
    serial = os.popen(serial_cmd).read().strip().split('\n')[-1].strip()
    encoded = base64.b64encode(serial.encode('utf-8'))
    encoded_text = encoded.decode('utf-8')
    return encoded_text

class SerialVerifier:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Confirmation")
        self.root.configure(bg="white")

        self.frame = tk.Frame(self.root, bg="white")
        self.frame.pack(expand=True, padx=20, pady=20)

        self.entry = tk.Entry(self.frame, width=30)
        self.entry.pack(pady=10)

        self.verify_button = tk.Button(self.frame, text="Check", command=self.verify_code)
        self.verify_button.pack()

    def verify_code(self):
        entered_code = self.entry.get()
        correct_code = get_machine_serial()
        if entered_code == correct_code:
            messagebox.showinfo("DONE", "Login successful!")
            self.root.destroy()
            self.delete_program()
            run_giaodienmodau()
        else:
            messagebox.showerror("ERROR", "CODE ERROR. please try again! ")
            self.entry.delete(0, tk.END)

    def delete_program(self):
        correct_code = get_machine_serial()
        with open("done/text1 - Copy (9).txt", "w") as f:
            f.write(f"verified{correct_code}")

    def run(self):
        self.root.mainloop()

def check_verification():
    if os.path.exists("done/text1 - Copy (9).txt"):
        return True
    return False

def run_verification():
    if not check_verification():
        verifier = SerialVerifier()
        verifier.run()
    else:
        run_giaodienmodau()

# Use system's temp directory for audio files
audio_folder = os.path.join(tempfile.gettempdir(), 'ielts_speaking_audio')
if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)

import subprocess

def open_folder(path):
    try:
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":  # macOS
            subprocess.call(["open", path])
        elif sys.platform.startswith("linux"):  # Linux
            subprocess.call(["xdg-open", path])
        else:
            print(f"Unsupported platform: {sys.platform}")
    except Exception as e:
        print(f"Error opening the folder: {e}")

class giaodienmodau:
    def __init__(self, master):
        self.master = master
        master.title("IELTS Virtual Speaking Room")
        master.geometry("400x460+450+150")
        master.configure(bg="white")

        filelogo = resource_path("pic/image.png")
        filebutton = resource_path("pic/button2.png")

        logo_image = Image.open(filelogo)
        power_icon_image = Image.open(filebutton)

        logo_image = logo_image.resize((317, 107), Image.LANCZOS)
        power_icon_image = power_icon_image.resize((50, 50), Image.LANCZOS)

        self.logo = ImageTk.PhotoImage(logo_image)
        self.power_icon = ImageTk.PhotoImage(power_icon_image)

        self.logo_label = tk.Label(master, image=self.logo, bg="white")
        self.logo_label.pack(pady=10)

        self.title_label = tk.Label(master, text="VIRTUAL SPEAKING ROOM", font=("Times New Roman", 14), bg="white")
        self.title_label.pack(pady=5)

        self.start_button = tk.Button(master, text="Start", command=self.Open_Login, width=20)
        self.start_button.pack(pady=5)

        self.history_button = tk.Button(master, text="History", command=self.Open_History, width=20)
        self.history_button.pack(pady=5)

        self.power_button_label = tk.Button(master, image=self.power_icon, command=sys.exit, bg="grey")
        self.power_button_label.pack(pady=10)

        self.credit_label = tk.Label(master, text="direct by: pcanh & hoag", font=("Brush Script MT", 12), bg="white")
        self.credit_label.place(relx=0.5, rely=0.95, anchor='center')

    def close_main_window(self):
        self.master.destroy()

    def Open_Login(self):
        print("Open Start Window")
        self.close_main_window()
        run_giaodienchuanbi()

    def Open_History(self):
        print("Open History Window")
        open_folder(audio_folder)

    def quit_app(self):
        self.master.destroy()
        run_giaodienketthuc()
        sys.exit()

def run_giaodienmodau():
    root = tk.Tk()
    app = giaodienmodau(root)
    root.mainloop()

class GiaoDienKetThuc:
    def __init__(self, master):
        self.master = master
        master.title("Speaking Test Completion")
        master.geometry("600x730+450+25")
        master.configure(bg='white')

        image_path = resource_path("pic/thu1.png")

        try:
            logo_image = Image.open(image_path)
            logo_image = logo_image.resize((823, 659), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(logo_image)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.photo = None

        if self.photo:
            self.image_label = tk.Label(master, image=self.photo, bg='white')
        else:
            self.image_label = tk.Label(master, text="Image not available", bg='white', font=("Arial", 14))
        self.image_label.pack(pady=5)

        self.button_frame = tk.Frame(master, bg='white')
        self.button_frame.pack(side=tk.BOTTOM, pady=(10, 20))

        self.back_button = tk.Button(self.button_frame, text="Back to Homepage", command=self.back_to_homepage, width=15)
        self.back_button.pack(side=tk.LEFT, padx=10)

        self.test_record_button = tk.Button(self.button_frame, text="Voice Record", command=self.test_record, width=15)
        self.test_record_button.pack(side=tk.LEFT, padx=10)

        self.voice_to_text_button = tk.Button(self.button_frame, text="Tips", command=self.voice_to_text, width=15)
        self.voice_to_text_button.pack(side=tk.LEFT, padx=10)

    def close_main_window(self):
        self.master.destroy()

    def back_to_homepage(self):
        print("Back to Homepage")
        self.master.destroy()
        run_giaodienmodau()

    def test_record(self):
        print("Test Record")
        open_folder(audio_folder)

    def voice_to_text(self):
        pdf_path = resource_path('script/instructor.pdf')
        if os.path.exists(pdf_path):
            self.open_pdf_window(pdf_path)
        else:
            print(f"File {pdf_path} not found.")

    def open_pdf_window(self, file_path):
        new_window = tk.Toplevel(self.master)
        new_window.title('Tips')
        new_window.geometry("600x730+450+25")

        canvas = tk.Canvas(new_window)
        scrollbar = tk.Scrollbar(new_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        pdf_document = fitz.open(file_path)
        image_labels = []

        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            photo = ImageTk.PhotoImage(image=img)
            image_label = tk.Label(scrollable_frame, image=photo)
            image_label.image = photo
            image_label.pack()
            image_labels.append(image_label)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def run_giaodienketthuc():
    root = tk.Tk()
    app = GiaoDienKetThuc(root)
    root.mainloop()

class giaodienchuanbi:
    def __init__(self, master):
        self.master = master
        master.title("ID CONFIRMATION")
        master.geometry("500x460+450+150")
        master.configure(bg='white')

        self.title_label = tk.Label(master, text="ID CONFIRMATION", font=("Arial", 20, "bold"), bg="#D00B0B",
                                    fg="white")
        self.title_label.pack(fill=tk.X)

        self.info_image_frame = tk.Frame(master, bg='white')
        self.info_image_frame.pack(padx=20, pady=10)

        self.info_frame = tk.Frame(self.info_image_frame, bg='white')
        self.info_frame.grid(row=0, column=0, padx=10)

        self.entries = {}
        info_fields = ["Name", "Age", "Nationality"]

        for i, field in enumerate(info_fields):
            label = tk.Label(self.info_frame, text=f"{field}:", font=("Arial", 12), bg="white")
            label.grid(row=i, column=0, sticky='e', pady=5)

            entry = ttk.Entry(self.info_frame, font=("Arial", 12), width=20)
            entry.grid(row=i, column=1, sticky='w', padx=5, pady=5)
            self.entries[field] = entry

        label = tk.Label(self.info_frame, text="Gender:", font=("Arial", 12), bg="white")
        label.grid(row=len(info_fields), column=0, sticky='e', pady=5)

        self.gender_combobox = ttk.Combobox(self.info_frame, values=["Male", "Female"], font=("Arial", 12), width=18,
                                            state="readonly")
        self.gender_combobox.grid(row=len(info_fields), column=1, sticky='w', padx=5, pady=5)
        self.gender_combobox.set("Select Gender")

        pic = resource_path("pic/avatar.png")
        try:
            logo_image = Image.open(pic)
            logo_image = logo_image.resize((125, 143), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(logo_image)

            self.image_label = tk.Label(self.info_image_frame, image=self.photo, bg='white')
            self.image_label.grid(row=0, column=1, padx=10)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image_label = tk.Label(self.info_image_frame, text="No Image Available", bg='white')
            self.image_label.grid(row=0, column=1, padx=10)

        self.start_button = tk.Button(master, text="Start test", font=("Arial", 14), command=self.start_test)
        self.start_button.pack(pady=10)

        self.footer_label = tk.Label(master, text="Don't use headphones to ensure the recording includes the examiner's speech",
                                     font=("Arial", 10), bg="white")
        self.footer_label.place(relx=0.5, rely=0.95, anchor='center')
        self.user_id = None

    def start_test(self):
        self.submit_info()
        self.master.destroy()
        run_giaodienthi()

    def submit_info(self):
        info = {field: entry.get() for field, entry in self.entries.items()}
        info["Gender"] = self.gender_combobox.get()
        print("User Information:", info)
        self.user_id = info

def run_giaodienchuanbi():
    root = tk.Tk()
    app = giaodienchuanbi(root)
    root.mainloop()



class giaodienthi:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Speaking Room")
        self.root.geometry("1200x700")
        self.root.configure(bg='white')

        self.setup_ui()
        self.setup_variables()
        self.setup_audio()

        # Start the main process after 0.5 seconds
        self.root.after(500, self.start_main_process)

        # Start the message processing
        self.process_messages()

    def setup_ui(self):
        # Top red bar with title
        self.top_frame = tk.Frame(self.root, bg='red', height=50)
        self.top_frame.pack(side="top", fill="x")
        self.title_label = tk.Label(self.top_frame, text="VIRTUAL SPEAKING ROOM", fg='white', bg='red',
                                    font=("Times New Roman", 16))
        self.title_label.pack(pady=10)

        # Frame for the image and question display
        self.main_frame = tk.Frame(self.root, bg='white')
        self.main_frame.pack(side="top", fill="both", expand=True, pady=20)

        # Load and place the imported image
        self.load_image()

        # Question display area
        self.question_display = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, width=40, height=15,
                                                          font=("Times New Roman", 14))
        self.question_display.pack(side="right", padx=20, fill="both", expand=True)

        # Bottom text
        self.bottom_text = tk.Label(self.root,
                                    text="Please ensure that your microphone is already turned on and the surrounding area is quiet.",
                                    font=("Times New Roman", 12), bg='white')
        self.bottom_text.pack(side="bottom", fill="x", pady=10)

        # Exit button (initially hidden)
        self.exit_button = ttk.Button(self.root, text="Exit", command=self.show_quit_dialog)
        self.exit_button.place(relx=0.0, rely=0.07, anchor='nw')
        self.exit_button.place_forget()  # Hide the button initially

        # Bind the configure event to update the bottom text position
        self.root.bind('<Configure>', self.on_resize)

    def setup_variables(self):
        self.recording = False
        self.record_start_time = None
        self.questions = []
        self.message_queue = queue.Queue()
        self.audio_filename = None

    def setup_audio(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 120)

    def load_image(self):
        pic = "pic/part12.png"
        try:
            logo_image = Image.open(pic)
            logo_image = logo_image.resize((600, 400), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(logo_image)
            self.image_label = tk.Label(self.main_frame, image=self.photo, bg='white')
            self.image_label.pack(side="left", padx=20)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image_label = tk.Label(self.main_frame, text="No Image Available", bg='white')
            self.image_label.pack(side="left", padx=20)

    def on_resize(self, event):
        # Update the position of the bottom text when the window is resized
        self.bottom_text.pack_forget()
        self.bottom_text.pack(side="bottom", fill="x", pady=10)

    def show_exit_button(self):
        # Simply show the exit button that was created in setup_ui
        self.exit_button.place(relx=0.0, rely=0.07, anchor='nw')

    def show_quit_dialog(self):
        # Create a blurred frame
        self.frame_blur = tk.Frame(self.root, bg='snow')
        self.frame_blur.place(relwidth=1, relheight=1)

        # Create a center frame for the exit button
        frame_center = tk.Frame(self.frame_blur, bg='snow')
        frame_center.place(relx=0.5, rely=0.5, anchor='center', width=200, height=100)

        # Create an exit button in the center frame
        quit_button = tk.Button(frame_center, text="Exit Chat", font=('Helvetica', 16), bg='red', fg='white',
                                command=self.quit_app, padx=15, pady=10)
        quit_button.place(relx=0.5, rely=0.5, anchor='center')

        # Bind click events
        self.frame_blur.bind("<Button-1>", self.close_frame_blur)
        quit_button.bind("<Button-1>", lambda e: self.quit_app())

    def close_frame_blur(self, event):
        self.frame_blur.destroy()

    def stop_propagation(self, event):
        # Stop the event from propagating to the parent widget
        return "break"

    def quit_app(self):
        # Stop recording if in progress
        self.recording = False

        # Stop all running threads
        for thread in threading.enumerate():
            if thread != threading.main_thread():
                thread.join(timeout=1.0)

        # Cancel all pending tasks
        for task in self.root.tk.call('after', 'info'):
            self.root.after_cancel(task)

        # Close the root window
        self.root.quit()
        self.root.destroy()
        run_giaodienketthuc()

        # Exit the program
        sys.exit(0)

    def start_main_process(self):
        # Start the main process in a separate thread
        threading.Thread(target=self.main_process, daemon=True).start()

    def main_process(self):
        # Get questions from randomquestionfull
        self.questions = randomquestionfull.main()

        # Display all questions in the question display area
        self.message_queue.put(('display_all_questions', self.questions))

        now = datetime.now()
        self.recording = True
        self.record_start_time = time.time()

        # Sử dụng audio_folder ở đây
        filename = os.path.join(audio_folder, f"recording_{now.strftime('%Y%m%d_%H%M%S')}.wav")

        record_thread = threading.Thread(target=self.record_audio, args=(filename,))
        record_thread.start()

        try:
            self.part1()
            self.part2()
            self.part3()
        except Exception as e:
            print(f"Error during main process: {str(e)}")

        self.recording = False
        record_thread.join()

        if self.record_start_time and (time.time() - self.record_start_time) > 180:
            self.save_recording()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout=4):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=4)
                return self.recognizer.recognize_google(audio)
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""

    def countdown(self, duration):
        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(0.1)
        return True


    def record_audio(self, output_filename):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2  # Stereo recording
        RATE = 44100

        audio = pyaudio.PyAudio()

        # List available audio devices to find the appropriate input/output
        print("Available audio devices:")
        for i in range(audio.get_device_count()):
            print(audio.get_device_info_by_index(i))

        # Specify input and output device indices (replace with actual device indices)
        input_device_index = 0  # Index of your microphone input device
        output_device_index = 1  # Index of your system audio output device

        stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            input_device_index=input_device_index,  # Set input device
                            frames_per_buffer=CHUNK)

        frames = []

        print("Recording...")
        try:
            while self.recording:
                data = stream.read(CHUNK)
                frames.append(data)
        except KeyboardInterrupt:
            pass
        finally:
            print("Recording stopped.")

            stream.stop_stream()
            stream.close()
            audio.terminate()

            # Save recorded audio to a WAV file
            try:
                wf = wave.open(output_filename, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                print(f"Recorded audio saved as {output_filename}")
            except Exception as e:
                print(f"Error saving audio: {str(e)}")

    def part1(self):
        self.speak(
            "This is the simulated speaking test and I'm your examiner. Can you hear my voice, OK please make sure that your microphone is on and keep your surrounding area silent. You should adjust the volume before the test. Are you ready? OK LET START")
        self.speak("Now, in this first part, I'd like to ask you some questions about yourself")
        exclamations = ["So", "Sounds great", "Ok", "Awesome", "Your idea is good", "Good", "Interesting", "Impressive",
                        "That's wonderful to hear!", "Fascinating", "Wow!", "Amazing!", "Incredible!", "Fantastic!",
                        "Wonderful!", "Excellent!", " ", "Fascinating!", "Interesting!", " ", " ", "Brilliant!", " ",
                        " ", "Impressive!", "Great!", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                        " ", " "]

        start_time = time.time()
        for i, question in enumerate(self.questions[:10]):
            if time.time() - start_time > 300:  # 5 minutes
                break
            if i == 0:
                self.speak(question)
            else:
                self.speak(f"{random.choice(exclamations)}! {question}")
            self.message_queue.put(('highlight_question', question))

            while True:
                response = self.listen()
                if not response:
                    break

        self.speak("That is the end of part 1, now we will turn to part 2.")

    def part2(self):
        original_rate = self.engine.getProperty('rate')

        self.speak("In part 2, I'm going to give you a topic and I'd like you to talk about it for one to two minutes. Before you talk, you'll have one minute to think about what you are going to say. You can make some notes if you wish. Here's some paper and a pencil for making notes, and here's your topic.")
        self.engine.setProperty('rate', 200)
        self.speak(self.questions[10])
        self.engine.setProperty('rate', original_rate)
        self.speak("you will have one minute to prepare, i will tell you when the time is up")
        self.countdown(60)  # 1 minute preparation
        self.speak("All right? Remember, you have one to two minutes for this, so don't worry if I stop you. I'll tell you when the time is up. Can you start speaking now?")

        start_time = time.time()
        speaking_started = False

        while time.time() - start_time < 120:  # Maximum 2 minutes
            if not speaking_started:
                response = self.listen(timeout=5)
                if response:
                    speaking_started = True
                    start_time = time.time()

            if speaking_started:
                response = self.listen(timeout=5)
                if not response:
                    break

        self.speak("OK, the time is up. Let's move to the next part ")

    def part3(self):
        self.message_queue.put(('move_image_left', None))
        self.speak(
            "Now we move on to part 3. You've been talking about a topic, and I'd like to discuss with you some general questions related to it.")
        exclamations = ["So", "Sounds great", "Ok", "Awesome", "Your idea is good", "Good", "Interesting", "Impressive",
                        "That's wonderful to hear!", "Fascinating", "Wow!", "Amazing!", "Incredible!", "Fantastic!",
                        "Wonderful!", "Excellent!", " ", "Fascinating!", "Interesting!", " ", " ", "Brilliant!",
                        "Impressive!", "Great!", " ", " ", " ", " ", " ", " ", " "]

        start_time = time.time()
        for i, question in enumerate(self.questions[11:]):
            if time.time() - start_time > 300:  # 5 minutes
                break
            if i == 0:
                self.speak(question)
            else:
                self.speak(f"{random.choice(exclamations)}! {question}")
            self.message_queue.put(('highlight_question', question))

            silence_duration = 0
            last_response_time = time.time()

            while silence_duration < 4:
                response = self.listen(timeout=2)  # Listen for 2 seconds at a time
                current_time = time.time()

                if response:
                    silence_duration = 0
                    last_response_time = current_time
                    print(f"User response: {response}")
                else:
                    silence_duration = current_time - last_response_time

            print("Moving to next question due to 4 seconds of silence")

        self.speak("That is the end of part 3, and also the end of the speaking test. Thank you")
        self.speak("The speaking test is now complete. Thank you for your time.")
        self.speak("The recording has been saved. You can now exit the test. Goodbye!")

        # Show the exit button after Part 3 is completed
        self.root.after(0, self.show_exit_button)

    def process_messages(self):
        try:
            while True:
                message, data = self.message_queue.get_nowait()

                if message == 'display_all_questions':
                    self.question_display.delete(1.0, tk.END)
                    for i, question in enumerate(data):
                        self.question_display.insert(tk.END, f"{i + 1}. {question}\n\n")

                elif message == 'highlight_question':
                    question = data
                    start_index = self.question_display.search(question, 1.0, tk.END)
                    if start_index:
                        end_index = f"{start_index} + {len(question)}c"
                        self.question_display.tag_add('highlight', start_index, end_index)
                        self.question_display.tag_config('highlight', background='yellow')
                        self.question_display.see(start_index)

                elif message == 'move_image_right':
                    self.image_label.pack_forget()
                    self.image_label.pack(side="right", padx=20)

                elif message == 'move_image_left':
                    self.image_label.pack_forget()
                    self.image_label.pack(side="left", padx=20)

        except queue.Empty:
            pass

        self.root.after(100, self.process_messages)


def run_giaodienthi():
    root = tk.Tk()
    app = giaodienthi(root)
    root.mainloop()


if __name__ == '__main__':
    try:
        run_verification()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
        sys.exit(1)