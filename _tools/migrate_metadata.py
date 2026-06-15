#!/usr/bin/env python3
"""
migrate_metadata.py — SyV vault frontmatter migration tool.

Reads every .md in syv-docs/, applies a deterministic set of transforms to
frontmatter + tags, and either reports proposed changes (--dry-run, default)
or writes them back (--apply).

Technique: ruamel.yaml round-trip with preserve_quotes — only the frontmatter
region (bytes between the leading ---) is replaced; body bytes are untouched.

Usage (via uv run):
    uv run python _tools/migrate_metadata.py                  # dry-run (default)
    uv run python _tools/migrate_metadata.py --dry-run        # explicit dry-run
    uv run python _tools/migrate_metadata.py --apply          # write changes

Requirements: ruamel.yaml (stdlib + ruamel.yaml only).
"""

from __future__ import annotations

import argparse
import io
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

VAULT_ROOT = Path(__file__).parent.parent  # syv-docs/

SKIP_DIRS = {".git", ".obsidian", "_tools", "_skills"}

# Taxonomy: the only valid tag values (without leading #)
VALID_TAXONOMY: set[str] = {
    "entidad/personaje",
    "entidad/faccion",
    "entidad/ubicacion",
    "entidad/concepto",
    "entidad/credo",
    "entidad/hito",
    "entidad/relato",
    "entidad/guia",
    "alcance/secreto",
    "alcance/publico",
    "estado/canon",
    "estado/borrador",
    "estado/propuesta",
}

# Synonyms → taxonomy. Only values that ACTUALLY occur in the corpus.
# Derived from inventory scan (see comments).
TAG_SYNONYMS: dict[str, str | None] = {
    # bare sub-labels that appeared (count = 1 each, index files)
    "personajes": None,   # purely loose → REMOVE (no matching basename in docs)
    "facciones":  None,   # purely loose → REMOVE
    "relato":     None,   # purely loose → REMOVE  (there IS a relato.md? checked: no)
    # non-standard but taxonomy-looking
    # entidad/aventura: keep as-is (it's a real sub-type used in 5_aventuras, report only)
    # estado/sospechoso: in _skills only, report only
}

# Spanish field name → English canonical (closed safe set)
SPANISH_TO_ENGLISH: dict[str, str] = {
    "titulo": "title",
    "carpeta": "folder",
    "descripcion": "description",
    "descripción": "description",
}

# Non-standard but taxonomy-looking tags to REPORT (not auto-remove)
REPORT_ONLY_TAGS: set[str] = {
    "entidad/aventura",
    "estado/sospechoso",
}

# Tags that look like old full-path trasfondo sub-trees → REMOVE
OLD_PATH_TAG_PATTERN = re.compile(r"^trasfondo/codex/.+$")

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class FileReport:
    rel_path: str
    transforms: list[str] = field(default_factory=list)   # applied / would-apply
    warnings: list[str] = field(default_factory=list)     # reported, not applied
    changed: bool = False


@dataclass
class RunReport:
    file_reports: list[FileReport] = field(default_factory=list)
    parse_errors: list[str] = field(default_factory=list)
    field_freq_before: dict[str, int] = field(default_factory=dict)
    tag_freq_before: dict[str, int] = field(default_factory=dict)

    # per-category change counts
    category_counts: dict[str, int] = field(default_factory=lambda: defaultdict(int))


# ---------------------------------------------------------------------------
# YAML helpers
# ---------------------------------------------------------------------------

_yaml = YAML()
_yaml.preserve_quotes = True
_yaml.width = 4096  # prevent line-wrapping
_yaml.indent(mapping=2, sequence=4, offset=2)  # match corpus style: "  - item"


def _load_yaml(text: str) -> Any:
    return _yaml.load(text)


def _dump_yaml(obj: Any) -> str:
    buf = io.StringIO()
    _yaml.dump(obj, buf)
    return buf.getvalue().strip()


# Frontmatter extraction: bytes between leading ---
_FM_RE = re.compile(r"^(---\n)(.*?)(\n---)", re.DOTALL)


def _split_content(content: str) -> tuple[str, str, str] | None:
    """Return (pre, fm_text, post) where pre='---\n', post='\n---<rest>'."""
    m = _FM_RE.match(content)
    if not m:
        return None
    pre = m.group(1)
    fm_text = m.group(2)
    rest = content[m.end():]  # everything after closing ---
    return pre, fm_text, rest


# ---------------------------------------------------------------------------
# Corpus helpers
# ---------------------------------------------------------------------------


