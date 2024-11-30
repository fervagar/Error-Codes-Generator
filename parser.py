#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2024 Fernando Vano Garcia <fervagar.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import argparse
import yaml
import sys

C_HEADER = """\
#ifndef ERROR_CODES_H
#define ERROR_CODES_H

// Auto-generated file. Do not edit. Changes will be overwritten.

#include <error_codes_def.h>
"""

C_FOOTER = """\
#endif // ERROR_CODES_H
"""

EC_BITS = {
    'module':    5,
    'submodule': 5,
    'error_id':  6,
}
EC_SIZE_BITS = sum(EC_BITS.values())

# ----------------------- #
START_MODULE_ID         = 1
START_SUBMODULE_ID      = 1
START_ERROR_ID          = 1
# ----------------------- #
MODULE_ID_INCREMENT     = 1
SUBMODULE_ID_INCREMENT  = 1
ERROR_ID_INCREMENT      = 1
# ----------------------- #

def calculate_mask(bits):
    return (1 << bits) - 1

def encode_error_code(module_id, submodule_id, error_id):
    module_bits = EC_BITS['module']
    submodule_bits = EC_BITS['submodule']
    error_bits = EC_BITS['error_id']

    module_mask = calculate_mask(module_bits)
    submodule_mask = calculate_mask(submodule_bits)
    error_mask = calculate_mask(error_bits)

    if module_id > module_mask:
        raise ValueError(f"Encoding error: module_id {module_id} exceeds allowed bit size of {module_bits} bits")
    if submodule_id > submodule_mask:
        raise ValueError(f"Encoding error: submodule_id {submodule_id} exceeds allowed bit size of {submodule_bits} bits")
    if error_id > error_mask:
        raise ValueError(f"Encoding error: error_id {error_id} exceeds allowed bit size of {error_bits} bits")

    return (module_id << (submodule_bits + error_bits)) | (submodule_id << error_bits) | error_id

def format_code(code):
    return f"(-0x{code:04x})"

def process_module(module_name, submodule_name, errors, module_id, submodule_id):
    return [
        (module_name, submodule_name, error_name, encode_error_code(module_id, submodule_id, error_id), error_description)
        for error_id, (error_name, error_description) in enumerate(errors.items(), START_ERROR_ID)
    ]

def validate_and_generate_error_codes(data):
    all_errors = []
    module_id = START_MODULE_ID

    for module_name, module_info in data.get('modules', {}).items():
        all_errors.extend(process_module(module_name, None, module_info.get('errors', {}), module_id, 0))

        submodule_id = START_SUBMODULE_ID
        if 'submodules' in module_info:
            for submodule_name, submodule_info in module_info['submodules'].items():
                all_errors.extend(process_module(module_name, submodule_name, submodule_info.get('errors', {}), module_id, submodule_id))
                submodule_id += SUBMODULE_ID_INCREMENT

        module_id += MODULE_ID_INCREMENT

    return format_output(all_errors)

def format_output(errors):
    max_name_length = max(len(error_name) for _, _, error_name, _, _ in errors)
    output = [C_HEADER]
    descriptions = [
        "#define EC_DEF_STRERROR_ARRAY \\",
        "static struct error_desc error_desc_array[] = { \\"
    ]

    current_module = None
    current_submodule = None

    def add_module_header(module_name):
        output.append(f"// {module_name}")
        descriptions.append(f"    /* {module_name} */\\")

    def add_submodule_header(module_name, submodule_name):
        output.append(f"// {module_name}::{submodule_name}")
        descriptions.append(f"    /* {module_name}::{submodule_name} */\\")

    for module_name, submodule_name, error_name, encoded_code, description in errors:
        if current_module != module_name:
            if current_module is not None:
                output.append("")
                # descriptions.append("")
            add_module_header(module_name)
            current_submodule = None

        if current_submodule != submodule_name and submodule_name is not None:
            output.append("")
            # descriptions.append("")
            add_submodule_header(module_name, submodule_name)

        output.append(f"#define {error_name.ljust(max_name_length + 2)} {format_code(encoded_code)}")
        descriptions.append(f"    {{{error_name}, {' ' * (max_name_length - len(error_name))}\"{description}\"}}, \\")

        current_module = module_name
        current_submodule = submodule_name

    descriptions.append("}\n")
    output.append("")
    output.extend(descriptions)
    output.append(C_FOOTER)
    return "\n".join(output)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate error codes from YAML.')
    parser.add_argument('yaml_file', type=str, help='Path to the YAML file defining error codes')
    parser.add_argument('-o', '--output', type=str, help='Output header file', default=None)
    return parser.parse_args()

def main():
    args = parse_arguments()
    try:
        with open(args.yaml_file, 'r') as file:
            data = yaml.safe_load(file)
        output_content = validate_and_generate_error_codes(data)
        if args.output:
            with open(args.output, 'w') as out_file:
                out_file.write(output_content)
            print(f"Successfully generated {args.output}", file=sys.stderr)
        else:
            sys.stdout.write(output_content)
    except Exception as e:
        print(f"Failed to generate error codes: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

