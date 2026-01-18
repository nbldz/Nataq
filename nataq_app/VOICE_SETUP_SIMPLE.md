# ⚠️ IMPORTANT: Pre-trained Voice Setup

## Issue with XTTS v2

The XTTS v2 model **requires voice cloning** - it doesn't have built-in speakers we can select.

This means we need **actual voice samples** to create pre-trained voices.

## 🎯 SIMPLE SOLUTION (3 Options)

### **Option 1: Use Custom Voice Every Time** (Current Working Method)

```
1. Run: python main.py
2. Select: 📁 Custom Voice
3. Upload: your 5-30 sec Arabic audio
4. Process video (takes 8-10 min)
```

**Pros:** Works immediately, no setup  
**Cons:** Slower (8-10 min per video)

---

### **Option 2: Record Your Own Reference Voices** (RECOMMENDED)

```bash
# 1. Record 10-30 seconds of Arabic speech:
#    - Male voice: Have a male friend speak Arabic
#    - Female voice: Have a female friend speak Arabic
#    - Use phone voice recorder or Audacity

# 2. Save as:
#    voices/male_arabic.wav
#    voices/female_arabic.wav

# 3. Use in app - now it's fast!
```

**How to record:**
1. Open Windows Voice Recorder
2. Speak in Arabic for 10-30 seconds (clear, natural)
3. Save as WAV file
4. Copy to `nataq_app/voices/` folder
5. Rename to `male_arabic.wav` or `female_arabic.wav`

**Pros:** Fast processing (2-3 min), personalized voices  
**Cons:** Need to record audio once

---

### **Option 3: Download Sample Voices** (If Available)

If you have access to Arabic voice samples:
1. Download male/female Arabic speech (10-30 sec)
2. Convert to WAV format
3. Place in `voices/` folder
4. Name as `male_arabic.wav` / `female_arabic.wav`

---

## 🎬 Quick Setup (Option 2 - Record Yourself)

### Windows Voice Recorder Method:

```
1. Press Windows key
2. Type "Voice Recorder"
3. Open app
4. Click microphone button
5. Speak in Arabic for 10-20 seconds
   Example: "مرحباً، اسمي أحمد. أنا أتحدث العربية بوضوح..."
6. Stop recording
7. Right-click → Save as → voices/male_arabic.wav
8. Done!
```

### Using Audacity (Better Quality):

```
1. Download Audacity (free): https://www.audacityteam.org/
2. Record audio:
   - File → Record
   - Speak Arabic clearly for 10-30 seconds
   - Click Stop
3. Export:
   - File → Export → Export as WAV
   - Save to: nataq_app/voices/male_arabic.wav
4. Repeat for female voice
```

---

## ✅ After Setup

Once you have voice files in `voices/` folder:

```bash
cd nataq_app
python main.py

# In GUI:
1. Select: 🎙️ Arabic Male Voice  # Uses your recorded voice!
2. Source: English → Target: Arabic
3. Start Dubbing
4. Wait: 2-3 minutes (fast!)
```

---

## 📁 Folder Structure

```
nataq_app/
├── voices/                    # Create this folder
│   ├── male_arabic.wav       # Record male voice (10-30 sec)
│   └── female_arabic.wav     # Record female voice (10-30 sec)
├── main.py
├── core/
└── ...
```

---

## 🎤 Recording Tips

**Good recording:**
- Clear speech
- No background noise
- 10-30 seconds long
- Natural speaking pace
- Arabic language
- Good microphone quality

**What to say:**
- Introduce yourself in Arabic
- Read a short paragraph
- Speak naturally, not robotic
- Use complete sentences

**Example script (Male):**
```
مرحباً، اسمي أحمد. أنا أتحدث اللغة العربية الفصحى بوضوح. 
هذا التسجيل سيُستخدم لإنشاء صوت مدبلج احترافي للفيديوهات.
أستطيع التحدث بطلاقة وبطريقة طبيعية وواضحة.
```

**Example script (Female):**
```
مرحباً، اسمي فاطمة. أتحدث العربية بلهجة واضحة وطبيعية.
سيتم استخدام هذا الصوت في تطبيق الدبلجة الآلية.
أحرص على النطق الصحيح والتحدث بشكل مريح.
```

---

## 🔧 Alternative: Use GTTS (Simple but Lower Quality)

If you can't record voices, you can generate simple ones:

```python
# Save this as: generate_simple_voice.py
from gtts import gTTS
from pathlib import Path

VOICES_DIR = Path("voices")
VOICES_DIR.mkdir(exist_ok=True)

# Male voice (use default gTTS)
text_male = "مرحباً، أنا صوت ذكر عربي. أتحدث العربية بوضوح."
tts = gTTS(text=text_male, lang='ar', slow=False)
tts.save(str(VOICES_DIR / "male_arabic.wav"))

# Female voice (same, but we'll use it as female reference)
text_female = "مرحباً، أنا صوت أنثى عربية. أتحدث العربية بوضوح."
tts = gTTS(text=text_female, lang='ar', slow=False)
tts.save(str(VOICES_DIR / "female_arabic.wav"))

print("✓ Simple voices created!")
```

**Note:** gTTS voices are simpler/robotic but work as reference.

---

## 🆚 Comparison

| Method | Setup Time | Processing Speed | Voice Quality |
|--------|-----------|-----------------|---------------|
| Custom upload | 0 min | 8-10 min/video | Excellent |
| Recorded voices | 5 min once | 2-3 min/video | Excellent |
| gTTS voices | 1 min once | 2-3 min/video | Good |

---

## ✅ Recommended: Record Your Voices

**Best approach:**
1. Spend 5 minutes recording male/female Arabic speech
2. Save in `voices/` folder
3. Use forever with 2-3 min processing

This gives you:
- ✓ Fast processing
- ✓ Good voice quality  
- ✓ Personalized to your preference
- ✓ One-time setup

---

## 📞 Need Help?

If you're stuck, the **easiest solution** is:

**Just use "Custom Voice" option** - it works perfectly, just takes a bit longer!

No setup needed, just upload a 5-30 sec audio each time you process a video.

---

**Summary:** The automatic speaker selection doesn't work with XTTS v2,  
but recording your own reference voices (5 min setup) gives you fast processing forever!
