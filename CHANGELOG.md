# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-04-22

### Added

* Introduce the `parse_file_content` function as an alternative to the `read_file` decorator.
  The `parse_file_content` function provides equivalent functionality to the `read_file` decorator but in a
  more versatile and widely applicable form.

### Deprecated

* Deprecate the `read_file` decorator in favor of the `parse_file_content` function. 
The `read_file` decorator is no longer recommended for use and will be removed in a future release. 
Users are encouraged to migrate to the `parse_file_content` function for file parsing functionality.

## [1.0.2] - 2024-03-27

### Changed

* Fix the issue, where the `@stopwatch` decorator, when used on recursive functions,
  would start a new timer for each recursive call. Now, the decorator will only
  start a timer for the first call and return the total time taken by the function
  and all its recursive calls.

## [1.0.1] - 2024-03-04

### Changed

* Update project links in `pyproject.toml`.

## [1.0.0] - 2024-03-03

### Added

* Official release of the package.
