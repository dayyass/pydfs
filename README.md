# PyDFS
Distributed File System written in Python.

## Installation
```
pip install dfspy
```

## Usage
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
- `pydfs init slave --master_ip [IP]`

### dfs commands
- `pydfs dfs put --path [PATH] --master_ip [IP]`
- `pydfs dfs get --path [PATH] --master_ip [IP]`

### other commands
- `pydfs --version`
- `pydfs --info`

### Docker
You can also use *docker-compose* to run multi-container application with:
- 1 master node
- 2 slave nodes
- 2 user nodes
```
docker-compose up --build
```

## Requirements
Python >= 3.7

## Citation
If you use **PyDFS** in a scientific publication, we would appreciate references to the following BibTex entry:
```bibtex
@misc{silkwayai2022pydfs,
    author       = {Dani El-Ayyass and Artem Fomin},
    title        = {Distributed File System written in Python},
    howpublished = {\url{https://github.com/silkway-ai/pydfs}},
    year         = {2022}
}
```
