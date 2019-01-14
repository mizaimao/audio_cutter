
# audio_cutter
## Description
This is a web service enabling audio extraction from given intervals in several selected YouTube videos. The program is based on Dash, and the backend is using python3.  
## Scripts
#### app.py
Main execution script.

#### audio_prep.py
Should be used before running app.py. Input audio file and it cuts it into pieces (default: 20000 ms) to speed up processing time and save memory.

#### cutter.py
Backend script having the following functions:
1. generate and return address of requested audio;
2. save quote and generate an record entry to a CSV file, which is displayed on the right side of page (will introduce SQL in future versions).
  
## Future Work
1. Audio processing: reducing noise, channel volume balancing;
2. Audio augmentation: combining other audio files (potentially copyright-free music) to generated audio;
3. Audio looping;
4. Refine input (from one textbox to several);
5. Introduce SQL method to integrate all backend data.

### Far-future work
1. Adding deep learning neural network to automatically add suitable copyright-free music pieces to generated audio.

##### Notes: For video player part, the following items were borrowed from other repos: 
https://github.com/plotly/dash-object-detection
dash_reusable_components.py (in utils)
video_engine (folder)

