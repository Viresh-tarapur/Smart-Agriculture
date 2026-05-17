import re

file_path = 'templates/what_to_grow.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace :root variables
content = re.sub(
    r':root\s*\{[^}]+\}',
    ':root {\n            --bg-color: #f5f7fa;\n            --surface-color: #ffffff;\n            --primary-accent: #2e7d32;\n            --text-primary: #333333;\n            --text-secondary: #666666;\n            --border-color: #e0e0e0;\n            --input-bg: #fdfdfd;\n            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);\n            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);\n        }',
    content
)

# Dark specific to light specific
content = content.replace('rgba(11, 15, 25, 0.9)', 'rgba(255, 255, 255, 0.95)')
content = content.replace('background-color: #2d3748;', 'background-color: #f0f0f0;')
content = content.replace('background: rgba(255, 255, 255, 0.05);', 'background: var(--surface-color);')
content = content.replace('background-color: white;', 'background-color: #fff;') # slider button
content = content.replace('background-color: rgba(255, 255, 255, 0.02);', 'background-color: #f5f5f5;')
content = content.replace('background-color: #0d8a6a;', 'background-color: #4caf50;') # hover submit

# Bubbles
content = content.replace('background: linear-gradient(145deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03));', 'background: var(--surface-color);')
content = content.replace('border: 1px solid rgba(255, 255, 255, 0.1);', 'border: 1px solid var(--border-color);')
content = content.replace('border-bottom: 1px solid rgba(255, 255, 255, 0.1);', 'border-bottom: 1px solid var(--border-color);')
content = content.replace('border-top: 1px solid rgba(255, 255, 255, 0.1);', 'border-top: 1px solid var(--border-color);')
content = content.replace('color: #fff;', 'color: var(--text-primary);')
content = content.replace('color: #d1d5db;', 'color: var(--text-primary);')

# Floating input
content = content.replace('background: rgba(32, 33, 35, 0.8);', 'background: rgba(255, 255, 255, 0.95);')
content = content.replace('color: white;', 'color: var(--text-primary);')
content = content.replace('.floating-input input {\\n            flex-grow: 1;\\n            background: transparent;\\n            border: none;\\n            color: var(--text-primary);', '.floating-input input {\\n            flex-grow: 1;\\n            background: transparent;\\n            border: none;\\n            color: var(--text-primary);', 1)

# Slider bg
content = content.replace('background-color: var(--input-bg);\\n            transition: .4s;\\n            border-radius: 34px;\\n            border: 1px solid var(--border-color);', 'background-color: #ccc;\\n            transition: .4s;\\n            border-radius: 34px;\\n            border: 1px solid var(--border-color);')


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Success')
