"""
Dialect-Specific Arabic Translation Module
Handles translation to specific Arabic dialects with proper prompting
"""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Dialect-specific system prompts for better translation
DIALECT_PROMPTS = {
    "gulf": {
        "name": "Gulf Arabic (Khaleeji)",
        "name_ar": "اللهجة الخليجية",
        "prefix": "ترجم إلى اللهجة الخليجية (السعودية، الإمارات، الكويت): ",
        "markers": ["شلون", "يالله", "إن شاء الله", "ما شاء الله"],
        "example": "كيف حالك؟ → شلونك؟"
    },
    "egyptian": {
        "name": "Egyptian Arabic (Masri)",
        "name_ar": "اللهجة المصرية",
        "prefix": "ترجم إلى اللهجة المصرية: ",
        "markers": ["إزيك", "يعني", "قوي", "خالص"],
        "example": "كيف حالك؟ → إزيك؟"
    },
    "levantine": {
        "name": "Levantine Arabic (Shami)",
        "name_ar": "اللهجة الشامية",
        "prefix": "ترجم إلى اللهجة الشامية (سوريا، لبنان، الأردن، فلسطين): ",
        "markers": ["كيفك", "هلأ", "شو", "ياللا"],
        "example": "كيف حالك؟ → كيفك؟"
    },
    "north_african": {
        "name": "North African Arabic (Maghrebi)",
        "name_ar": "اللهجة المغاربية",
        "prefix": "ترجم إلى اللهجة المغاربية (الجزائر، المغرب، تونس): ",
        "markers": ["كيفاش", "بزاف", "واش", "مزيان"],
        "example": "كيف حالك؟ → كيفاش راك؟"
    },
    "msa": {
        "name": "Modern Standard Arabic",
        "name_ar": "العربية الفصحى",
        "prefix": "ترجم إلى العربية الفصحى: ",
        "markers": [],
        "example": "Standard formal Arabic"
    }
}

