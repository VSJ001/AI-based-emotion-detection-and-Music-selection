# AI-based Emotion Detection and Music Selection

A multimodal emotion recognition system that detects the user's mood from
**facial expression**, **voice**, or **text input**, then opens a Spotify
playlist or song that matches the detected emotion. Built in Python with
a Tkinter front end.

## How it works

1. The user picks an input modality on the launch screen: **Face**, **Voice**,
   or **Text**.
2. Depending on the choice:
   - **Face**: opens the webcam, runs DeepFace on each frame for emotion
     classification, and overlays the detected emotion on top of an OpenCV
     Haar Cascade face bounding box.
   - **Voice**: presents four reflective questions; for each one the user
     speaks an answer, the speech is transcribed by Google Web Speech API,
     and VADER sentiment analysis returns a compound score per answer.
   - **Text**: presents the same four questions; the user types each answer
     directly. VADER scores each answer's compound sentiment.
3. For voice and text, the four compound scores are averaged. The resulting
   `[-1, +1]` score is bucketed into `happy`, `surprise`, `neutral`, `sad`,
   `disgust`, or `angry`.
4. The "Navigate to Spotify" page offers three actions:
   - **Open playlist**: opens a curated Spotify playlist matching the emotion
   - **Open song**: queries the Spotify API for tracks tagged with the emotion
     and opens a random one in the browser
   - **Play offline songs**: picks a random track from a local `offline_songs/<emotion>/` folder

## Architecture

```
                    main.py
                       |
                       v
                    gui.Gui
        +--------------+--------------+
        |              |              |
       Face          Voice           Text
        |              |              |
        v              v              v
 face_recognition  voice_text_recognition
        |              |              |
        |              | (mic + STT)  | (typed text)
        |              v              v
        |          VADER SentimentIntensityAnalyzer
        |              |              |
        +-------+------+--------------+
                v
           emotion label
                |
                v
            spotify.MySpotify
        (Spotipy + Spotify Web API)
```

| Module                       | Responsibility                                 |
|------------------------------|------------------------------------------------|
| `main.py`                    | Entry point; instantiates and shows the GUI    |
| `gui.py`                     | Tkinter UI flow, glue between the modalities and Spotify |
| `face_recognition.py`        | OpenCV webcam capture, Haar Cascade face detection, DeepFace emotion classification |
| `voice_text_recognition.py`  | `speech_recognition` for microphone capture, VADER for text + voice sentiment |
| `spotify.py`                 | Spotify API client (Spotipy + python-dotenv); playlist routing per emotion |

## Emotion bucketing (voice + text)

The averaged compound score from VADER is mapped as follows:

| Score range          | Emotion   |
|----------------------|-----------|
| score >= 0.5         | happy     |
| 0.05 <= score < 0.5  | surprise  |
| -0.05 < score < 0.05 | neutral   |
| -0.5 < score <= -0.05| sad       |
| -0.75 <= score <= -0.5| disgust  |
| score < -0.75        | angry     |

The face mode uses DeepFace's dominant emotion directly (no bucketing).

## Setup

### 1. Spotify API credentials

Create a Spotify app at https://developer.spotify.com/dashboard and note its
Client ID and Client Secret. Copy `.env.example` to `.env` and fill in:

```env
CLIENT_ID=your_real_client_id
CLIENT_SECRET=your_real_client_secret
USERNAME=your_spotify_username
```

`.env` is gitignored. Never commit real credentials.

### 2. Python dependencies

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# or: source venv/bin/activate # macOS/Linux
pip install -r requirements.txt
```

`PyAudio` may need a system-level install on some platforms (`portaudio19-dev`
on Debian/Ubuntu, or a prebuilt wheel from
https://www.lfd.uci.edu/~gohlke/pythonlibs/ on Windows).

### 3. (Optional) Offline songs

Drop MP3 files into `offline_songs/<emotion>/` for the offline playback path:

```
offline_songs/
  happy/
  sad/
  angry/
  surprise/
  disgust/
  neutral/
```

This folder is gitignored.

## Run

```bash
python main.py
```

A 800x800 Tkinter window will open. Pick a modality and follow the prompts.

## File layout

```
AI-based-emotion-detection-and-Music-selection/
  main.py                                # entry point
  gui.py                                 # Tkinter UI controller
  face_recognition.py                    # webcam + DeepFace + Haar Cascade
  voice_text_recognition.py              # speech_recognition + VADER
  spotify.py                             # Spotify Web API client
  haarcascade_frontalface_default.xml    # OpenCV pretrained face detector
  requirements.txt                       # Python dependencies
  .env.example                           # template for Spotify credentials
  .gitignore
```

## Notes

- The face-recognition path takes a single frame after a 5-second `time.sleep`
  to give the camera time to focus and the user time to settle into the
  frame. DeepFace runs once per session.
- Speech recognition uses Google Web Speech API by default, which requires
  internet access and has a free-tier rate limit. For offline use, swap in
  `recognizer.recognize_sphinx()` (CMU PocketSphinx).
- The `redirect_url` in `spotify.py` is set to `https://google.com/`, which
  works for the simple search/playlist-open use case (browser redirect, no
  callback needed). For OAuth user-scope endpoints you'd need a real
  callback URL registered in the Spotify dashboard.
