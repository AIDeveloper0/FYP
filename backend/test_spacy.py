import spacy

try:
    # Load the model
    nlp = spacy.load("en_core_web_sm")
    print("✅ spaCy model loaded successfully!")
    
    # Test with sample text
    text = "If the user is logged in, show the dashboard. Otherwise, show the login screen."
    doc = nlp(text)
    
    print(f"📊 Processing: {text}")
    print(f"🔍 Found {len(list(doc.sents))} sentences")
    
    for sent in doc.sents:
        print(f"  📝 Sentence: {sent.text}")
        
        for token in sent:
            if token.pos_ == "VERB":
                print(f"    🔹 Verb: {token.text} (lemma: {token.lemma_})")
    
    print("🎉 spaCy is working perfectly!")
    
except OSError as e:
    print(f"❌ Error loading spaCy model: {e}")
    print("💡 Try running: python -m spacy download en_core_web_sm")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")