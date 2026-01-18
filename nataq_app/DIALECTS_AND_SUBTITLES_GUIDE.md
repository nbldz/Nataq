# Nataq v1.3 - Arabic Dialects & Subtitles Guide

## 🆕 New Features

### 1. **Proper Arabic Dialect Support** ✅
- Gulf Arabic (الخليجية)
- Egyptian Arabic (المصرية)
- Levantine Arabic (الشامية)
- North African Arabic (المغاربية - Algerian, Moroccan, Tunisian)
- Modern Standard Arabic (الفصحى)

### 2. **Accessibility Subtitles** ♿
- Burned-in subtitles for deaf/hard-of-hearing users
- Arabic RTL (Right-to-Left) text support
- Automatic timing synchronized with audio
- Professional styling

---

## 🗣️ Arabic Dialects Explained

### **Gulf Arabic (الخليجية)**
**Used in:** Saudi Arabia, UAE, Kuwait, Qatar, Bahrain, Oman

**Example transformations:**
- "How are you?" → شلونك؟ (Shlōnak?)
- "What?" → شنو؟ / ويش؟ (Shinu? / Wēsh?)
- "Why?" → ليش؟ (Lēsh?)
- "Thank you" → مشكور (Mashkūr)

**Best for:** Gulf region content, business in GCC countries

---

### **Egyptian Arabic (المصرية)**
**Used in:** Egypt (most widely understood across Arab world)

**Example transformations:**
- "How are you?" → إزيك؟ (Izzayyak?)
- "What?" → إيه؟ (Ēh?)
- "Why?" → ليه؟ (Lēh?)
- "Yes" → أيوه (Aywa)
- "Very" → قوي (Awi)

**Best for:** Movies, entertainment, casual content

---

### **Levantine Arabic (الشامية)**
**Used in:** Syria, Lebanon, Jordan, Palestine

