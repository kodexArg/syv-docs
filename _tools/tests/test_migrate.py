#!/usr/bin/env python3
"""
Tests for migrate_metadata.py transforms.

Run with: uv run python _tools/tests/test_migrate.py
or: uv run pytest _tools/tests/test_migrate.py -v

Each test exercises a specific transform (T1–T11) on fixture .md content.
Idempotency is verified by processing each fixture twice and asserting zero
additional changes on the second pass.
"""
from __future__ import annotations

import io
import re
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Allow importing migrate_metadata from sibling directory
sys.path.insert(0, str(Path(__file__).parent.parent))

import migrate_metadata as mm

# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------


def _run_on_content(
    content: str,
    rel_path: str = "3_personajes/principais/x.md",
    toggles: mm.Toggles | None = None,
) -> tuple[str, mm.FileReport, mm.RunReport]:
    """Run the full transform pipeline on raw .md content via process_file.

    Writes to a temp file under a fake vault root mirroring rel_path so that
    process_file sees the same ordering/toggles the CLI uses, then returns
    (new_content, file_report, run_report). Dry-run, so the file is never written.
    """
    import tempfile

    run_rpt = mm.RunReport()
    if toggles is None:
        # Default for legacy tests: legacy-only pipeline (matches pre-N behavior).
        toggles = mm.Toggles(
            legacy=True,
            fix_string_tags=False,
            normalize_stragglers=False,
            dimensions_to_fields=False,
        )

    # Collect basenames from fixtures dir for realistic tests
    fixture_dir = Path(__file__).parent / "fixtures"
    basenames: set[str] = (
        {f.stem for f in fixture_dir.glob("*.md")} if fixture_dir.exists() else set()
    )

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fpath = root / rel_path
        fpath.parent.mkdir(parents=True, exist_ok=True)
        fpath.write_text(content, encoding="utf-8")

        # Capture the produced content by intercepting the write: run in dry-run
        # and reconstruct via the same internals process_file uses. Simplest is
        # to run process_file with apply against the temp file, then read it back.
        mm.process_file(fpath, root, basenames, dry_run=False, run_rpt=run_rpt, toggles=toggles)
        new_content = fpath.read_text(encoding="utf-8")

    rpt = run_rpt.file_reports[0]
    return new_content, rpt, run_rpt


def _assert_idempotent(
    content: str,
    rel_path: str = "3_personajes/principals/x.md",
    toggles: mm.Toggles | None = None,
) -> None:
    """Assert that running twice produces no additional changes on the second pass."""
    result1, rpt1, _ = _run_on_content(content, rel_path, toggles)
    result2, rpt2, _ = _run_on_content(result1, rel_path, toggles)
    assert result1 == result2, (
        f"Not idempotent!\n"
        f"Pass-2 transforms: {rpt2.transforms}\n"
        f"Pass-2 warnings:   {rpt2.warnings}\n"
        f"--- pass1 result ---\n{result1}\n"
        f"--- pass2 result ---\n{result2}"
    )


def _fm_of(content: str) -> dict:
    split = mm._split_content(content)
    assert split
    return mm._load_yaml(split[1])


# ---------------------------------------------------------------------------
# Individual transform tests
# ---------------------------------------------------------------------------

PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"
_results: list[tuple[str, bool, str]] = []


def run_test(name: str, fn) -> None:
    try:
        fn()
        _results.append((name, True, ""))
        print(f"  {PASS}  {name}")
    except Exception as exc:
        _results.append((name, False, str(exc)))
        print(f"  {FAIL}  {name}")
        print(f"         {exc}")


# T7: Spanish field names
def test_spanish_fields():
    content = textwrap.dedent("""\
        ---
        titulo: Mi Titulo
        carpeta: 3_personajes/principales
        descripcion: Una descripcion.
        tags:
          - entidad/personaje
        ---

        Body.
        """)
    result, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md")
    fm = _fm_of(result)
    assert "title" in fm and fm["title"] == "Mi Titulo", f"title not set: {fm}"
    assert "folder" in fm, f"folder not set: {fm}"
    assert "description" in fm, f"description not set: {fm}"
    assert "titulo" not in fm, f"titulo still present: {fm}"
    assert "carpeta" not in fm, f"carpeta still present: {fm}"
    assert "descripcion" not in fm, f"descripcion still present: {fm}"
    assert any("field-rename" in t for t in rpt.transforms)
    _assert_idempotent(content, "3_personajes/principales/x.md")