def collect_files(root: Path) -> list[Path]:
    result: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if fname.endswith(".md"):
                result.append(Path(dirpath) / fname)
    return sorted(result)


def collect_skipped_files(root: Path) -> list[str]:
    """List .md files that are excluded from the walk (out-of-scope dirs)."""
    out_of_scope_dirs = {"_skills"}
    result: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        parts = rel.parts
        if parts and parts[0] in out_of_scope_dirs:
            for fname in filenames:
                if fname.endswith(".md"):
                    result.append((rel / fname).as_posix())
    return sorted(result)


def collect_basenames(files: list[Path]) -> set[str]:
    return {f.stem for f in files}


# ---------------------------------------------------------------------------
# Transforms (all operate on the parsed fm dict in-place and append to log)
# ---------------------------------------------------------------------------


def _transform_spanish_fields(
    fm: dict, rpt: FileReport, category_counts: dict
) -> None:
    """T7: español field names → English (closed safe map)."""
    for src, dst in SPANISH_TO_ENGLISH.items():
        if src in fm:
            if dst in fm:
                rpt.warnings.append(
                    f"key-conflict: '{src}' → '{dst}' but '{dst}' already exists; skipped"
                )
                category_counts["key_conflict"] += 1
            else:
                fm[dst] = fm.pop(src)
                rpt.transforms.append(f"field-rename: '{src}' → '{dst}'")
                category_counts["field_rename"] += 1
                rpt.changed = True


def _transform_spoilers(fm: dict, rpt: FileReport, category_counts: dict) -> None:
    """T6: alerta-spoiler / alerta-spoilers → spoilers list + alcance/secreto."""
    for legacy_key in ("alerta-spoiler", "alerta-spoilers"):
        if legacy_key in fm:
            val = fm.pop(legacy_key)
            existing = fm.get("spoilers") or []
            if isinstance(existing, str):
                existing = [existing]
            if isinstance(val, str):
                val = [val]
            elif not isinstance(val, list):
                val = [str(val)]
            fm["spoilers"] = existing + [v for v in val if v not in existing]
            rpt.transforms.append(f"spoiler-migrate: '{legacy_key}' → 'spoilers'")
            category_counts["spoiler_migrate"] += 1
            rpt.changed = True
    # Ensure alcance/secreto tag if spoilers present
    if fm.get("spoilers"):
        tags = _get_tags_list(fm)
        if "alcance/secreto" not in tags:
            tags.append("alcance/secreto")
            fm["tags"] = tags
            rpt.transforms.append("tag-add: 'alcance/secreto' (spoilers present)")
            category_counts["tag_add"] += 1
            rpt.changed = True


def _get_tags_list(fm: dict) -> list[str]:
    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    return [str(t).lstrip("#").strip() for t in tags if t is not None]


def _transform_tags(
    fm: dict, rpt: FileReport, category_counts: dict, basenames: set[str], rel_path: str
) -> None:
    """T2/T3/T5: normalize tags to taxonomy; remove loose theme-words or move to related."""
    raw_tags = fm.get("tags")
    if raw_tags is None:
        return

    tags = _get_tags_list(fm)
    new_tags: list[str] = []
    changed = False

    for t in tags:
        t_norm = t.lstrip("#").strip()

        if t_norm in VALID_TAXONOMY:
            # Already valid — keep as-is
            new_tags.append(t_norm)
            continue

        if t_norm in REPORT_ONLY_TAGS:
            # Non-standard but structurally OK; report, keep
            rpt.warnings.append(
                f"non-standard-tag: '{t_norm}' not in taxonomy (entidad/aventura or estado/sospechoso); kept"
            )
            new_tags.append(t_norm)
            continue

        # Old deep-path tags (trasfondo/codex/...)
        if OLD_PATH_TAG_PATTERN.match(t_norm):
            rpt.transforms.append(f"tag-remove: '{t_norm}' (old path-style tag)")
            category_counts["tag_remove"] += 1
            changed = True
            continue

        # Synonym?
        if t_norm in TAG_SYNONYMS:
            target = TAG_SYNONYMS[t_norm]
            if target is None:
                # purely loose
                if t_norm in basenames:
                    _move_tag_to_related(fm, t_norm, rpt, category_counts)
                    changed = True
                else:
                    rpt.transforms.append(f"tag-remove: '{t_norm}' (loose/synonym→None)")
                    category_counts["tag_remove"] += 1
                    changed = True
            else:
                if target not in new_tags:
                    new_tags.append(target)
                rpt.transforms.append(f"tag-normalize: '{t_norm}' → '{target}'")
                category_counts["tag_normalize"] += 1
                changed = True
            continue

        # Loose theme-word
        if t_norm in basenames:
            _move_tag_to_related(fm, t_norm, rpt, category_counts)
            changed = True
        else:
            rpt.transforms.append(f"tag-remove: '{t_norm}' (loose, not a basename)")
            category_counts["tag_remove"] += 1
            changed = True

    if changed:
        fm["tags"] = new_tags
        rpt.changed = True
    else:
        fm["tags"] = new_tags  # still normalize (strip leading #)


