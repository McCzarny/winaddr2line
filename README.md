# winaddr2line

[![Build project and create release](https://github.com/McCzarny/winaddr2line/actions/workflows/build-release.yml/badge.svg)](https://github.com/McCzarny/winaddr2line/actions/workflows/build-release.yml)
![License](https://img.shields.io/github/license/McCzarny/winaddr2line)
![Version](https://img.shields.io/github/v/release/McCzarny/winaddr2line)

> addr2line for Windows

A small tool for getting symbol based on the address. The goal of the project is to provide similar functionality to addr2line for Windows. 

## Features
- Convert addresses to symbols using PDB files
- Supports multiple addresses at once
- Easy to use command-line interface

## Installation
Download the latest release from the [releases page](https://github.com/McCzarny/winaddr2line/releases).

## Usage
```
winaddr2line.exe -e <pdb file> [-f] <address>
```

### Examples
Convert a single address:
```
> winaddr2line.exe -e myapp.pdb 0x1000
D:\a\myapp\src\main.cpp:42
```

Convert a single address and show the function name:
```
> winaddr2line.exe -e myapp.pdb -f 0x1000
main
D:\a\myapp\src\main.cpp:42
```

Convert multiple addresses:
```
winaddr2line.exe -e myapp.pdb 0x1000 0x1100 0x2800
main
D:\a\myapp\src\main.cpp:42
foo
D:\a\myapp\src\main.cpp:44
Foo::bar<<lambda_de390742b4447c477e4e7f2e67523fc2> >
D:\a\myapp\src\foo.cpp:10
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