**Example transformations:**
- "How are you?" → كيفك؟ (Kīfak?)
- "What?" → شو؟ (Shū?)
- "Now" → هلأ (Halla')
- "Let's go" → ياللا (Yalla)
- "Thanks" → يسلمو (Yislamu)

**Best for:** Levant region content, Syrian/Lebanese productions

---

### **North African Arabic (المغاربية)**
**Used in:** Algeria, Morocco, Tunisia, Libya

**Example transformations:**
- "How are you?" → كيفاش راك؟ (Kīfāsh rāk?)
- "What?" → واش؟ (Wāsh?)
- "Why?" → علاش؟ ('Alāsh?)
- "A lot" → بزاف (Bezzāf)
- "Good" → مزيان (Mezyan)

**Best for:** Maghreb region content, Algerian/Moroccan media

---

### **Modern Standard Arabic (الفصحى)**
**Used in:** Formal contexts, news, education, literature

**Characteristics:**
- Formal, classical Arabic
- Used in official documents
- News broadcasts
- Academic content

**Best for:** Professional content, news, formal presentations

---

## ♿ Subtitle Features

### **Why Subtitles?**
- ✅ Accessibility for deaf/hard-of-hearing
- ✅ Better comprehension
- ✅ Language learning
- ✅ Noisy environments
- ✅ Professional presentation

### **Subtitle Characteristics:**
- **Language:** Matches audio (Arabic dialects supported)
- **Timing:** Auto-synchronized with speech
- **Style:** White text, black outline, bottom-center
- **Format:** Burned-in (permanent, not removable)
- **RTL Support:** Proper Arabic right-to-left rendering

### **Subtitle Styling:**
```
Font: Arial
Size: 24pt
Color: White
Outline: Black (2px)
Shadow: 3px
Position: Bottom-center
Margin: 20px from bottom
```

---

## 🎬 Usage Examples

### Example 1: Gulf Arabic with Subtitles
```
Input: English educational video
Settings:
  - Source: English
  - Target: Arabic
  - Dialect: Gulf Arabic (الخليجية)
  - Voice: Male
  - Subtitles: ✅ Enabled

Output: Video with Gulf dialect audio + Gulf dialect subtitles
Perfect for: Saudi/UAE educational content
```

### Example 2: Egyptian Arabic (No Subtitles)
```
Input: English movie
Settings:
  - Source: English
  - Target: Arabic
  - Dialect: Egyptian Arabic (المصرية)
  - Voice: Female
  - Subtitles: ❌ Disabled

Output: Video with Egyptian dialect audio only
Perfect for: Entertainment, casual content
```

### Example 3: Levantine with Accessibility
```
Input: News broadcast
Settings:
  - Source: English
  - Target: Arabic
  - Dialect: Levantine Arabic (الشامية)
  - Voice: Male
  - Subtitles: ✅ Enabled

Output: Accessible video for Syrian/Lebanese audience
Perfect for: News, documentaries for Levant region
```

### Example 4: North African for Algeria
```
Input: Training video
Settings:
  - Source: French
  - Target: Arabic
  - Dialect: North African Arabic (المغاربية)
  - Voice: Male
  - Subtitles: ✅ Enabled

Output: Training video in Algerian dialect
Perfect for: Corporate training in Maghreb
```

---

## 🎯 Dialect Selection Guide

| Content Type | Recommended Dialect | Why |
|--------------|-------------------|-----|
| News/Formal | MSA (الفصحى) | Universal understanding |
| Saudi/GCC Business | Gulf (الخليجية) | Regional authenticity |
| Movies/Entertainment | Egyptian (المصرية) | Widely understood |
| Syrian/Lebanese Content | Levantine (الشامية) | Cultural accuracy |
| Algerian/Moroccan | North African (المغاربية) | Regional relevance |

---

## 📊 Dialect Comparison

**Phrase: "How are you?"**
- MSA: كيف حالك؟ (Kayfa hāluk?)
- Gulf: شلونك؟ (Shlōnak?)
- Egyptian: إزيك؟ (Izzayyak?)
- Levantine: كيفك؟ (Kīfak?)
- North African: كيفاش راك؟ (Kīfāsh rāk?)

**Phrase: "What do you want?"**
- MSA: ماذا تريد؟ (Mādhā turīd?)
- Gulf: شنو تبي؟ (Shinu tibi?)
- Egyptian: عايز إيه؟ ('Āyiz ēh?)
- Levantine: شو بدك؟ (Shū biddak?)
- North African: واش تحب؟ (Wāsh t  ḥebb?)

---

## ⚙️ Technical Details

### Dialect Translation Method
1. **Base translation** to Modern Standard Arabic using NLLB-200
2. **Dialect adaptation** using rule-based transformations
3. **Context-aware** replacements for common phrases
4. **Maintains meaning** while changing expression

### Subtitle Generation Process
1. **Extract timing** from Whisper speech segments
2. **Match translation** to original timing
3. **Create SRT** file with timestamps
4. **Convert to ASS** format (better Arabic support)
5. **Burn into video** using FFmpeg

### Performance Impact
- **Dialect translation:** +10-20 seconds
- **Subtitle generation:** +30-60 seconds
- **Total overhead:** ~1 minute per video

---

## 🔧 Customization Options

### Disable Subtitles
If you don't need accessibility features:
```
In GUI: Uncheck "Add subtitles to video (burned-in)"
Processing time: Saves ~1 minute
```

### Subtitle Styling
To customize subtitle appearance, edit:
```python
# In core/subtitle_generator.py, line ~60
subtitle_style = {
    "font": "Arial",        # Change font
    "font_size": 24,        # Change size
    "primary_color": "&HFFFFFF",  # White text
    # ... modify as needed
}
```

---

## 🎓 Best Practices

### For Educational Content
- **Dialect:** MSA or Gulf (formal)
- **Subtitles:** ✅ Enabled
- **Voice:** Professional male/female
- **Why:** Clear, accessible, professional

### For Entertainment
- **Dialect:** Egyptian (widely understood)
- **Subtitles:** Optional
- **Voice:** Expressive
- **Why:** Natural, engaging

### For Regional Content
- **Dialect:** Match target region
- **Subtitles:** ✅ Enabled for accessibility
- **Voice:** Local preference
- **Why:** Cultural authenticity

### For Multilingual Audiences
- **Dialect:** MSA (neutral)
- **Subtitles:** ✅ Enabled
- **Voice:** Clear, professional
- **Why:** Maximum understanding

---

## ⚠️ Important Notes

### Dialect Limitations
- Transformations are **rule-based**, not perfect
- Works best for **common phrases**
- May not capture all **regional nuances**
- **MSA** is always most accurate for formal content

### Subtitle Considerations
- Subtitles are **permanently burned-in**
- Cannot be turned off by viewer
- May overlap with video content
- Positioned to minimize interference

### Recommendations
1. **Test with short video** first
2. **Review dialect accuracy**
3. **Check subtitle positioning**
4. **Adjust settings** as needed

---

## 🆚 Version Comparison

| Feature | v1.0-1.2 | v1.3 (New) |
|---------|----------|------------|
| Dialect support | MSA only | 5 dialects |
| Dialect accuracy | Generic Arabic | Region-specific |
| Subtitles | ❌ None | ✅ Full support |
| Accessibility | ❌ Limited | ✅ Deaf-friendly |
| RTL text | Partial | ✅ Full support |

---

## 📥 Quick Start

```bash
# 1. Update to v1.3
Download nataq_app_v1.3.zip

# 2. Install (if needed)
cd nataq_app
install_fixed.bat

# 3. Run
python main.py

# 4. Select dialect
Source: English
Target: Arabic
Dialect: Gulf Arabic  # NEW!

# 5. Enable subtitles
☑ Add subtitles to video  # NEW!

# 6. Process
Click "Start Dubbing"
```

---

**Enjoy dialect-accurate translations with full accessibility support!** 🌍♿

---

**Version:** 1.3.0  
**Date:** December 2025  
**Features:** Arabic Dialects + Accessibility Subtitles
