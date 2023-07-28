from collections import Counter

def combine_transcripts(transcripts):
    # Preprocess each transcript to remove leading and trailing whitespaces
    transcripts = [transcript.strip() for transcript in transcripts]

    # Find word frequencies across all transcripts
    word_frequencies = Counter()
    for transcript in transcripts:
        word_frequencies.update(transcript.split())

    # Find segments that exist in all transcripts
    num_transcripts = len(transcripts)
    common_segments = set(word for word, count in word_frequencies.items() if count == num_transcripts)

    # Split transcripts into matching and non-matching parts
    matching_parts = []
    non_matching_parts = []
    for transcript in transcripts:
        transcript_parts = []
        current_phrase = []
        for word in transcript.split():
            if word in common_segments:
                if current_phrase:
                    transcript_parts.append(" ".join(current_phrase))
                    current_phrase = []
                transcript_parts.append(word)
            else:
                current_phrase.append(word)
        if current_phrase:
            transcript_parts.append(" ".join(current_phrase))
        matching_parts.append(transcript_parts)

    # Insert <blank> into non-matching parts
    max_len = max(len(sublist) for sublist in matching_parts)
    for sublist in matching_parts:
        while len(sublist) < max_len:
            sublist.append('<blank>')

    # Choose most common word at each position
    final_transcript = []
    print(matching_parts)
    for parts in zip(*matching_parts):
        for i in range(max_len):
            # Exclude empty parts to avoid IndexError
            word_counts = Counter([part.split()[i] for part in parts if len(part.split()) > i])
            print(word_counts)
            if word_counts:
                most_common_word = word_counts.most_common(1)[0][0]
            else:
                most_common_word = '<blank>'
            final_transcript.append(most_common_word)

    return final_transcript

# Example usage
input_strings = [
    "antarctica is earths coolest continent and most complicated the claimed continent yet sadly has no official flag to unite her now you might say theres this and that flag is antarctica associated but its not official official and comes",
    "antarctica is earths coolest continent and most complicatedly claimed continent yet sadly has no official flag to unite her now you might say theres this and that flag is antarctica associated but its not official official and comes with",
    "and arctica is earths coolest continent and most complicatedly claimed continent yet sadly has no official flag to unite her nay you might say theres this and that flag is antarctica associated but its not official official and comes"
]

combined_transcript = combine_transcripts(input_strings)
print("Final Answer:", combined_transcript)

