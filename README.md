# Batch File Renamer

[绠€浣撲腑鏂嘳(README.zh-CN.md)

Preview, apply, and undo safe batch file renaming from the command line.

## Highlights

- Python standard library only; no runtime dependencies.
- Command-line interface and automated tests included.
- Safe defaults and clear output.
- Windows, macOS, and Linux; Python 3.10+.

## Installation

```bash
git clone https://github.com/jellywong343-sys/batch-file-renamer.git
cd batch-file-renamer
python -m pip install -e .
```

Replace `jellywong343-sys` with your GitHub username.

## Usage

```bash
batch-rename ./photos --prefix holiday- --start 1
batch-rename ./photos --prefix holiday- --apply
batch-rename ./photos --undo
```

Run `batch-rename --help` to see every option.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
batch-file-renamer/
鈹溾攢鈹€ src/batch_file_renamer/
鈹溾攢鈹€ tests/
鈹溾攢鈹€ README.md
鈹溾攢鈹€ README.zh-CN.md
鈹溾攢鈹€ pyproject.toml
鈹斺攢鈹€ LICENSE
```

## Safety

Review command output before applying changes to important files. Keep backups of irreplaceable data.

## License

MIT


