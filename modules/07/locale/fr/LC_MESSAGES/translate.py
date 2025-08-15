import os
import time

import polib
import requests

# --- Configuration ---
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PO_FILE_PATH = "django.po"
TARGET_LANGUAGE = "French"
# You can find more models at https://openrouter.ai/models
MODEL_NAME = "openai/gpt-4.1-mini"


def translate_text(text, target_language):
    """
    Translates a given text to the target language using the OpenRouter API.

    Args:
        text (str): The text to translate.
        target_language (str): The language to translate the text into.

    Returns:
        str: The translated text, or None if an error occurs.
    """
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY environment variable not set.")
        return None

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate the following text to {target_language}. Respond only with the translated text, without any additional explanations or pleasantries. Preserve original formatting, especially for code placeholders like %(...)s.",
                    },
                    {"role": "user", "content": text},
                ],
            },
        )

        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()
        translated_text = data["choices"][0]["message"]["content"].strip()

        return translated_text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the API request: {e}")
        return None
    except KeyError:
        print(f"Unexpected API response format: {response.text}")
        return None


def process_po_file(file_path):
    """
    Reads a .po file, translates untranslated entries, and saves it back.

    Args:
        file_path (str): The path to the .po file.
    """
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return

    print(f"Loading '{file_path}'...")
    po = polib.pofile(file_path)

    untranslated_entries = [e for e in po if not e.msgstr and e.msgid]

    if not untranslated_entries:
        print("No untranslated entries found. Nothing to do.")
        return

    print(
        f"Found {len(untranslated_entries)} untranslated entries. Starting translation..."
    )

    for i, entry in enumerate(untranslated_entries):
        print(f"Translating entry {i + 1}/{len(untranslated_entries)}: '{entry.msgid}'")

        # Add a small delay to avoid hitting API rate limits
        time.sleep(1)

        translated = translate_text(entry.msgid, TARGET_LANGUAGE)

        if translated:
            entry.msgstr = translated
            print(f"  -> Translation: '{translated}'")
        else:
            print("  -> Failed to translate. Skipping.")

    print("\nTranslation process finished. Saving the file...")
    po.save(file_path)
    print(f"Successfully saved the updated translations to '{file_path}'.")


if __name__ == "__main__":
    # Before running, make sure you have a 'django.po' file in the same directory
    # or update the PO_FILE_PATH variable.
    # Also, ensure the OPENROUTER_API_KEY is set as an environment variable.

    process_po_file(PO_FILE_PATH)
