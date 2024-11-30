# Error Codes Generator

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview

The **Error Codes Generator** project allows you to define error codes in a structured YAML file and automatically generate corresponding C header files. This ensures consistency and ease of maintenance across your C projects.

## Features

- **YAML Configuration:** Define modules, submodules, and their associated error codes in a readable YAML format.
- **Automated Header Generation:** Use `parser.py` to parse the YAML file and generate `error_codes.h`.
- **Example Program:** An example C program demonstrates how to utilize the generated error codes.

## Project Structure

```
.
├── error_codes.c
├── error_codes_def.h
├── error_codes.yml
├── example.c
├── LICENSE
├── Makefile
└── parser.py
```

- `error_codes.yml`: YAML configuration file defining modules, submodules, and error codes.
- `parser.py`: Python script that parses `error_codes.yml` and generates `error_codes.h`.
- `error_codes.h`: Generated C header file containing defined error codes.
- `error_codes.c`: C source file related to error code handling.
- `example.c`: Example C program demonstrating the usage of error codes.
- `Makefile`: Build script to automate the generation and compilation process.
- `LICENSE`: MIT License file.

## Getting Started

### Prerequisites

- **Python 3.x**: Required to run `parser.py`.
- **GCC**: C compiler to build the example program.
- **Make**: Build automation tool.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/fervagar/Error-Codes-Generator.git
   ```

2. **Ensure `parser.py` is Executable**

   If not already executable, set the appropriate permissions:

   ```bash
   chmod +x parser.py
   ```

## Usage

### Generating `error_codes.h` and Building the Example

The Makefile automates the process of generating `error_codes.h` and compiling the example program.

1. **Build the Project**

   Simply run:

   ```bash
   make
   ```

   This command performs the following:
   - Parses `error_codes.yml` using `parser.py` to generate `error_codes.h`.
   - Compiles `example.c` and `error_codes.c` into the `example` executable.

2. **Run the Example Program**

   After a successful build, execute the example program:

   ```bash
   ./example
   ```

## Defining Error Codes

Edit the `error_codes.yml` file to define your modules, submodules, and error codes. Here's an example structure:

```yaml
# This YAML file configures modules, their errors, and submodules with their own errors.

modules:
  TestMod1:
    errors:
      E_OPEN_DEV: "Error opening device"
      E_CLOSE_DEV: "Error closing device"
    submodules:
      TestMod1SubMod1:
        errors:
          E_READ_DEV: "Error reading from device"
          E_WRITE_DEV: "Error writing to device"
  TestMod2:
    errors:
      E_INIT_MOD: "Error initializing module"
    submodules:
      TestMod2SubMod1:
        errors:
          E_CONFIG_FAIL: "Configuration failure"
```

After updating `error_codes.yml`, rebuild the project to regenerate `error_codes.h`:

```bash
make
```

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this code in both open-source and commercial projects, provided that you preserve the original license and attribution notices.
