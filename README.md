# PyDFS
Distributed File System written in Python.

## Installation
```
pip install pydfs
```

## Usage:
PyDFS is Centralized Distributed File System, which means there is a *master* and *slave* nodes.
The current implementation assumes that the system has only one master node and many slave nodes.

PyDFS supports *command line interface* (*CLI*) to interact with it.
There are 2 groups of the commands (like Docker Management Commands):
- `pydfs init` - to initialize, manage and sync nodes
- `pydfs dfs` - to interact with DFS itself (put/get data to/from it)

Let's take a closer look at these commands.

### init commands
With `pydfs init` command you can initialize master and slave nodes - it's pretty simple:
- `pydfs init master`
- `pydfs init slave --master_ip 127.0.0.1`

### dfs commands
- `pydfs dfs put --path PATH`
- `pydfs dfs get --path PATH`

## Requirements
Python >= 3.7
