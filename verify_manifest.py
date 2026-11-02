import hashlib, json, sys
from pathlib import Path

def pairs(kv):
    d = {}
    for k, v in kv:
        if k in d:
            raise ValueError("D002_PARSE_NONDETERMINISM: duplicate key")
        d[k] = v
    return d

def verify(filename, files_dir=None):
    obj = json.loads(Path(filename).read_text(encoding="utf-8"), object_pairs_hook=pairs)
    assert set(obj) == {"files", "jason", "manifest_type", "root"}, "E_SCHEMA"
    assert obj["jason"] == "manifest/1" and obj["manifest_type"] == "content", "E_SCHEMA"
    fs = obj["files"]
    assert isinstance(fs, list) and all(type(f) == dict and set(f) == {"path", "bytes", "sha256"} for f in fs), "E_SCHEMA"
    ps = [f["path"] for f in fs]
    assert all(type(p) == str for p in ps), "E_SCHEMA"
    assert len(set(ps)) == len(ps) and all(p and not p.startswith("/") and not p.startswith("./") and not p.endswith("/") and "\\" not in p and all(seg not in (".", "..") for seg in p.split("/")) for p in ps), "E_MANIFEST_PATH"
    assert ps == sorted(ps, key=lambda p: p.encode("utf-8")), "E_MANIFEST_ORDER"
    for f in fs:
        assert type(f["bytes"]) == int and 0 <= f["bytes"] < 2**53 and type(f["sha256"]) == str and len(f["sha256"]) == 64 and all(c in "0123456789abcdef" for c in f["sha256"]), "E_SCHEMA"
        if files_dir is not None:
            b = (Path(files_dir) / f["path"]).read_bytes()
            assert len(b) == f["bytes"], "E_MANIFEST_LENGTH"
            assert hashlib.sha256(b).hexdigest() == f["sha256"], "E_MANIFEST_FILE_HASH"
    assert all(p.isascii() for p in ps), "D004_CANONICALIZATION: restricted reference only"
    body = {k: v for k, v in obj.items() if k != "root"}
    c = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    root = "sha256:" + hashlib.sha256(b"jason.manifest.v1.hash\0" + c).hexdigest()
    assert root == obj["root"], "E_MANIFEST_ROOT_MISMATCH"
    return root

if __name__ == "__main__":
    print(verify(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
