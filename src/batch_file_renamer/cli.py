from __future__ import annotations
import argparse, json, uuid
from pathlib import Path

def build_plan(directory: Path, prefix="file-", suffix="", start=1, width=3, extension=None):
    directory = directory.expanduser().resolve()
    if not directory.is_dir(): raise ValueError(f"Not a directory: {directory}")
    ext = None if not extension else (extension if extension.startswith(".") else f".{extension}").lower()
    files = sorted((p for p in directory.iterdir() if p.is_file() and p.name != "rename-manifest.json" and (ext is None or p.suffix.lower()==ext)), key=lambda p:p.name.lower())
    plan = [(source, directory/f"{prefix}{index:0{width}d}{suffix}{source.suffix}") for index,source in enumerate(files,start=start)]
    plan = [(a,b) for a,b in plan if a != b]
    targets=[b for _,b in plan]; sources={a for a,_ in plan}
    if len(targets)!=len(set(targets)): raise ValueError("Generated target names are not unique.")
    conflicts=[p for p in targets if p.exists() and p not in sources]
    if conflicts: raise ValueError(f"Target already exists: {conflicts[0].name}")
    return plan

def apply_plan(plan, manifest: Path):
    staged=[]
    try:
        for source,target in plan:
            temp=source.with_name(f".rename-{uuid.uuid4().hex}.tmp"); source.rename(temp); staged.append((source,temp,target))
        for _,temp,target in staged: temp.rename(target)
    except Exception:
        for source,temp,target in reversed(staged):
            current=target if target.exists() else temp
            if current.exists() and not source.exists(): current.rename(source)
        raise
    manifest.write_text(json.dumps([{"original":str(a),"renamed":str(b)} for a,b in plan],indent=2),encoding="utf-8")

def undo(manifest: Path):
    records=json.loads(manifest.read_text(encoding="utf-8")); staged=[]
    for item in records:
        original,renamed=Path(item["original"]),Path(item["renamed"])
        if not renamed.exists(): raise FileNotFoundError(f"Cannot undo; missing file: {renamed}")
        temp=renamed.with_name(f".undo-{uuid.uuid4().hex}.tmp"); renamed.rename(temp); staged.append((original,temp))
    for original,temp in staged: temp.rename(original)
    manifest.unlink(missing_ok=True)

def main():
    parser=argparse.ArgumentParser(description="Safely preview, apply, and undo batch renames.")
    parser.add_argument("directory",nargs="?",default="."); parser.add_argument("--prefix",default="file-"); parser.add_argument("--suffix",default="")
    parser.add_argument("--start",type=int,default=1); parser.add_argument("--width",type=int,default=3); parser.add_argument("--extension")
    parser.add_argument("--manifest",default="rename-manifest.json"); parser.add_argument("--apply",action="store_true"); parser.add_argument("--undo",action="store_true")
    args=parser.parse_args(); directory=Path(args.directory).expanduser().resolve(); manifest=directory/args.manifest
    if args.undo: undo(manifest); print("Rename successfully undone."); return
    plan=build_plan(directory,args.prefix,args.suffix,args.start,args.width,args.extension)
    if not plan: print("No files need renaming."); return
    for source,target in plan: print(f"{source.name} -> {target.name}")
    if args.apply: apply_plan(plan,manifest); print(f"Renamed {len(plan)} files. Undo manifest: {manifest}")
    else: print("Preview only. Add --apply to rename files.")
if __name__ == "__main__": main()
