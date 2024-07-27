from openai import OpenAI
import random

OpenAI.api_key = 'your-api-key-here'

client = OpenAI()


def determine_max_tokens(length):
    if length == "short":
        return 64
    elif length == "medium":
        return 128
    elif length == "long":
        return 256
    else:
        raise ValueError("Invalid length. Please choose 'short', 'medium', or 'long'.")


def get_random_japanese_word():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Generate a random Japanese kanji."
            }
        ],
        temperature=0.7,
        max_tokens=10,
        top_p=1
    )
    return response.choices[0].message.content


def get_random_genre():
    genres = ["action", "comedy", "drama", "fantasy", "horror", "mystery", "romance", "sci-fi", "thriller"]
    return random.choice(genres)


# Function to generate media sentences
def generate_media_sentences(media_type, genre, japanese_word, length):
    max_tokens = determine_max_tokens(length)

    if not japanese_word:
        japanese_word = get_random_japanese_word()
    if not genre:
        genre = get_random_genre()

    # Construct the system message based on the type of media and genre
    if media_type == "book":
        system_message = f"You are a writer creating a {genre} book. Generate a short story in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "news":
        system_message = f"You are a journalist writing a {genre} news article. Generate a short news segment in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "movie":
        system_message = f"You are a screenwriter writing a {genre} movie. Generate a short dialogue or narration in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "anime":
        system_message = f"You are a scriptwriter creating a {genre} anime. Generate a short dialogue or narration in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "manga":
        system_message = f"You are a mangaka creating a {genre} manga. Generate a short dialogue in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "tv show":
        system_message = f"You are a scriptwriter creating a {genre} TV show. Generate a short dialogue or narration in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "game":
        system_message = f"You are a game writer creating a {genre} RPG game. Generate a short dialogue or narration in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "music":
        system_message = f"You are a songwriter creating a {genre} song. Generate a short song lyric or stanza in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."

    # Call the OpenAI API with the constructed prompt
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_message
            }
        ],
        temperature=0.7,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=2
    )

    japanese_sentence = response.choices[0].message.content

    # Translate the sentence to English
    translation_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"Translate the following Japanese sentence to English: {japanese_sentence}"
            }
        ],
        temperature=0.7,
        max_tokens=256,
        top_p=1
    )

    english_translation = translation_response.choices[0].message.content

    return {
        "sentence": japanese_sentence,
        "translation": english_translation
    }


# Main program
def main(args):
    japanese_word = args.get("japanese_word", "")
    media_type = args.get("media_type", "").lower()
    genre = args.get("genre", "").lower()
    length = args.get("length", "").lower()

    try:
        result = generate_media_sentences(media_type, genre, japanese_word, length)
        return {
            "statusCode": 200,
            "body": result
        }
    except ValueError as e:
        return {
            "statusCode": 400,
            "body": str(e)
        }