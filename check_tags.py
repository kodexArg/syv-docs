import os
import re
import yaml

def get_markdown_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                yield os.path.join(root, file)

files = list(get_markdown_files('.'))

tag_files = {}

frontmatter_pattern = re.compile(r'^---\n(.*?)\n---', re.DOTALL)
inline_tag_pattern = re.compile(r'(?<![\w#])#([a-zA-Z0-9_-]+)')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = frontmatter_pattern.search(content)
    tags_in_file = set()
    if match:
        fm_text = match.group(1)
        try:
            fm = yaml.safe_load(fm_text)
            if fm and 'tags' in fm:
                tags = fm['tags']
                if isinstance(tags, list):
                    for t in tags:
                        tags_in_file.add(t)
                elif isinstance(tags, str):
                    for t in tags.split(','):
                        tags_in_file.add(t.strip())
        except Exception as e:
            pass
            
    for t in inline_tag_pattern.findall(content):
        tags_in_file.add(t)
        
    for t in tags_in_file:
        if t not in tag_files:
            tag_files[t] = set()
        tag_files[t].add(file)

single_node_tags = {tag: list(paths)[0] for tag, paths in tag_files.items() if len(paths) == 1}

print(f"Total single node tags: {len(single_node_tags)}")
character_tags_to_remove = {}
for tag, path in single_node_tags.items():
    if '3_personajes' in path:
        if path not in character_tags_to_remove:
            character_tags_to_remove[path] = []
        character_tags_to_remove[path].append(tag)

print(f"Files in 3_personajes to modify: {len(character_tags_to_remove)}")
for p, ts in list(character_tags_to_remove.items())[:5]:
    print(f"{p}: {ts}")
