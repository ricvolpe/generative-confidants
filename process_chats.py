import os
import pandas as pd

data_dir = 'data/anonymised'
ai_prefixes = [ 
    "ChatGPT:", 
    "ChatGPT said:", 
    "AI:",
    "Meta AI:",
    "Gemini:",
    "Biblical Angel (c.ai):",
    "Cthulu (c.ai):",
    "Bing:"
]
results = []
for filename in sorted(os.listdir(data_dir)):
    user = filename.split('_')[0]
    if 'chat' in filename:
        entry_no = filename.split('_')[1]
        file_path = os.path.join(data_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            user_messages = []
            ai_messages = []
            lines = content.splitlines()
            current = None
            buffer = []
            for line in lines + ['']:
                if line.startswith(f"{user.capitalize()}:"):
                    if current == "ai" and buffer:
                        ai_messages.append('\n'.join(buffer).strip())
                        buffer = []
                    current = "user"
                    buffer = []
                elif any(line.startswith(prefix) for prefix in ai_prefixes):
                    if current == "user" and buffer:
                        user_messages.append('\n'.join(buffer).strip())
                        buffer = []
                    current = "ai"
                    buffer = []
                else:
                    buffer.append(line)
            if current == "user" and buffer:
                user_messages.append('\n'.join(buffer).strip())
            elif current == "ai" and buffer:
                ai_messages.append('\n'.join(buffer).strip())
            user_msg_count = len(user_messages)
            ai_msg_count = len(ai_messages)
            avg_user_len = int(sum(len(msg.split()) for msg in user_messages) 
                               / user_msg_count if user_msg_count else 0)
            avg_ai_len = int(sum(len(msg.split()) for msg in ai_messages) 
                             / ai_msg_count if ai_msg_count else 0)
            results.append({
                'user': user,
                'entry_no': entry_no,
                'user_msg': user_msg_count,
                'user_len': avg_user_len,
                'ai_len': avg_ai_len
            })

df = pd.DataFrame(results)
grouped = df.groupby('user').agg({
    'user_msg': ['mean', 'std', 'count'],
    'user_len': ['mean', 'std'],
    'ai_len': ['mean', 'std']
}).reset_index()
grouped.columns = ['_'.join(col).strip('_') for col in grouped.columns.values]
grouped = grouped.round(1).fillna(0)
df.to_excel('data/chat_stats_raw.xlsx', index=False)
grouped.to_excel('data/chat_stats_grouped.xlsx', index=False)