def _move_tag_to_related(
    fm: dict, tag: str, rpt: FileReport, category_counts: dict
) -> None:
    wikilink = f"[[{tag}]]"
    related = fm.get("related") or []
    if isinstance(related, str):
        related = [related]
    related = list(related)
    if wikilink not in [str(r) for r in related]:
        # DoubleQuotedScalarString ensures the emitted YAML uses "[[...]]"
        # (double-quoted), matching corpus convention and making it valid YAML
        # (bare [[x]] would be parsed as a flow sequence).
        related.append(DoubleQuotedScalarString(wikilink))
        fm["related"] = related
        rpt.transforms.append(
            f"tag-to-related: '{tag}' → related: '{wikilink}'"
        )
        category_counts["tag_to_related"] += 1


def _report_missing_entidad_tag(
    fm: dict, rpt: FileReport, category_counts: dict, rel_path: str
) -> None:
    """T4 (report-only): flag files with no entidad/* tag for human review.

    Folder→entidad inference is deferred: every missing-entidad case in the
    corpus is an index.md / landing page where the right tag requires content
    judgment, not path arithmetic.
    """
    tags = _get_tags_list(fm)
    has_entidad = any(t.startswith("entidad/") for t in tags)
    if not has_entidad:
        rel_parts = Path(rel_path).parent.as_posix()
        rpt.warnings.append(
            f"missing-entidad-tag: no entidad/* tag; folder='{rel_parts}' (needs human review)"
        )
        category_counts["missing_entidad"] += 1


def _transform_folder_normalize(
    fm: dict, rpt: FileReport, category_counts: dict, rel_path: str
) -> None:
    """T8: normalize folder to real relative directory."""
    real_dir = Path(rel_path).parent.as_posix()
    if real_dir == ".":
        # root-level file — skip if no folder set
        return
    current = fm.get("folder", "")
    if not current:
        return  # missing folder — reported elsewhere (T11)
    if str(current) != real_dir:
        fm["folder"] = real_dir
        rpt.transforms.append(
            f"folder-normalize: '{current}' → '{real_dir}'"
        )
        category_counts["folder_normalize"] += 1
        rpt.changed = True


def _transform_missing_fields(
    fm: dict, rpt: FileReport, category_counts: dict, rel_path: str
) -> None:
    """T11: report missing title / description. Auto-fill folder where derivable."""
    if not fm.get("title"):
        rpt.warnings.append("missing-title: no 'title' field (cannot fabricate)")
        category_counts["missing_title"] += 1

    if not fm.get("description"):
        rpt.warnings.append("missing-description: no 'description' field (cannot fabricate)")
        category_counts["missing_description"] += 1

    # Auto-derive folder only if absent
    if not fm.get("folder"):
        real_dir = Path(rel_path).parent.as_posix()
        if real_dir != ".":
            fm["folder"] = real_dir
            rpt.transforms.append(
                f"folder-set: '{real_dir}' (derived from path)"
            )
            category_counts["folder_set"] += 1
            rpt.changed = True
        else:
            rpt.warnings.append("missing-folder: root-level file, cannot derive")
            category_counts["missing_folder"] += 1


