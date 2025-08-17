#!/usr/bin/env python3
# sqlite_to_mermaid.py
# Usage: python sqlite_to_mermaid.py path/to.db > erd.mmd

import sqlite3, sys, re, pathlib

def sanitize(name: str) -> str:
    # Mermaid 식별자에 안전하도록 간단 정제(공백/기타 문자 -> _)
    s = re.sub(r'[^0-9a-zA-Z_]', '_', name)
    if re.match(r'^\d', s):  # 숫자로 시작하면 접두사
        s = '_' + s
    return s

def get_tables(cur):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
    return [r[0] for r in cur.fetchall()]

def get_columns(cur, tbl):
    cur.execute(f"PRAGMA table_info('{tbl}')")
    # cid, name, type, notnull, dflt_value, pk
    cols = []
    for cid, name, ctype, notnull, dflt, pk in cur.fetchall():
        cols.append({
            "name": name,
            "type": (ctype or "TEXT").upper(),
            "notnull": bool(notnull),
            "pk": pk > 0
        })
    return cols

def get_fk_list(cur, tbl):
    cur.execute(f"PRAGMA foreign_key_list('{tbl}')")
    # id, seq, table, from, to, on_update, on_delete, match
    fks = []
    for _, _, ref_table, from_col, to_col, *_ in cur.fetchall():
        fks.append({
            "child_table": tbl,
            "child_col": from_col,
            "parent_table": ref_table,
            "parent_col": to_col or "id"  # SQLite에서 to 생략 시 PK로 가정
        })
    return fks

def build_notnull_map(columns):
    return {c["name"]: c["notnull"] for c in columns}

def main(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    tables = get_tables(cur)
    table_cols = {t: get_columns(cur, t) for t in tables}
    fk_edges = []
    for t in tables:
        fk_edges.extend(get_fk_list(cur, t))

    print("erDiagram")
    print(f"  %% Auto-generated from {pathlib.Path(db_path).name}")

    # 테이블 정의
    for t in tables:
        t_id = sanitize(t)
        print(f"  {t_id} {{")
        for col in table_cols[t]:
            pk = " PK" if col["pk"] else ""
            ctype = col["type"] or "TEXT"
            cname = sanitize(col["name"])
            print(f"    {ctype} {cname}{pk}")
        print("  }")

    # 관계(부모 1 : 자식 N)
    for fk in fk_edges:
        parent = sanitize(fk["parent_table"])
        child  = sanitize(fk["child_table"])
        child_notnull = build_notnull_map(table_cols[fk["child_table"]]).get(fk["child_col"], False)
        many_mark = "|{" if child_notnull else "o{"
        label = f'{sanitize(fk["child_col"])}->{sanitize(fk["parent_col"])}'
        print(f"  {parent} ||--{many_mark} {child} : {label}")

    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python sqlite_to_mermaid.py path/to.db > erd.mmd\n")
        sys.exit(1)
    main(sys.argv[1])