# T7: conflict detection (existing 'title' + 'titulo')
def test_spanish_field_conflict():
    content = textwrap.dedent("""\
        ---
        title: Original
        titulo: Duplicado
        folder: 3_personajes/principales
        description: Desc.
        tags:
          - entidad/personaje
        ---

        Body.
        """)
    _, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md")
    assert any("key-conflict" in w for w in rpt.warnings), f"no conflict warning: {rpt.warnings}"


# T6: spoiler migration
def test_spoiler_migrate():
    content = textwrap.dedent("""\
        ---
        title: Secreto
        folder: 3_personajes/principales
        description: Con secreto.
        alerta-spoilers: "Su lealtad final."
        tags:
          - entidad/personaje
        ---

        Body.
        """)
    result, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md")
    fm = _fm_of(result)
    assert "spoilers" in fm, f"spoilers not migrated: {fm}"
    assert "alerta-spoilers" not in fm, f"legacy key remains: {fm}"
    assert isinstance(fm["spoilers"], list), "spoilers not a list"
    tags = mm._get_tags_list(fm)
    assert "alcance/secreto" in tags, f"alcance/secreto not added: {tags}"
    _assert_idempotent(content, "3_personajes/principales/x.md")


# T6: alerta-spoiler (singular)
def test_spoiler_migrate_singular():
    content = textwrap.dedent("""\
        ---
        title: Secreto2
        folder: 3_personajes/principales
        description: Otro secreto.
        alerta-spoiler: "Un dato sensible."
        tags:
          - entidad/personaje
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md")
    fm = _fm_of(result)
    assert "spoilers" in fm
    assert "alerta-spoiler" not in fm
    _assert_idempotent(content, "3_personajes/principales/x.md")


# T2/T5: loose theme-word tags → remove
def test_loose_tag_remove():
    content = textwrap.dedent("""\
        ---
        title: Trasfondo Index
        folder: 1_trasfondo
        description: Index.
        tags:
          - trasfondo
          - cosmovision
          - historia
          - entidad/concepto
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "1_trasfondo/index.md")
    fm = _fm_of(result)
    tags = mm._get_tags_list(fm)
    assert "trasfondo" not in tags, f"trasfondo still in tags: {tags}"
    assert "cosmovision" not in tags, f"cosmovision still in tags: {tags}"
    assert "historia" not in tags, f"historia still in tags: {tags}"
    assert "entidad/concepto" in tags, f"valid tag removed: {tags}"
    assert any("tag-remove" in t for t in rpt.transforms)
    _assert_idempotent(content, "1_trasfondo/index.md")


# T3: old-path tags → remove
def test_old_path_tags_remove():
    content = textwrap.dedent("""\
        ---
        title: Codex Index
        folder: 1_trasfondo/codex
        description: Codex.
        tags:
          - trasfondo/codex/anatema-mecanico
          - trasfondo/codex/constitucion-argentina
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "1_trasfondo/codex/index.md")
    fm = _fm_of(result)
    tags = mm._get_tags_list(fm)
    assert not any(t.startswith("trasfondo/codex/") for t in tags), f"old-path tags remain: {tags}"
    _assert_idempotent(content, "1_trasfondo/codex/index.md")


# T5: loose tag that IS a basename → move to related
def test_loose_tag_to_related():
    # t02_tag_normalize is a basename in fixtures
    content = textwrap.dedent("""\
        ---
        title: Con Basename Tag
        folder: 1_trasfondo/facciones
        description: Tiene tag-como-basename.
        tags:
          - entidad/faccion
          - t02_tag_normalize
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "1_trasfondo/facciones/x.md")
    fm = _fm_of(result)
    tags = mm._get_tags_list(fm)
    assert "t02_tag_normalize" not in tags, f"tag-as-basename still in tags: {tags}"
    related = [str(r) for r in (fm.get("related") or [])]
    assert "[[t02_tag_normalize]]" in related, f"not moved to related: {related}"
    _assert_idempotent(content, "1_trasfondo/facciones/x.md")


