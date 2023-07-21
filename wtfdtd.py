from collections import Counter

def combine_transcripts(transcripts):
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
        for word in transcript.split():  # Update this line to use word directly (since it's an array of strings)
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
    
    for line in matching_parts:
        print(line)
    print("__________________________________________________________________________________________________________________")
    # Insert <blank> into non-matching parts
    size = len(matching_parts)
    tracker = [1,1,1]
    for count in range(max([len(i) for i in matching_parts])):
        if all(matching_parts[0][count] == sublist[count] for sublist in matching_parts[1:]):
            pass
        else:
            if all(len(matching_parts[0][count]) == len(sublist[count]) for sublist in matching_parts[1:]):
                pass
            else:
                maxLen = max(len(matching_parts[i][count].split()) for i in range(len(transcripts)))

                for j in range(len(transcripts)):
                    tracking = 0
                    while (len(matching_parts[j][count].split())+tracking) < maxLen:  
                        matching_parts[j].insert(count+tracker[j],' <blank>')
                        tracker[j]+=1
                        tracking+=1
    for line in matching_parts:
        print(line)
    # Choose most common word at each position
    final_transcript = []
    for parts in zip(*matching_parts):
        for i in range(len(parts[0])):
            print(parts)
            print(i)
            word_counts = Counter([part[i] for part in parts])
            most_common_word = word_counts.most_common(1)[0][0]
            final_transcript.append(most_common_word)

    return ' '.join(final_transcript)

# Example usage
input_strings = [
    "either way a slow painful death begins for all but one player the rest of the game can take ayear or six",
    "either way a slow painful death begins for all but one player the rest of the game can take an hour or six",
    "by their way a slow painful death begins for all but one player the rest of the game can take an hour or six"
]

combined_transcript = combine_transcripts(input_strings)
print(combined_transcript)



# Example usage
input_transcripts = [
    "start: antarctica is earths coolest cat continent",
    "start: antarctica is earths coolest continent",
    "start: and arctica is earths coolest continent"
]

combined_transcript = combine_transcripts(input_transcripts)
print(combined_transcript)