import os
import re
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True

def get_markdown_files(directory):
    for root, dirs, files in os.walk(directory):
        if '.obsidian' in dirs:
            dirs.remove('.obsidian')
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.endswith('.md'):
                yield os.path.join(root, file)

files = list(get_markdown_files('.'))
tag_files = {}

frontmatter_pattern = re.compile(r'^---\n(.*?)\n---', re.DOTALL)
inline_tag_pattern = re.compile(r'(?<![\w#])#([a-zA-Z0-9_-]+)')

# Step 1: Collect tag frequencies across all markdown files
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = frontmatter_pattern.search(content)
    tags_in_file = set()
    if match:
        fm_text = match.group(1)
        try:
            fm = yaml.load(fm_text)
            if fm and 'tags' in fm:
                tags = fm['tags']
                if isinstance(tags, list):
                    for t in tags:
                        if t is not None:
                            tags_in_file.add(str(t).strip())
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

# Step 2: Identify single node tags
single_node_tags = {tag: list(paths)[0] for tag, paths in tag_files.items() if len(paths) == 1}

# Step 3: Filter those that are in 3_personajes
character_tags_to_remove = {}
for tag, path in single_node_tags.items():
    if '3_personajes' in path.replace('\\', '/'):
        if path not in character_tags_to_remove:
            character_tags_to_remove[path] = set()
        character_tags_to_remove[path].add(tag)

print(f"Total files in 3_personajes to modify: {len(character_tags_to_remove)}")

# Step 4: Remove these tags from the specific files
for file_path, tags_to_remove in character_tags_to_remove.items():
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    match = frontmatter_pattern.search(content)
    new_content = content
    if match:
        fm_text = match.group(1)
        try:
            fm = yaml.load(fm_text)
            if fm and 'tags' in fm:
                original_tags = fm['tags']
                if isinstance(original_tags, list):
                    new_tags = [t for t in original_tags if t is not None and str(t).strip() not in tags_to_remove]
                    fm['tags'] = new_tags
                    
                    import io
                    buf = io.StringIO()
                    yaml.dump(fm, buf)
                    new_fm_text = buf.getvalue().strip()
                    new_content = new_content[:match.start()] + '---\n' + new_fm_text + '\n---' + new_content[match.end():]
                elif isinstance(original_tags, str):
                    new_tags = [t.strip() for t in original_tags.split(',') if t.strip() not in tags_to_remove]
                    fm['tags'] = new_tags
                    
                    import io
                    buf = io.StringIO()
                    yaml.dump(fm, buf)
                    new_fm_text = buf.getvalue().strip()
                    new_content = new_content[:match.start()] + '---\n' + new_fm_text + '\n---' + new_content[match.end():]
        except Exception as e:
            print(f"Error parsing frontmatter in {file_path}: {e}")
            
    # Also remove inline tags
    for tag in tags_to_remove:
        # replace #tag only when it's an isolated tag (not part of a word or link, basic heuristic)
        # we can replace '#tag ' with '' or similar, but just doing a regex substitution:
        pattern = r'(?<![\w#])#' + re.escape(tag) + r'\b\s*'
        new_content = re.sub(pattern, '', new_content)
        
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")

print("Done.")