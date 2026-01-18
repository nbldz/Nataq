# Nataq - Pre-trained Voices Setup Guide v1.2

## 🎯 Two-Phase System (IMPORTANT!)

### Phase 1: Generate Voices ONCE ⚡
Run `create_voices.py` to generate male and female Arabic voices (2-3 minutes)

### Phase 2: Use App UNLIMITED Times 🚀
Select pre-trained voices for 3-5x faster processing

---

## 🚀 Quick Start

### Step 1: Generate Voices (ONE TIME ONLY)

```bash
cd nataq_app
venv\Scripts\activate

# Windows (easy):
create_voices.bat

# Or Python:
python create_voices.py
```

**What this does:**
- Loads XTTS v2 model
- Generates male Arabic voice → `voices/male_arabic.wav`
- Generates female Arabic voice → `voices/female_arabic.wav`
- Takes 2-3 minutes total
- **Only do this ONCE!**

### Step 2: Use the Application

```bash
python main.py
```

In the app:
1. Select video
2. Choose "🎙️ Arabic Male Voice" (already generated!)
3. Start dubbing
4. **Wait only 2-3 minutes** instead of 8-10 minutes!

---

## 📊 Why Pre-train Voices?

| Method | Time (2min video) | Setup Required |
|--------|------------------|----------------|
| **Pre-trained voice** | 2-3 min | One-time (3 min) |
| Custom voice upload | 8-10 min | Every time |

**After one-time setup, you save 5-7 minutes per video!**

---

## 🔧 Detailed Instructions

### Phase 1: Voice Generation

Run this command:
```bash
python create_voices.py
```

**You'll see:**
```
==================================================================
              Nataq - Voice Pre-training System
==================================================================
Device: CUDA
Output Directory: C:\...\nataq_app\voices
==================================================================

Generate voices now? (y/n): y

──────────────────────────────────────────────────────────────────
GENERATING MALE VOICE
──────────────────────────────────────────────────────────────────
[Step 1/2] Loading XTTS v2 model...
✓ Model loaded successfully
[Step 2/2] Selecting speaker from 15 available...
✓ Selected speaker #1
[Synthesizing] Generating male voice...
✓ Male voice saved: male_arabic.wav (156 KB)

──────────────────────────────────────────────────────────────────
GENERATING FEMALE VOICE
──────────────────────────────────────────────────────────────────
✓ Female voice saved: female_arabic.wav (162 KB)

✓ SUCCESS! All voices generated.
```

**Voices are now ready to use!**

---

## ✅ Verification

### Check voices exist:
```bash
dir voices
```

Should show:
```
male_arabic.wav     (~150-200 KB)
female_arabic.wav   (~150-200 KB)
```

### Test voice quality:
Play the WAV files with Windows Media Player

---

## 🐛 Troubleshooting

### Error: "Model is multi-speaker but no speaker provided"

**Cause:** You're using the app without generating voices first  
**Fix:**
```bash
python create_voices.py
```

### Error: "Pre-trained male voice not found"

**Fix:**
```bash
python create_voices.py
```

### Incomplete audio in output

**Cause:** Text chunking issue  
**Fix:** Already fixed in v1.2! Update your files.

---

## 📋 Complete Setup Workflow

```bash
# 1. Install application (first time)
cd nataq_app
install_fixed.bat

# 2. Generate voices (ONE TIME)
python create_voices.py

# 3. Run application (every time)
python main.py
```

---

## 💡 Best Practices

1. ✅ **Generate voices once** - Reused automatically
2. ✅ **Use pre-trained for speed** - 3-5x faster
3. ✅ **Custom voice for branding** - When you need specific person
4. ✅ **Keep `voices/` folder** - Don't delete it!

---

**Ready! Now run `python create_voices.py` to generate your voices!**
