# markdown-vault-syv (Corpus MCP)

SSOT del corpus `syv-docs`. Paquete: [`markdown-vault-mcp`](https://pypi.org/project/markdown-vault-mcp/) **≥ 4.1.0**.

## Instalar (debian-sid / máquina del vault)

```bash
uv tool install 'markdown-vault-mcp[all]==4.1.0' --force
```

El launcher de host (compat) vive en `/home/kodex/MCP/bin/mcp-markdown-vault-syv` y llama a `markdown-vault-mcp serve` con `SOURCE_DIR` = este repo.

## Config en el repo

- [`.mcp.json`](../../.mcp.json) — Cursor / clientes MCP (command + env).
- Estado/índice local (no se commitea): `.markdown_vault_mcp/` (ver `.gitignore`).

## Índice inicial

```bash
export MARKDOWN_VAULT_MCP_SOURCE_DIR="$(pwd)"
export MARKDOWN_VAULT_MCP_INDEX_PATH="$(pwd)/.markdown_vault_mcp/index.db"
markdown-vault-mcp index --force
```

## Preflight

En un cliente con el server montado: tool `stats` (o `get_server_info`). Sin MCP up: no usar el filesystem como SSOT de lore.

## Lectura vs escritura

`MARKDOWN_VAULT_MCP_READ_ONLY=false` (default SyV): writes + auto-index. Para co-escritura Highlightr en Obsidian, preferí edición a disco en el archivo marcado; el MCP reindexa vía file-watcher o `reindex`.

## Embeddings (opcional)

Con `MARKDOWN_VAULT_MCP_EMBEDDING_PROVIDER` + keys, se puede subir `DEFAULT_SEARCH_MODE` a `hybrid`. Sin embeddings, `keyword` alcanza para higiene de frontmatter/links.
