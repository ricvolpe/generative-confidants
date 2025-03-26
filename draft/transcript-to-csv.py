import pandas as pd
import re

def analyze_conversation(transcript_text):
    # Precompile regex patterns
    author_pattern = re.compile(r'^(ME:|HAL:|AI:)')
    metadata_patterns = ('Original source:', 'Posted on:', 'Context:', 
                        'Chatbot:', 'Transcript')
    
    messages = []
    current_lines = []
    current_author = None
    
    # Process all lines in a single pass
    for line in transcript_text.splitlines():
        line = line.strip()
        
        # Skip empty lines and metadata efficiently
        if not line or any(line.startswith(p) for p in metadata_patterns):
            continue
            
        # Check for new message markers
        if line.startswith(('ME:', 'HAL:')):
            # Save previous message if exists
            if current_lines:
                messages.append({
                    'author': current_author,
                    'text': ' '.join(current_lines),
                    'word_count': sum(len(l.split()) for l in current_lines)
                })
            current_author = 'human'
            current_lines = [author_pattern.sub('', line)]
        
        elif line.startswith('AI:'):
            if current_lines:
                messages.append({
                    'author': current_author,
                    'text': ' '.join(current_lines),
                    'word_count': sum(len(l.split()) for l in current_lines)
                })
            current_author = 'chatbot'
            current_lines = [author_pattern.sub('', line)]
        
        # Handle implicit chatbot responses
        elif current_author == 'human' and line and not line.startswith('###'):
            if current_lines:
                messages.append({
                    'author': current_author,
                    'text': ' '.join(current_lines),
                    'word_count': sum(len(l.split()) for l in current_lines)
                })
            current_author = 'chatbot'
            current_lines = [line]
        
        # Append to current message
        elif current_author and not line.startswith('###'):
            current_lines.append(line)
    
    # Add final message
    if current_lines:
        messages.append({
            'author': current_author,
            'text': ' '.join(current_lines),
            'word_count': sum(len(l.split()) for l in current_lines)
        })
    
    # Create DataFrame directly with all required columns
    df = pd.DataFrame(messages)
    
    # Add length category using vectorized operations
    df['length'] = pd.cut(df['word_count'], 
                         bins=[-float('inf'), 49, 150, float('inf')],
                         labels=['Short', 'Medium', 'Long'])
    
    # Calculate position vectorized (fixed the rounding issue)
    total_messages = len(df)
    df['position'] = ((df.index + 1) / total_messages * 100).astype(int)
    
    return df

# Example usage:
if __name__ == "__main__":
    with open('gen-confidants/transcripts/raw/anxious-teen.txt', 'r') as file:
        transcript = file.read()
    
    conversation_df = analyze_conversation(transcript)
    conversation_df.to_csv('gen-confidants/transcripts/csv/anxious-teen.csv', index=False)