# T4: folder→entidad inference is REMOVED; missing entidad tag → warning only, no transform
def test_missing_entidad_tag_reported_not_inferred():
    content = textwrap.dedent("""\
        ---
        title: Sin Entidad
        folder: 3_personajes/principales
        description: No tiene entidad tag.
        tags:
          - alcance/publico
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md")
    fm = _fm_of(result)
    tags = mm._get_tags_list(fm)
    # Must NOT be inferred — only reported
    assert "entidad/personaje" not in tags, f"entidad/personaje was auto-inferred (should not be): {tags}"
    assert not any("tag-infer-entidad" in t for t in rpt.transforms), (
        f"infer transform fired (should not): {rpt.transforms}"
    )
    assert any("missing-entidad-tag" in w for w in rpt.warnings), (
        f"no missing-entidad-tag warning: {rpt.warnings}"
    )
    _assert_idempotent(content, "3_personajes/principales/x.md")


# T4: any file without entidad/* → warning (regardless of folder)
def test_missing_entidad_tag_any_folder():
    content = textwrap.dedent("""\
        ---
        title: Ambiguous
        folder: 5_aventuras
        description: No clear entity type.
        tags:
          - alcance/publico
        ---
        Body.
        """)
    _, rpt, _ = _run_on_content(content, "5_aventuras/index.md")
    assert any("missing-entidad-tag" in w for w in rpt.warnings), f"no warning: {rpt.warnings}"


# T8: folder normalization
def test_folder_normalize():
    content = textwrap.dedent("""\
        ---
        title: Folder Wrong
        folder: 3_personajes/wrong_sub
        description: Folder mismatch.
        tags:
          - entidad/personaje
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md")
    fm = _fm_of(result)
    assert fm["folder"] == "3_personajes/principales", f"folder not normalized: {fm['folder']}"
    assert any("folder-normalize" in t for t in rpt.transforms)
    _assert_idempotent(content, "3_personajes/principales/x.md")


# T11: missing folder auto-derive
def test_folder_auto_derive():
    content = textwrap.dedent("""\
        ---
        title: No Folder
        description: Sin carpeta.
        tags:
          - entidad/personaje
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md")
    fm = _fm_of(result)
    assert fm.get("folder") == "3_personajes/principales", f"folder not derived: {fm}"
    _assert_idempotent(content, "3_personajes/principales/x.md")


# T11: missing title/description → warning only, not fabricated
def test_missing_title_description_reported():
    content = textwrap.dedent("""\
        ---
        folder: 3_personajes/principales
        tags:
          - entidad/personaje
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md")
    fm = _fm_of(result)
    assert "title" not in fm or fm.get("title") is None, "title was fabricated"
    assert any("missing-title" in w for w in rpt.warnings)
    assert any("missing-description" in w for w in rpt.warnings)


# T9: @[...] bare text in body → [[basename]]
def test_at_syntax_body_bare():
    content = textwrap.dedent("""\
        ---
        title: At Test
        folder: 0_proyecto
        description: Body has at-syntax.
        tags:
          - entidad/guia
        ---

        Ver @[some/path/docs.md] para mas info. Y @[otro/archivo.md].
        """)
    result, rpt, _ = _run_on_content(content, "0_proyecto/x.md")
    assert "@[" not in result, f"@[ still in result:\n{result}"
    assert "[[docs]]" in result, f"[[docs]] not in result:\n{result}"
    assert "[[archivo]]" in result, f"[[archivo]] not in result:\n{result}"
    assert any("at-syntax" in t for t in rpt.transforms)
    _assert_idempotent(content, "0_proyecto/x.md")


# T9: @[...] inside inline code span → NOT transformed
def test_at_syntax_inside_inline_code_not_transformed():
    content = textwrap.dedent("""\
        ---
        title: At Inline Code Test
        folder: 0_proyecto
        description: At-syntax inside backticks must be left alone.
        tags:
          - entidad/guia
        ---

        Use `@[ruta.md]` syntax to reference files. But @[bare.md] should change.
        """)
    result, rpt, _ = _run_on_content(content, "0_proyecto/x.md")
    # The backtick-protected occurrence must survive unchanged
    assert "`@[ruta.md]`" in result, f"inline-code @[...] was incorrectly transformed:\n{result}"
    # The bare occurrence must be transformed
    assert "[[bare]]" in result, f"bare @[...] was NOT transformed:\n{result}"
    _assert_idempotent(content, "0_proyecto/x.md")


# T9: @[...] inside fenced code block → NOT transformed
def test_at_syntax_inside_fence_not_transformed():
    content = textwrap.dedent("""\
        ---
        title: At Fence Test
        folder: 0_proyecto
        description: At-syntax inside a fence must be left alone.
        tags:
          - entidad/guia
        ---

        Example:

        ```
        @[ruta.md] is used like this
        ```

        But @[bare.md] outside the fence should change.
        """)
    result, rpt, _ = _run_on_content(content, "0_proyecto/x.md")
    # Inside fence: must survive
    assert "@[ruta.md]" in result, f"fenced @[...] was incorrectly transformed:\n{result}"
    # Outside fence: must be replaced
    assert "[[bare]]" in result, f"bare @[...] was NOT transformed:\n{result}"
    _assert_idempotent(content, "0_proyecto/x.md")


# T9: all @[...] inside code → zero transforms
def test_at_syntax_all_in_code_no_transform():
    content = textwrap.dedent("""\
        ---
        title: At All Code Test
        folder: 0_proyecto
        description: All occurrences inside code.
        tags:
          - entidad/guia
        ---

        See `@[ruta.md]` for details.
        """)
    result, rpt, _ = _run_on_content(content, "0_proyecto/x.md")
    assert "`@[ruta.md]`" in result, f"protected @[...] was transformed:\n{result}"
    assert not any("at-syntax" in t for t in rpt.transforms), (
        f"at-syntax transform fired on code-only content: {rpt.transforms}"
    )
    _assert_idempotent(content, "0_proyecto/x.md")


# Idempotency on already-valid file
def test_idempotent_already_valid():
    content = textwrap.dedent("""\
        ---
        title: Already Valid
        folder: 3_personajes/principales
        description: Todo en orden.
        aliases:
          - Valid
        tags:
          - entidad/personaje
          - alcance/publico
          - estado/canon
        related:
          - "[[otro-personaje]]"
        ---

        Body unchanged.
        """)
    _assert_idempotent(content, "3_personajes/principales/x.md")
    _, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md")
    assert not rpt.transforms, f"Valid file had transforms: {rpt.transforms}"


# T10: wikilink quoting — non-wikilink display name reported
def test_non_wikilink_display_name_reported():
    content = textwrap.dedent("""\
        ---
        title: Display Name Test
        folder: 3_personajes/principales
        description: Con display name en facciones.
        facciones:
          - Sagrada Inquisicion Argentina
          - "[[iglesia-de-darsena]]"
        tags:
          - entidad/personaje
        ---
        Body.
        """)
    _, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md")
    assert any("non-wikilink-display" in w for w in rpt.warnings), (
        f"no non-wikilink-display warning: {rpt.warnings}"
    )
    _assert_idempotent(content, "3_personajes/principales/x.md")


# T6 + T4: spoilers trigger alcance/secreto; idempotent
def test_spoiler_adds_secreto_tag_idempotent():
    content = textwrap.dedent("""\
        ---
        title: Secreto Idempotent
        folder: 3_personajes/principales
        description: Desc.
        alerta-spoiler: "Dato sensible."
        tags:
          - entidad/personaje
          - alcance/publico
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md")
    fm = _fm_of(result)
    tags = mm._get_tags_list(fm)
    assert "alcance/secreto" in tags
    _assert_idempotent(content, "3_personajes/principales/x.md")


# Emit style: folder-normalize must change ONLY the folder line — no quote/indent churn
def test_no_churn_on_folder_normalize():
    # Content mirrors the exact byte style of the corpus: 2-space list indent,
    # double-quoted wikilinks, plain scalars. Only folder is wrong.
    content = (
        "---\n"
        "title: Cronología\n"
        "folder: 1_trasfondo/wrong\n"
        "description: Registro completo.\n"
        "aliases:\n"
        "  - Cronología\n"
        "related:\n"
        '  - "[[anatema-mecanico]]"\n'
        '  - "[[inquisicion]]"\n'
        "tags:\n"
        "  - entidad/concepto\n"
        "  - alcance/publico\n"
        "sidebar:\n"
        "  order: 999\n"
        "---\n"
        "\n"
        "Body text.\n"
    )
    result, rpt, _ = _run_on_content(content, "1_trasfondo/x.md")

    # Exactly one transform: folder-normalize
    assert rpt.transforms == ["folder-normalize: '1_trasfondo/wrong' → '1_trasfondo'"], (
        f"unexpected transforms: {rpt.transforms}"
    )

    # Build expected: only the folder line changed, everything else byte-identical
    expected = content.replace(
        "folder: 1_trasfondo/wrong\n",
        "folder: 1_trasfondo\n",
    )
    assert result == expected, (
        "YAML churn detected — output differs beyond the folder line:\n"
        + _show_diff(expected, result)
    )
    _assert_idempotent(content, "1_trasfondo/x.md")


def _show_diff(expected: str, got: str) -> str:
    """Return a compact line-diff for assertion messages."""
    exp_lines = expected.splitlines(keepends=True)
    got_lines = got.splitlines(keepends=True)
    lines = []
    for i, (e, g) in enumerate(zip(exp_lines, got_lines), 1):
        if e != g:
            lines.append(f"  line {i}: expected {repr(e)}")
            lines.append(f"  line {i}:      got {repr(g)}")
    if len(exp_lines) != len(got_lines):
        lines.append(f"  line count: expected {len(exp_lines)}, got {len(got_lines)}")
    return "\n".join(lines) if lines else "(no line diff found — check whitespace)"


# ---------------------------------------------------------------------------
# New transforms (N1 fix-string-tags, N2 normalize-stragglers, N3 dims-to-fields)
# ---------------------------------------------------------------------------

# All-new-transforms toggles, legacy OFF, so each test isolates the new behavior.
_N = mm.Toggles(
    legacy=False,
    fix_string_tags=True,
    normalize_stragglers=True,
    dimensions_to_fields=True,
)
# fix-string-tags in isolation
_N1 = mm.Toggles(legacy=False, fix_string_tags=True,
                 normalize_stragglers=False, dimensions_to_fields=False)
# normalize-stragglers in isolation
_N2 = mm.Toggles(legacy=False, fix_string_tags=False,
                 normalize_stragglers=True, dimensions_to_fields=False)
# dimensions-to-fields in isolation
_N3 = mm.Toggles(legacy=False, fix_string_tags=False,
                 normalize_stragglers=False, dimensions_to_fields=True)


# N1: tags as a flow-string '["entidad/guia"]' → real list
def test_fix_string_tags():
    content = textwrap.dedent("""\
        ---
        title: Cartas
        folder: 4_diegesis/cartas
        description: Indice de cartas.
        tags: '["entidad/guia"]'
        ---

        Body.
        """)
    result, rpt, _ = _run_on_content(content, "4_diegesis/cartas/cartas.md", _N1)
    fm = _fm_of(result)
    assert isinstance(fm["tags"], list), f"tags not a list: {fm['tags']!r}"
    assert fm["tags"] == ["entidad/guia"], f"tags wrong: {fm['tags']!r}"
    assert any("fix-string-tags" in t for t in rpt.transforms)
    _assert_idempotent(content, "4_diegesis/cartas/cartas.md", _N1)


# N1: multi-value flow-string with quotes → list
def test_fix_string_tags_multi():
    content = textwrap.dedent("""\
        ---
        title: X
        folder: 4_diegesis/cartas
        description: D.
        tags: '["entidad/guia", "alcance/publico"]'
        ---
        Body.
        """)
    result, _, _ = _run_on_content(content, "4_diegesis/cartas/x.md", _N1)
    fm = _fm_of(result)
    assert fm["tags"] == ["entidad/guia", "alcance/publico"], f"got {fm['tags']!r}"


# N1: a plain single-word string tag is NOT touched by fix-string-tags
def test_fix_string_tags_ignores_plain_scalar():
    content = textwrap.dedent("""\
        ---
        title: X
        folder: 4_diegesis/cartas
        description: D.
        tags: entidad/guia
        ---
        Body.
        """)
    _, rpt, _ = _run_on_content(content, "4_diegesis/cartas/x.md", _N1)
    assert not any("fix-string-tags" in t for t in rpt.transforms), (
        f"fix-string-tags fired on plain scalar: {rpt.transforms}"
    )


# N1 → N3 pipeline: string tags fixed, THEN promoted to a field
def test_fix_string_tags_then_dimensions():
    content = textwrap.dedent("""\
        ---
        title: Cronicas
        folder: 4_diegesis/cronicas
        description: Indice.
        tags: '["entidad/guia"]'
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "4_diegesis/cronicas/cronicas.md", _N)
    fm = _fm_of(result)
    assert fm.get("entidad") == "guia", f"entidad field not set: {fm}"
    assert fm["tags"] == [], f"tags should be empty list: {fm['tags']!r}"
    _assert_idempotent(content, "4_diegesis/cronicas/cronicas.md", _N)


# N2: faccion (typo) → facciones
def test_straggler_rename_faccion():
    content = textwrap.dedent("""\
        ---
        title: Personaje
        folder: 3_personajes/principales
        description: D.
        faccion:
          - "[[inquisicion]]"
        tags:
          - entidad/personaje
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md", _N2)
    fm = _fm_of(result)
    assert "faccion" not in fm, f"typo key remains: {fm}"
    assert "facciones" in fm, f"facciones not set: {fm}"
    assert [str(v) for v in fm["facciones"]] == ["[[inquisicion]]"], f"value lost: {fm['facciones']}"
    assert any("straggler-rename" in t for t in rpt.transforms)
    _assert_idempotent(content, "3_personajes/principales/x.md", _N2)


# N2: faccion rename when facciones already present → conflict, no clobber
def test_straggler_rename_conflict():
    content = textwrap.dedent("""\
        ---
        title: Personaje
        folder: 3_personajes/principales
        description: D.
        faccion:
          - "[[a]]"
        facciones:
          - "[[b]]"
        tags:
          - entidad/personaje
        ---
        Body.
        """)
    _, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md", _N2)
    assert any("straggler-conflict" in w for w in rpt.warnings), f"no conflict warning: {rpt.warnings}"


# N2: faccion whose value is a MAPPING (stats blob) → NOT renamed, flagged instead
def test_straggler_rename_skips_mapping():
    content = textwrap.dedent("""\
        ---
        title: Menores
        folder: 1_trasfondo/facciones/facciones-menores
        description: D.
        faccion:
          tipo: Variado
          alcance: Local/Regional
          regiones:
            - Ciudad Dársena
        tags: []
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "1_trasfondo/facciones/facciones-menores/x.md", _N2)
    fm = _fm_of(result)
    assert "faccion" in fm, f"mapping-valued 'faccion' was renamed (must be left): {fm}"
    assert "facciones" not in fm, f"facciones must NOT be created from a mapping: {fm}"
    assert isinstance(fm["faccion"], dict), f"value type changed: {fm['faccion']!r}"
    assert not any("straggler-rename:" in t for t in rpt.transforms), (
        f"rename fired on mapping: {rpt.transforms}"
    )
    assert any("straggler-rename-skipped" in w for w in rpt.warnings), (
        f"no skip warning: {rpt.warnings}"
    )
    _assert_idempotent(content, "1_trasfondo/facciones/facciones-menores/x.md", _N2)


# N2: 1-use keys flagged, never deleted
def test_straggler_flag_keys():
    content = textwrap.dedent("""\
        ---
        title: X
        folder: 1_trasfondo
        description: D.
        status: borrador
        type: cosa
        fechas-clave:
          - 2099
        personajes-historicos:
          - "[[alguien]]"
        tags:
          - entidad/concepto
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "1_trasfondo/x.md", _N2)
    fm = _fm_of(result)
    for k in ("status", "type", "fechas-clave", "personajes-historicos"):
        assert k in fm, f"flagged key '{k}' was deleted (must be left): {fm}"
        assert any(f"'{k}'" in w and "straggler-flag" in w for w in rpt.warnings), (
            f"no flag warning for '{k}': {rpt.warnings}"
        )
    _assert_idempotent(content, "1_trasfondo/x.md", _N2)


# N3: the big one — three dimensions promoted, tags emptied to []
def test_dimensions_to_fields_full():
    content = textwrap.dedent("""\
        ---
        title: Personaje
        folder: 3_personajes/principales
        description: D.
        aliases:
          - P
        tags:
          - entidad/personaje
          - alcance/secreto
          - estado/canon
        related:
          - "[[otro]]"
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "3_personajes/principales/x.md", _N3)
    fm = _fm_of(result)
    assert fm.get("entidad") == "personaje", f"entidad: {fm}"
    assert fm.get("alcance") == "secreto", f"alcance: {fm}"
    assert fm.get("estado") == "canon", f"estado: {fm}"
    assert fm["tags"] == [], f"tags not empty: {fm['tags']!r}"
    assert sum(1 for t in rpt.transforms if "dimension-to-field" in t) == 3
    _assert_idempotent(content, "3_personajes/principales/x.md", _N3)


# N3: non-dimensional tags stay in the nursery
def test_dimensions_keeps_nursery_tags():
    content = textwrap.dedent("""\
        ---
        title: X
        folder: 1_trasfondo
        description: D.
        tags:
          - entidad/concepto
          - misterio-emergente
        ---
        Body.
        """)
    result, _, _ = _run_on_content(content, "1_trasfondo/x.md", _N3)
    fm = _fm_of(result)
    assert fm.get("entidad") == "concepto"
    assert fm["tags"] == ["misterio-emergente"], f"nursery tag lost: {fm['tags']!r}"


# N3: field ordering — entidad/alcance/estado sit right after description
def test_dimensions_field_order():
    content = textwrap.dedent("""\
        ---
        title: X
        folder: 1_trasfondo
        description: D.
        aliases:
          - X
        tags:
          - entidad/concepto
          - alcance/publico
          - estado/canon
        ---
        Body.
        """)
    result, _, _ = _run_on_content(content, "1_trasfondo/x.md", _N3)
    fm = _fm_of(result)
    keys = list(fm.keys())
    di = keys.index("description")
    # The three dimension fields immediately follow description, in canonical order.
    assert keys[di + 1: di + 4] == ["entidad", "alcance", "estado"], f"bad order: {keys}"


# N3: two entidad/* values → conflict, no guess, tags untouched-for-that-tree
def test_dimensions_conflict_no_guess():
    content = textwrap.dedent("""\
        ---
        title: X
        folder: 1_trasfondo
        description: D.
        tags:
          - entidad/concepto
          - entidad/faccion
        ---
        Body.
        """)
    result, rpt, _ = _run_on_content(content, "1_trasfondo/x.md", _N3)
    fm = _fm_of(result)
    assert "entidad" not in fm, f"entidad field should NOT be set on conflict: {fm}"
    assert any("dimension-conflict" in w for w in rpt.warnings), f"no conflict warning: {rpt.warnings}"
    tags = mm._get_tags_list(fm)
    assert "entidad/concepto" in tags and "entidad/faccion" in tags, f"conflicting tags lost: {tags}"


# N3: already-migrated file (fields set, tags []) is a no-op
def test_dimensions_idempotent_already_migrated():
    content = textwrap.dedent("""\
        ---
        title: X
        folder: 1_trasfondo
        description: D.
        entidad: concepto
        alcance: publico
        estado: canon
        tags: []
        ---
        Body.
        """)
    _, rpt, _ = _run_on_content(content, "1_trasfondo/x.md", _N3)
    assert not rpt.transforms, f"already-migrated file had transforms: {rpt.transforms}"
    _assert_idempotent(content, "1_trasfondo/x.md", _N3)


# Full pipeline (legacy + all N): spoilers + dimensions must not churn.
# Regression: legacy spoiler-migrate re-added alcance/secreto tag, N3 re-promoted
# it to a field every pass → infinite churn. Guarded by the alcance-field check.
_FULL = mm.Toggles(legacy=True, fix_string_tags=True,
                   normalize_stragglers=True, dimensions_to_fields=True)


def test_spoilers_plus_dimensions_no_churn():
    content = textwrap.dedent("""\
        ---
        title: Secreto
        folder: 1_trasfondo/credos
        description: D.
        spoilers:
          - "Un secreto."
        tags:
          - entidad/credo
          - alcance/secreto
        ---
        Body.
        """)
    # First pass promotes alcance/secreto → field; second pass must be a no-op.
    result1, rpt1, _ = _run_on_content(content, "1_trasfondo/credos/x.md", _FULL)
    fm1 = _fm_of(result1)
    assert fm1.get("alcance") == "secreto", f"alcance not promoted: {fm1}"
    assert fm1["tags"] == ["entidad/credo"] or "alcance/secreto" not in mm._get_tags_list(fm1), (
        f"alcance/secreto should be a field, not a tag: {fm1}"
    )
    _assert_idempotent(content, "1_trasfondo/credos/x.md", _FULL)


def test_spoilers_with_publico_field_flagged_not_churned():
    content = textwrap.dedent("""\
        ---
        title: Contradiccion
        folder: 1_trasfondo/credos
        description: D.
        alcance: publico
        spoilers:
          - "Pero tiene secretos."
        tags: []
        ---
        Body.
        """)
    _, rpt, _ = _run_on_content(content, "1_trasfondo/credos/x.md", _FULL)
    assert any("spoiler-alcance-mismatch" in w for w in rpt.warnings), (
        f"no mismatch warning: {rpt.warnings}"
    )
    _assert_idempotent(content, "1_trasfondo/credos/x.md", _FULL)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def main() -> None:
    tests = [
        ("T7 spanish fields rename", test_spanish_fields),
        ("T7 spanish field conflict", test_spanish_field_conflict),
        ("T6 spoiler migrate (alerta-spoilers)", test_spoiler_migrate),
        ("T6 spoiler migrate (alerta-spoiler singular)", test_spoiler_migrate_singular),
        ("T2/T5 loose tag remove", test_loose_tag_remove),
        ("T3 old-path tags remove", test_old_path_tags_remove),
        ("T5 loose tag → related (basename match)", test_loose_tag_to_related),
        ("T4 missing entidad tag reported, NOT inferred", test_missing_entidad_tag_reported_not_inferred),
        ("T4 missing entidad tag any folder → warning", test_missing_entidad_tag_any_folder),
        ("T8 folder normalize", test_folder_normalize),
        ("T11 folder auto-derive", test_folder_auto_derive),
        ("T11 missing title/description reported", test_missing_title_description_reported),
        ("T9 @[...] bare text transforms", test_at_syntax_body_bare),
        ("T9 @[...] inside inline code NOT transformed", test_at_syntax_inside_inline_code_not_transformed),
        ("T9 @[...] inside fenced block NOT transformed", test_at_syntax_inside_fence_not_transformed),
        ("T9 all @[...] in code → zero transforms", test_at_syntax_all_in_code_no_transform),
        ("idempotency on already-valid file", test_idempotent_already_valid),
        ("T10 non-wikilink display name reported", test_non_wikilink_display_name_reported),
        ("T6+T4 spoilers → alcance/secreto idempotent", test_spoiler_adds_secreto_tag_idempotent),
        ("emit style: folder-normalize touches only folder line", test_no_churn_on_folder_normalize),
        ("N1 fix-string-tags → list", test_fix_string_tags),
        ("N1 fix-string-tags multi-value", test_fix_string_tags_multi),
        ("N1 fix-string-tags ignores plain scalar", test_fix_string_tags_ignores_plain_scalar),
        ("N1→N3 string tags fixed then promoted", test_fix_string_tags_then_dimensions),
        ("N2 straggler rename faccion→facciones (list)", test_straggler_rename_faccion),
        ("N2 straggler rename SKIPS mapping value", test_straggler_rename_skips_mapping),
        ("N2 straggler rename conflict", test_straggler_rename_conflict),
        ("N2 straggler flag 1-use keys (not deleted)", test_straggler_flag_keys),
        ("N3 dimensions-to-fields full", test_dimensions_to_fields_full),
        ("N3 dimensions keeps nursery tags", test_dimensions_keeps_nursery_tags),
        ("N3 dimensions field order", test_dimensions_field_order),
        ("N3 dimensions conflict — no guess", test_dimensions_conflict_no_guess),
        ("N3 dimensions idempotent (already migrated)", test_dimensions_idempotent_already_migrated),
        ("FULL spoilers+dimensions no churn", test_spoilers_plus_dimensions_no_churn),
        ("FULL spoilers+publico field flagged, not churned", test_spoilers_with_publico_field_flagged_not_churned),
    ]

    print(f"\n{'='*60}")
    print("  SyV migrate_metadata — test suite")
    print(f"{'='*60}\n")

    for name, fn in tests:
        run_test(name, fn)

    passed = sum(1 for _, ok, _ in _results if ok)
    failed = sum(1 for _, ok, _ in _results if not ok)
    print(f"\n{'='*60}")
    print(f"  {passed} passed, {failed} failed")
    print(f"{'='*60}\n")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
