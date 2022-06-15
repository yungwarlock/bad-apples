# Bad Apples

Bad apples periodically kills unwanted processes running in vm instance

# Quickstart

Install to your computer

```sh
python setup.py install
```

Running the app
```sh
bad_apples -c bad_apples.txt -d
```

# Setup

Install dev dependencies

```sh
sudo apt install -y devscripts debhelper build-essential dh-python python3-all
```

Build the debian package
```sh
debuild -b -us -uc
```

It will be built at `../<your-root-folder>`

The packages can then be installed into your VMs using packer, ansible or what you use
  