class DialectTranslator:
    """Handles dialect-specific Arabic translation"""
    
    def __init__(self, model_name="facebook/nllb-200-distilled-600M", device="cuda"):
        self.device = device
        self.model_name = model_name
        
        # Load model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        
        # For GPT-based post-processing (if needed)
        self.dialect_examples = self._load_dialect_examples()
    
    def _load_dialect_examples(self):
        """Load example phrases for each dialect"""
        return {
            "gulf": {
                "hello": "السلام عليكم → السلام عليكم",
                "how_are_you": "كيف حالك؟ → شلونك؟ / كيفك؟",
                "thank_you": "شكراً → مشكور / يزاك الله خير",
                "goodbye": "وداعاً → يالله بالسلامة",
                "yes": "نعم → إي / إيه",
                "no": "لا → لا",
                "what": "ما / ماذا → شنو / ويش",
                "why": "لماذا → ليش",
                "when": "متى → متى / وين",
            },
            "egyptian": {
                "hello": "السلام عليكم → السلام عليكم",
                "how_are_you": "كيف حالك؟ → إزيك؟ / عامل إيه؟",
                "thank_you": "شكراً → شكراً",
                "goodbye": "وداعاً → سلام / باي باي",
                "yes": "نعم → آه / أيوه",
                "no": "لا → لأ",
                "what": "ما / ماذا → إيه",
                "why": "لماذا → ليه",
                "when": "متى → إمتى",
            },
            "levantine": {
                "hello": "السلام عليكم → مرحبا / السلام عليكم",
                "how_are_you": "كيف حالك؟ → كيفك؟ / شلونك؟",
                "thank_you": "شكراً → شكراً / يسلمو",
                "goodbye": "وداعاً → ياللا بالسلامة",
                "yes": "نعم → آه / إي",
                "no": "لا → لأ",
                "what": "ما / ماذا → شو",
                "why": "لماذا → ليش",
                "when": "متى → إيمتى",
            },
            "north_african": {
                "hello": "السلام عليكم → السلام عليكم / أهلاً",
                "how_are_you": "كيف حالك؟ → كيفاش راك؟ / لاباس؟",
                "thank_you": "شكراً → بارك الله فيك",
                "goodbye": "وداعاً → بسلامة",
                "yes": "نعم → إيه / واه",
                "no": "لا → لا",
                "what": "ما / ماذا → واش / شنوة",
                "why": "لماذا → علاش",
                "when": "متى → وقتاش",
            }
        }
    
    def translate_to_dialect(self, text, source_lang="eng_Latn", dialect="gulf", 
                           progress_callback=None):
        """
        Translate text to specific Arabic dialect
        
        Args:
            text: Source text
            source_lang: NLLB language code for source
            dialect: Target dialect (gulf, egyptian, levantine, north_african, msa)
            progress_callback: Progress reporting function
        
        Returns:
            Translated text in specified dialect
        """
        
        # First: Standard Arabic translation
        if progress_callback:
            progress_callback(60, f"Translating to Arabic ({dialect})...")
        
        # Standard translation to MSA
        msa_translation = self._translate_base(text, source_lang, "arb_Arab")
        
        if dialect == "msa":
            # Return MSA as-is
            return msa_translation
        
        # Second: Dialect adaptation (post-processing)
        if progress_callback:
            progress_callback(63, f"Adapting to {DIALECT_PROMPTS[dialect]['name']}...")
        
        # Apply dialect-specific transformations
        dialect_text = self._adapt_to_dialect(msa_translation, dialect)
        
        if progress_callback:
            progress_callback(65, f"✓ Translation to {dialect} complete")
        
        return dialect_text
    
    def _translate_base(self, text, source_lang, target_lang):
        """Base NLLB translation"""
        
        # Tokenize
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.device)
        
        # Force target language
        forced_bos_token_id = self.tokenizer.lang_code_to_id[target_lang]
        
        # Translate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                forced_bos_token_id=forced_bos_token_id,
                max_length=512,
                num_beams=5
            )
        
        translation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translation
    
    def _adapt_to_dialect(self, msa_text, dialect):
        """
        Adapt MSA text to specific dialect using rule-based transformations
        This is a simple approach - for better results, use dialect-specific models
        """
        
        text = msa_text
        
        if dialect == "gulf":
            # Gulf Arabic transformations
            text = text.replace("كيف حالك", "شلونك")
            text = text.replace("ماذا", "شنو")
            text = text.replace("لماذا", "ليش")
            text = text.replace("أين", "وين")
            text = text.replace("نعم", "إي")
            text = text.replace("شكراً لك", "مشكور")
            text = text.replace("وداعاً", "يالله بالسلامة")
            
        elif dialect == "egyptian":
            # Egyptian Arabic transformations
            text = text.replace("كيف حالك", "إزيك")
            text = text.replace("ماذا", "إيه")
            text = text.replace("لماذا", "ليه")
            text = text.replace("متى", "إمتى")
            text = text.replace("نعم", "أيوه")
            text = text.replace("لا", "لأ")
            text = text.replace("جيد", "كويس")
            text = text.replace("كثير", "قوي")
            
        elif dialect == "levantine":
            # Levantine Arabic transformations
            text = text.replace("كيف حالك", "كيفك")
            text = text.replace("ماذا", "شو")
            text = text.replace("لماذا", "ليش")
            text = text.replace("الآن", "هلأ")
            text = text.replace("نعم", "آه")
            text = text.replace("شكراً", "يسلمو")
            text = text.replace("هيا", "ياللا")
            
        elif dialect == "north_african":
            # North African Arabic transformations
            text = text.replace("كيف حالك", "كيفاش راك")
            text = text.replace("ماذا", "واش")
            text = text.replace("لماذا", "علاش")
            text = text.replace("متى", "وقتاش")
            text = text.replace("كثير", "بزاف")
            text = text.replace("جيد", "مزيان")
            text = text.replace("نعم", "واه")
        
        return text
    
    def translate_with_context(self, text, source_lang, dialect, context_hint=None,
                              progress_callback=None):
        """
        Enhanced translation with contextual hints
        
        Args:
            text: Source text
            source_lang: Source language code
            dialect: Target dialect
            context_hint: Optional context (e.g., "formal", "casual", "technical")
            progress_callback: Progress function
        """
        
        # Add context to improve dialect accuracy
        if context_hint:
            # Adjust translation strategy based on context
            if context_hint == "formal" and dialect != "msa":
                # Use more MSA-influenced dialect
                pass
            elif context_hint == "casual":
                # Use more colloquial forms
                pass
        
        return self.translate_to_dialect(text, source_lang, dialect, progress_callback)