def _transform_at_syntax(
    content: str, fm_end: int, rpt: FileReport, category_counts: dict
) -> str:
    """T9: @[path.md] → [[basename]] in body (after fm_end).

    Skips occurrences inside inline code spans (`...`) and fenced code blocks
    (``` ... ```) so that documentation examples are never rewritten.
    """
    body = content[fm_end:]

    # Build a set of character ranges that are inside code spans or fences.
    # We scan once; any @[...] match whose start falls in a protected range is skipped.
    protected: list[tuple[int, int]] = []

    # Fenced code blocks: opening ``` (with optional language) to closing ```
    for m in re.finditer(r"```[^\n]*\n.*?```", body, re.DOTALL):
        protected.append((m.start(), m.end()))

    # Inline code spans: single backtick pairs (not preceded/followed by additional backticks)
    for m in re.finditer(r"(?<!`)`(?!`)[^`\n]+?`(?!`)", body):
        protected.append((m.start(), m.end()))

    def _in_protected(pos: int) -> bool:
        return any(start <= pos < end for start, end in protected)

    n = 0
    result_parts: list[str] = []
    last = 0
    for m in re.finditer(r"@\[([^\]]+)\]", body):
        if _in_protected(m.start()):
            continue
        result_parts.append(body[last:m.start()])
        result_parts.append(f"[[{Path(m.group(1)).stem}]]")
        last = m.end()
        n += 1
    result_parts.append(body[last:])
    new_body = "".join(result_parts)

    if n:
        rpt.transforms.append(f"at-syntax: replaced {n} @[...] → [[...]] in body")
        category_counts["at_syntax"] += 1
        rpt.changed = True
        return content[:fm_end] + new_body
    return content


def _transform_wikilink_quoting(
    fm: dict, rpt: FileReport, category_counts: dict
) -> None:
    """T10: ensure wikilink values in relation fields are quoted strings.

    Existing wikilink values are kept as-is (preserving their ruamel scalar
    type, e.g. DoubleQuotedScalarString) so that preserve_quotes round-trips
    them without style churn. Only non-wikilink display-name values are reported.
    """
    for field_name in ("facciones", "related", "ubicaciones", "apariciones"):
        vals = fm.get(field_name)
        if not vals:
            continue
        if isinstance(vals, str):
            vals = [vals]
        for v in vals:
            sv = str(v).strip()
            if not (sv.startswith("[[") and sv.endswith("]]")):
                # Non-wikilink display name — report, leave value in place
                rpt.warnings.append(
                    f"non-wikilink-display: {field_name}: {repr(sv)} (needs manual review)"
                )
                category_counts["non_wikilink_display"] += 1
        # Do NOT reassign fm[field_name] — preserve the original ruamel list
        # object (and its scalar type annotations) to avoid quote/style churn.


# ---------------------------------------------------------------------------
# Per-file processing
# ---------------------------------------------------------------------------


