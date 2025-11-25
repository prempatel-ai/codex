import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def translate_dynamic_text(text, target_language):
    """
    Uses Groq LLM to translate dynamic content into target language.
    Skip translation if target_language == English.
    """
    if not text or target_language == "English":
        return text

    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return text

        client = Groq(api_key=api_key)
        
        prompt = f"""
        Translate the following text into {target_language}.
        Keep all emojis, markdown formatting, and numbers exactly as they are.
        Do not add any introductory or concluding remarks.
        Just provide the direct translation.
        
        Text to translate:
        {text}
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a precise translator. Translate the text exactly, preserving formatting and emojis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        translated_text = completion.choices[0].message.content.strip()
        
        # Remove quotes if the model added them
        if translated_text.startswith('"') and translated_text.endswith('"'):
            translated_text = translated_text[1:-1]
            
        return translated_text

    except Exception as e:
        print(f"Translation error: {e}")
        return text
