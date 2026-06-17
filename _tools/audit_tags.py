#!/usr/bin/env python3
"""
Audit de tags y metadatos del frontmatter en el corpus SyV.

READ-ONLY: parsea el frontmatter YAML de cada .md del corpus y reporta
frecuencias de tags, conformidad con la taxonomía canónica, inventario de
campos y anomalías de formato.

Uso:
    uv run --with pyyaml _tools/audit_tags.py
o, si pyyaml ya está disponible:
    python3 _tools/audit_tags.py

El indexador `markdown-vault-syv` guarda los tags PLANOS (no parte por `/`),
así que los reportamos verbatim como los ve el indexador.
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Falta pyyaml. Corré: uv run --with pyyaml _tools/audit_tags.py")

ROOT = Path(__file__).resolve().parent.parent
CORPUS_FOLDERS = [
    "0_proyecto", "1_trasfondo", "2_atlas",
    "3_personajes", "4_diegesis", "5_aventuras", "6_media",
]
ROOT_NOTES = ["inicio.md", "404.md"]  # las 4 root notes; se filtran por existencia
EXCLUDE_NAMES = {"AGENTS.md", "CLAUDE.md", "CHANGELOG.md"}
EXCLUDE_DIRS = {"_tools", ".claude", ".obsidian", "_skills"}

# Taxonomía canónica (guia-de-metadatos.md)
ENTIDAD = {"personaje", "faccion", "ubicacion", "concepto", "credo", "hito", "relato", "guia"}
ALCANCE = {"secreto", "publico"}
ESTADO = {"canon", "borrador", "propuesta"}
LEGACY_FORBIDDEN = {"alerta-spoiler", "alerta-spoilers"}
ASCII_KEYS_OK = True  # detectamos field names no-inglés/no-ascii


def iter_corpus_files():
    # root notes
    for name in ROOT_NOTES:
        p = ROOT / name
        if p.exists():
            yield p
    # corpus folders
    for folder in CORPUS_FOLDERS:
        base = ROOT / folder
        if not base.is_dir():
            continue
        for p in base.rglob("*.md"):
            if any(part in EXCLUDE_DIRS for part in p.parts):
                continue
            if p.name in EXCLUDE_NAMES:
                continue
            yield p


def parse_frontmatter(path: Path):
    """Devuelve (dict|None, error|None). None dict = sin frontmatter o malformado."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return None, f"read-error: {e}"
    if not text.startswith("---"):
        return None, "no-frontmatter"
    # localizar el cierre
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, "unterminated-frontmatter"
    block = "\n".join(lines[1:end])
    try:
        data = yaml.safe_load(block)
    except Exception as e:
        return None, f"yaml-error: {e}"
    if data is None:
        return {}, None
    if not isinstance(data, dict):
        return None, "frontmatter-not-mapping"
    return data, None


def normalize_tags(value):
    """Devuelve (lista_de_tags, formato) donde formato in {list,string,other,absent}."""
    if value is None:
        return [], "absent"
    if isinstance(value, str):
        # un solo string: puede tener comas o espacios? lo tratamos como 1 tag verbatim
        return [value], "string"
    if isinstance(value, list):
        out = []
        for v in value:
            out.append(str(v))
        return out, "list"
    return [str(value)], "other"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def cap(items, n=15):
    items = list(items)
    if len(items) <= n:
        return items
    return items[:n] + [f"... (+{len(items) - n} más)"]