def process_file(
    fpath: Path,
    vault_root: Path,
    basenames: set[str],
    dry_run: bool,
    run_rpt: RunReport,
) -> None:
    rel_path = fpath.relative_to(vault_root).as_posix()
    rpt = FileReport(rel_path=rel_path)
    run_rpt.file_reports.append(rpt)

    content = fpath.read_text(encoding="utf-8")

    # Collect before-stats
    split = _split_content(content)
    if split is None:
        rpt.warnings.append("no-frontmatter: file skipped")
        return

    pre, fm_text, rest = split
    try:
        fm = _load_yaml(fm_text)
    except Exception as exc:
        run_rpt.parse_errors.append(f"{rel_path}: {exc}")
        rpt.warnings.append(f"parse-error: {exc}")
        return

    if fm is None:
        rpt.warnings.append("empty-frontmatter: skipped")
        return

    # Record field + tag frequencies BEFORE
    for k in fm.keys():
        run_rpt.field_freq_before[str(k)] = run_rpt.field_freq_before.get(str(k), 0) + 1
    raw_tags = fm.get("tags") or []
    if isinstance(raw_tags, str):
        raw_tags = [raw_tags]
    for t in raw_tags:
        if t is not None:
            ts = str(t).lstrip("#").strip()
            run_rpt.tag_freq_before[ts] = run_rpt.tag_freq_before.get(ts, 0) + 1

    # --- Apply transforms (order matters) ---

    # T7: español field names
    _transform_spanish_fields(fm, rpt, run_rpt.category_counts)

    # T6: spoilers migration
    _transform_spoilers(fm, rpt, run_rpt.category_counts)

    # T11: missing fields (folder auto-fill + reports)
    _transform_missing_fields(fm, rpt, run_rpt.category_counts, rel_path)

    # T8: folder normalize
    _transform_folder_normalize(fm, rpt, run_rpt.category_counts, rel_path)

    # T2/T3/T5: tag normalization (loose → remove or related)
    _transform_tags(fm, rpt, run_rpt.category_counts, basenames, rel_path)

    # T4: report missing entidad/* tag (inference deferred — content-judgment required)
    _report_missing_entidad_tag(fm, rpt, run_rpt.category_counts, rel_path)

    # T10: wikilink quoting in relation fields
    _transform_wikilink_quoting(fm, rpt, run_rpt.category_counts)

    # Reconstruct content
    new_fm_text = _dump_yaml(fm)
    new_content = pre + new_fm_text + "\n---" + rest

    # T9: @[...] syntax in body (after frontmatter)
    fm_end = len(pre) + len(new_fm_text) + len("\n---")
    new_content = _transform_at_syntax(new_content, fm_end, rpt, run_rpt.category_counts)

    if rpt.changed:
        run_rpt.category_counts["files_changed"] = (
            run_rpt.category_counts.get("files_changed", 0) + 1
        )
        if not dry_run:
            fpath.write_text(new_content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def print_report(run_rpt: RunReport, dry_run: bool, skipped_files: list[str] | None = None) -> None:
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"\n{'='*70}")
    print(f"  SyV metadata migration — {mode}")
    print(f"{'='*70}\n")

    # (a) Field-name frequency BEFORE
    print("### (a) Field-name frequency BEFORE\n")
    print(f"  {'Count':>5}  Field")
    print(f"  {'-----':>5}  -----")
    for k, v in sorted(run_rpt.field_freq_before.items(), key=lambda x: -x[1]):
        print(f"  {v:>5}  {k}")
    print()

    # (b) Tag-value frequency BEFORE
    print("### (b) Tag-value frequency BEFORE\n")
    print(f"  {'Count':>5}  Tag")
    print(f"  {'-----':>5}  ---")
    for k, v in sorted(run_rpt.tag_freq_before.items(), key=lambda x: -x[1]):
        print(f"  {v:>5}  {k}")
    print()

    # (c) Files-changed count per transform category
    print("### (c) Changes per transform category\n")
    cat_order = [
        "files_changed",
        "field_rename",
        "key_conflict",
        "spoiler_migrate",
        "tag_add",
        "tag_normalize",
        "tag_remove",
        "tag_to_related",
        "tag_infer_entidad",
        "folder_normalize",
        "folder_set",
        "at_syntax",
        "missing_title",
        "missing_description",
        "missing_folder",
        "missing_entidad",
        "non_wikilink_display",
    ]
    for cat in cat_order:
        v = run_rpt.category_counts.get(cat, 0)
        if v:
            print(f"  {v:>5}  {cat}")
    print()

    # (d) Full residual report
    print("### (d) Residual report\n")

    warnings_by_type: dict[str, list[str]] = defaultdict(list)
    files_with_transforms: list[FileReport] = []

    for fr in run_rpt.file_reports:
        if fr.transforms:
            files_with_transforms.append(fr)
        for w in fr.warnings:
            tag = w.split(":")[0]
            warnings_by_type[tag].append(f"  {fr.rel_path}\n      {w}")

    if run_rpt.parse_errors:
        print(f"#### Parse errors ({len(run_rpt.parse_errors)})\n")
        for e in run_rpt.parse_errors:
            print(f"  {e}")
        print()

    for wtype, items in sorted(warnings_by_type.items()):
        print(f"#### {wtype} ({len(items)})\n")
        for item in items:
            print(item)
        print()

    if dry_run and files_with_transforms:
        print(f"#### Files with proposed transforms ({len(files_with_transforms)})\n")
        for fr in files_with_transforms:
            print(f"  {fr.rel_path}")
            for t in fr.transforms:
                print(f"      {t}")
        print()

    if skipped_files:
        print(f"#### skipped: out-of-scope ({len(skipped_files)} files — _skills/ excluded from migration)\n")
        for sf in skipped_files:
            print(f"  {sf}")
        print()

    total_files = len(run_rpt.file_reports)
    changed = run_rpt.category_counts.get("files_changed", 0)
    print(f"Total .md scanned : {total_files}")
    print(f"Files with changes: {changed}")
    print(f"Mode              : {mode}")
    if dry_run:
        print("\nNo corpus files were modified. Run with --apply to write changes.")
    else:
        print(f"\n{changed} file(s) written.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="SyV vault frontmatter migration tool"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Report proposed changes without writing (default)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help="Write changes to corpus files",
    )
    args = parser.parse_args()

    dry_run = not args.apply

    files = collect_files(VAULT_ROOT)
    basenames = collect_basenames(files)
    skipped = collect_skipped_files(VAULT_ROOT)
    run_rpt = RunReport()

    for fpath in files:
        process_file(fpath, VAULT_ROOT, basenames, dry_run, run_rpt)

    print_report(run_rpt, dry_run, skipped_files=skipped)


if __name__ == "__main__":
    main()
