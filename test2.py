def tokenize(sentence):
    # Helper function to tokenize a sentence into words
    return sentence.split()

def find_longest_sentence(sentences):
    # Helper function to find the longest sentence length
    return max(len(tokenize(sentence)) for sentence in sentences)

def insert_blank(sentence, idx, word):
    # Helper function to insert '<blank>' at the appropriate index in the sentence
    words = tokenize(sentence)
    words.insert(idx, word)
    return ' '.join(words)

def create_alignment_grid(sentences):
    longest_sentence_length = find_longest_sentence(sentences)
    grid = [[''] * longest_sentence_length for _ in range(3)]

    for i, sentence in enumerate(sentences):
        words = tokenize(sentence)
        for j, word in enumerate(words):
            # Check if the word exists in other sentences
            if all(word in tokenize(s) for s in sentences):
                grid[i][j] = word
            else:
                # Find the best index to insert '<blank>' to maximize alignment
                best_idx = -1
                best_score = -1

                for k in range(longest_sentence_length + 1):
                    if k < len(grid[i]):
                        grid_copy = [row[:] for row in grid]  # Create a copy of the grid
                        grid_copy[i][k] = word
                        score = sum(1 for x in range(longest_sentence_length) if grid_copy[0][x] == grid_copy[1][x] == grid_copy[2][x])
                        if score > best_score:
                            best_idx = k
                            best_score = score

                if best_idx != -1:
                    grid[i].insert(best_idx, word)

    return grid

# Test with your example input
input_sentences = [
    "antarctica is earths coolest continent and most complicated the claimed continent yet sadly has no official flag to unite her now you might say theres this and that flag is antarctica associated but its not official official and comes",
    "antarctica is earths foolest continent and most complicatedly claimed continent yet sadly has no official flag to unite her now you might say theres this and that flag is antarctica associated but its not official official and comes with",
    "and arctica is earths coolest continent and most complicatedly claimed continent yet sadly has no official flag to unite her nay you might say theres this and that flag is antarctica associated but its not official official and comes"
]

output_grid = create_alignment_grid(input_sentences)

for row in output_grid:
    print(row)



