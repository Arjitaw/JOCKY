# JOCKY Language Specification

## 1. Hash a file
Syntax:
HASH FILE <path>

Example:
HASH FILE hello.txt

Meaning:
Calculate the hash of the specified file.


## 2. Encrypt a file
Syntax:
ENCRYPT FILE <path>

Example:
ENCRYPT FILE secret.txt

Meaning:
Encrypt the specified file.


## 3. System information
Syntax:
SYSTEM INFO

Example:
SYSTEM INFO

Meaning:
Request system information.

## 4. List
Syntax:
LIST FILES <path>

Example:
LIST FILES .

Meaning:
Lists the files in current folder('.' means current)

## 5. Processes
Syntax:
PROCESSES

Example:
PROCESSES

Meaning:
Requests process information

## 6. Search file
Syntax:
SEARCH FILE <path>

Example:
SEARCH FILE <malware.exe> IN <folder>

Meaning:
searches for specific file using the provided path or the file identifier

## 7. Syntax Rules

Jocky commands must follow the syntax defined in the grammar.

Invalid or incomplete commands are rejected by the parser.

## 8. Command Summary

| Command | Syntax | Purpose |
|---|---|---|
| HASH | `HASH FILE <PATH>` | Hashes a file |
| ENCRYPT | `ENCRYPT FILE <PATH>` | Encrypts a file |
| LIST | `LIST FILES <PATH>` | Lists files in a directory |
| SYSTEM INFO | `SYSTEM INFO` | Requests system information |
| PROCESSES | `PROCESSES`| Requests process information |
| SEARCH | `SEARCH FILE <PATH`| Searches for a specific file |