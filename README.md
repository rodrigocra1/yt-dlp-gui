# GUI for yt-dlp

This is a simple Graphical User Interface (GUI) built in Python with the Tkinter library for the powerful command-line tool `yt-dlp`.

## 📜 About This Project

This project was born from a personal need: to simplify the daily task of downloading videos without having to memorize and type commands into a terminal every time.

It is important to note that a significant portion of this code was developed with the assistance of Artificial Intelligence (AI), such as Gemini, to accelerate its creation and explore the tool's capabilities. As a personal use project, the focus was on **immediate, practical functionality** rather than on best practices for large-scale software development.

The goal is to have a tool that "just works" for my daily needs.


<img width="812" height="740" alt="Captura de Tela 2025-07-10 às 11 40 21" src="https://github.com/user-attachments/assets/a907f23c-0a8b-44cd-ba77-9c9053e6db69" />


## ✨ Features

The interface offers simplified control over the main options of `yt-dlp`:

* **Fetch Formats:** Paste a URL and click a button to load all available download options.
* **Quality Selection:** Choose the video resolution (e.g., 1080p, 720p) from a dropdown menu.
* **Codec Selection:** Select the video codec (e.g., h264, vp9) to ensure compatibility.
* **Audio-Only Downloads:** Check a box to download only the audio, which is automatically converted to `.mp3`.
* **Audio Language Selection:** Specify a language code (e.g., `en`, `es`, `pt`) to download the correct audio track when multiple are available.
* **Output Folder Selection:** Easily choose where to save the final file.
* **Visual Feedback:** A progress bar and a status label provide real-time updates on the download progress.

## 🛠️ Prerequisites

Before running the application, ensure you have the following installed and configured on your system:

1.  **Python 3:** The programming language the application is written in.
2.  **yt-dlp:** The core library for downloading. It can be installed via `pip`:
    ```bash
    pip install yt-dlp
    ```
3.  **FFmpeg:** Highly recommended. It is required for merging the separate video and audio files that `yt-dlp` often downloads and for converting audio to `.mp3`.
    * **Important:** `ffmpeg` must be available in your system's PATH for the script to find and use it.

## 🚀 How to Run

1.  **Save the Code:** Save the application code to a file with a `.py` extension (e.g., `gui_app.py`).
2.  **Navigate to the Folder:** Open a terminal or command prompt and navigate to the directory where you saved the file.
3.  **Run the Script:** Use the following command to start the application:
    ```bash
    python gui_app.py
    ```
4.  **Use the Interface:**
    * Paste the desired video URL.
    * Click "Fetch Formats".
    * Adjust the quality, codec, and language options as needed.
    * Select an output folder.
    * Click "Download".
