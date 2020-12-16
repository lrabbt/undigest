# Undigest

Simple digest breaker server created as example for distributed processing. It was created for an assignment and is not intended for real life usage.

## Requirements

* Python3.8

## Instalation

Clonning from git:

```bash
git clone git@github.com:lrabbt/undigest.git
cd undigest
```

It is advisable to create and run a virtualenv before installing:

```bash
virtualenv -p python3.8 venv
source venv/bin/activate
```

Installing package:

```bash
pip install .
```

Or you can add the packages directly to $PYTHONPATH. On Linux:

```bash
export PYTHONPATH=/path/to/project/root:$PYTHONPATH
```

## Usage

Running example server with debug on:

```bash
python examples/xmlrpc_server.py
```

Running example request:

```bash
python examples/xmlrpc_client.py "http://localhost:8000" 2 6d563251c5d6f4a82c75a2b6ae0ed8ed93c6a4028f8f07442b75891d550be544 4
```

In this example, the parameters after the script name are: server url, number of workers, hex digest of message, message size. After running, you should see:

```bash
Undigested: "heyo"
```

If the package was installed with `pip`, you can also run the server with:

```bash
undigest-server
```
