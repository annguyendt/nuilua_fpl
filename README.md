# 🌋 Núi Lửa FPL Dashboard

Live FPL mini-league dashboard built with Streamlit.

## Files
- `app.py` — the main dashboard app
- `requirements.txt` — Python dependencies
- `.streamlit/config.toml` — dark theme config

## Setup (one-time)

### 1. Create a GitHub account
Go to https://github.com and sign up (free).

### 2. Create a new repository
- Click **New** → name it `nuilua-fpl` → set to **Public** → Create

### 3. Upload these files to GitHub
Upload all files in this folder to your new repo.

### 4. Deploy on Streamlit Community Cloud
- Go to https://share.streamlit.io
- Sign in with your GitHub account
- Click **New app**
- Select your `nuilua-fpl` repo → branch `main` → main file `app.py`
- Click **Deploy**

Your app will be live at:
`https://YOUR-USERNAME-nuilua-fpl-app-XXXX.streamlit.app`

## Updating
The app pulls live data from the FPL API automatically every 5 minutes.
No action needed from you after each gameweek — it updates itself! 🎉
