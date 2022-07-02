# pydfs
Distributed File System written in Python

### Installation
```
git clone https://github.com/silkway-ai/pydfs.git
cd pydfs
pip install .
```

### Usage:
pydfs supports command line interface (CLI)

#### init commands
- `pydfs init master`
- `pydfs init slave --master_ip 127.0.0.1`

#### dfs commands
- `pydfs dfs put --path PATH`
- `pydfs dfs get --path PATH`

### Requirements
Python >= 3.7