def main():
    files = sorted(iter_corpus_files())

    tag_counter = Counter()
    tag_to_files = defaultdict(list)
    key_counter = Counter()
    key_examples = defaultdict(list)

    files_no_entidad = []
    files_multi_entidad = []
    loose_tag_counter = Counter()
    loose_tag_files = defaultdict(list)
    legacy_tag_files = defaultdict(list)
    slug_like_tag_files = defaultdict(list)

    tags_as_string = []
    missing_title = []
    missing_folder = []
    missing_description = []
    folder_mismatch = []
    nonascii_keys = []
    parse_errors = []
    no_frontmatter = []

    for path in files:
        data, err = parse_frontmatter(path)
        if err == "no-frontmatter":
            no_frontmatter.append(rel(path))
            continue
        if err is not None:
            parse_errors.append(f"{rel(path)} :: {err}")
            continue

        # field inventory
        for k in data.keys():
            key_counter[k] += 1
            if len(key_examples[k]) < 15:
                key_examples[k].append(rel(path))
            if not isinstance(k, str) or not k.isascii():
                nonascii_keys.append(f"{rel(path)} :: {k!r}")

        # universal fields
        if not data.get("title"):
            missing_title.append(rel(path))
        if not data.get("folder"):
            missing_folder.append(rel(path))
        else:
            actual = str(path.parent.relative_to(ROOT))
            if str(data["folder"]).strip().strip("/") != actual:
                folder_mismatch.append(f"{rel(path)} :: folder={data['folder']!r} actual={actual!r}")
        if not data.get("description"):
            missing_description.append(rel(path))

        # tags
        tags, fmt = normalize_tags(data.get("tags"))
        if fmt == "string":
            tags_as_string.append(f"{rel(path)} :: tags={data.get('tags')!r}")

        entidad_tags = []
        for t in tags:
            tag_counter[t] += 1
            tag_to_files[t].append(rel(path))

            if t in LEGACY_FORBIDDEN:
                legacy_tag_files[t].append(rel(path))
                continue

            if "/" in t:
                tree, _, leaf = t.partition("/")
                if tree == "entidad":
                    entidad_tags.append(t)
                    if leaf not in ENTIDAD:
                        loose_tag_counter[t] += 1
                        loose_tag_files[t].append(rel(path))
                elif tree == "alcance":
                    if leaf not in ALCANCE:
                        loose_tag_counter[t] += 1
                        loose_tag_files[t].append(rel(path))
                elif tree == "estado":
                    if leaf not in ESTADO:
                        loose_tag_counter[t] += 1
                        loose_tag_files[t].append(rel(path))
                else:
                    # rama desconocida
                    loose_tag_counter[t] += 1
                    loose_tag_files[t].append(rel(path))
            else:
                # sin "/" => palabra suelta o slug/wikilink
                loose_tag_counter[t] += 1
                loose_tag_files[t].append(rel(path))
                if t.startswith("[[") or "|" in t or " " not in t and "-" in t:
                    slug_like_tag_files[t].append(rel(path))

        if not entidad_tags:
            files_no_entidad.append(rel(path))
        elif len(entidad_tags) > 1:
            files_multi_entidad.append(f"{rel(path)} :: {entidad_tags}")

    # ---- REPORTE ----
    out = []
    P = out.append
    total = len(files)
    P("=" * 72)
    P(f"AUDITORÍA DE TAGS Y METADATOS — corpus SyV ({total} archivos .md)")
    P("=" * 72)
    if no_frontmatter:
        P(f"\n[!] {len(no_frontmatter)} archivos SIN frontmatter:")
        for f in cap(no_frontmatter):
            P(f"    - {f}")
    if parse_errors:
        P(f"\n[!] {len(parse_errors)} archivos con frontmatter MALFORMADO:")
        for f in cap(parse_errors):
            P(f"    - {f}")

    # 1
    P("\n" + "-" * 72)
    P("1. FRECUENCIA DE VALORES DE TAG (verbatim, como los ve el indexador plano)")
    P("-" * 72)
    P(f"   Tags distintos: {len(tag_counter)}  ·  ocurrencias totales: {sum(tag_counter.values())}")
    for tag, n in sorted(tag_counter.items(), key=lambda kv: (-kv[1], kv[0])):
        P(f"   {n:5d}  {tag}")

    # 2
    P("\n" + "-" * 72)
    P("2. CONFORMIDAD CON LA TAXONOMÍA CANÓNICA")
    P("-" * 72)
    P("   Esquema: entidad/{%s}" % "|".join(sorted(ENTIDAD)))
    P("            alcance/{%s}  ·  estado/{%s}" % ("|".join(sorted(ALCANCE)), "|".join(sorted(ESTADO))))

    P(f"\n   2a. Archivos SIN tag entidad/* : {len(files_no_entidad)}")
    for f in cap(files_no_entidad):
        P(f"       - {f}")

    P(f"\n   2b. Archivos con MÁS DE UN tag entidad/* : {len(files_multi_entidad)}")
    for f in cap(files_multi_entidad):
        P(f"       - {f}")

    P(f"\n   2c. Valores de tag FUERA de los tres árboles (palabras sueltas / ramas inválidas): "
      f"{len(loose_tag_counter)} distintos")
    for tag, n in sorted(loose_tag_counter.items(), key=lambda kv: (-kv[1], kv[0])):
        ex = cap(loose_tag_files[tag], 8)
        P(f"       {n:4d}  {tag}")
        for f in ex:
            P(f"             · {f}")

    P(f"\n   2d. Formas LEGACY/PROHIBIDAS (alerta-spoiler/-spoilers): "
      f"{sum(len(v) for v in legacy_tag_files.values())}")
    for tag, fl in legacy_tag_files.items():
        P(f"       {tag}: {len(fl)}")
        for f in cap(fl):
            P(f"             · {f}")

    P(f"\n   2e. Tags que parecen slug/wikilink: {len(slug_like_tag_files)} distintos")
    for tag, fl in sorted(slug_like_tag_files.items(), key=lambda kv: -len(kv[1])):
        P(f"       {tag}: {len(fl)}")
        for f in cap(fl, 6):
            P(f"             · {f}")

    # 3
    P("\n" + "-" * 72)
    P("3. INVENTARIO DE CAMPOS DEL FRONTMATTER")
    P("-" * 72)
    for k, n in sorted(key_counter.items(), key=lambda kv: (-kv[1], str(kv[0]))):
        P(f"   {n:5d}  {k}")

    # 4
    P("\n" + "-" * 72)
    P("4. ANOMALÍAS DE FORMATO")
    P("-" * 72)
    P(f"   4a. tags como STRING (no lista): {len(tags_as_string)}")
    for f in cap(tags_as_string):
        P(f"       - {f}")
    P(f"\n   4b. falta `title`: {len(missing_title)}")
    for f in cap(missing_title):
        P(f"       - {f}")
    P(f"\n   4c. falta `folder`: {len(missing_folder)}")
    for f in cap(missing_folder):
        P(f"       - {f}")
    P(f"\n   4d. falta `description`: {len(missing_description)}")
    for f in cap(missing_description):
        P(f"       - {f}")
    P(f"\n   4e. `folder` NO coincide con la carpeta real: {len(folder_mismatch)}")
    for f in cap(folder_mismatch):
        P(f"       - {f}")
    P(f"\n   4f. nombres de campo no-ascii / no-inglés sospechosos: {len(nonascii_keys)}")
    for f in cap(nonascii_keys):
        P(f"       - {f}")

    P("\n" + "=" * 72)
    P("FIN")
    P("=" * 72)
    print("\n".join(out))


if __name__ == "__main__":
    main()
