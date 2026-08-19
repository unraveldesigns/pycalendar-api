# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.5.2](https://gitlab.com/ud-labs/py-calendar-api/-/releases/0.5.2) - 2026-07-17

### Documentation

- Update: Register endpoint URL in the docs.
- Add link to the main website

## [0.5.1](https://gitlab.com/ud-labs/py-calendar-api/-/releases/0.5.1) - 2026-05-15

### Documentation - CI

- fix: MkDocs CI/CD Build remove `--strict` flag: MkDocs-Material generates a warning that blocks the build with `--strict` flag.

## [0.5.0](https://gitlab.com/ud-labs/py-calendar-api/-/releases/0.5.0) - 2026-05-15

### Documentation

- Add: Code reference of classes and functions

## [0.4.0](https://gitlab.com/ud-labs/py-calendar-api/-/releases/0.4.0) - 2026-05-14

### Refactoring

- Drop `niquests` in favor of `httpxyz`

### Bug Fixes

- `DateSeries`: `min_date` and `max_date` weren't deserialized as datetime.date (Thanks to tests)

### Tests

- Add a small test suite (Boundaries Testing) based on pytest
  - Checks deserialisation and data structs
  - Asserts lightweight logic for calendar operations

TODO:
  - Test Base Mixin
  - Test query params (filter params)

### Documentation

- Rewrite the documentation index page
- Add `how-it-works` section

## [0.3.0](https://gitlab.com/ud-labs/py-calendar-api/-/releases/0.3.0) - 2026-03-07

### Refactoring

- Drop `httpx` in favor of `niquests`

## [0.2.1](https://gitlab.com/ud-labs/py-calendar-api/-/releases/0.2.1) - 2026-03-06

### Project chores

- Add pypi publishing
- Adapt License
- Proof reading the ReadME
- Remove unused dependencies
- Add pages publishing step
- Add badges to the project page + description

## [0.1.0](https://gitlab.com/ud-labs/py-calendar-api/-/releases/0.1.0) - 2026-03-05

### Features

- Python Client for calendar-api.ma
- Centralised entry point via CalendarApi
- dataclasses Responses
