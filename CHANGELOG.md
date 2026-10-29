# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [1.0.0](https://gitlab.com/ud-labs/py-calendar-api/-/releases/1.0.0) - 2026-10-28

### Features

- Tagged Calendar: `api.tagged.year(year)` and `api.tagged.month(year, month)` (`/tagged-calendar`), sync and async. Every day is tagged `BUSINESS`, `WEEKEND` or `HOLIDAY`, months are laid out in ISO weeks
- New models `TaggedYear`, `TaggedMonth`, `TaggedDay`, `TaggedDaysCount` and the `DayKind` enum

### Documentation

- Document the Tagged Calendar in the README and in How it Works

## [0.9.0](https://gitlab.com/ud-labs/py-calendar-api/-/releases/0.9.0) - 2026-10-26

### Features

- HTTP options can be passed to `CalendarApi` / `AsyncCalendarApi` (and `from_env()` / `from_config_file()`) as keyword arguments: `CalendarApi(key, proxy=..., timeout=..., verify=...)`. Unknown options raise `TypeError`
- New `[http_client]` options: `proxy`, `trust_env`, `read_timeout`, `cert`, `cert_key`. `verify` accepts a CA bundle path
- `client_kwargs`: extra `httpx.Client` / `httpx.AsyncClient` arguments (`limits`, `auth`, `event_hooks`...)
- Export `HTTPClientConfig` and `HTTPClientOptions`

### Bug Fixes

- The `HTTPS_PROXY` / `HTTP_PROXY` / `NO_PROXY` environment variables were ignored, because the client always set its own transport
- The `retries` default of `get_http_client` / `get_http_client_async` (2) differed from the configuration (3)

### Documentation

- Document the configuration (proxy, timeouts, certificates) in the README

## [0.8.0](https://gitlab.com/ud-labs/py-calendar-api/-/releases/0.8.0) - 2026-10-26

### Features

- Add `AsyncCalendarApi`: async client mirroring `CalendarApi` (`bdays`, `holidays`, `health`), usable with `async with`
- `CalendarApi` can be used as a context manager (`with`) and exposes `close()`
- `CalendarApi(..., transport=...)`: optional custom `httpx` transport (proxies, tests)
- 401/403 responses raise `CalendarAPIAuthError` (subclass of `CalendarAPIClientError`)

### Bug Fixes

- Async HTTP client: TLS verification was disabled by default (`verify=False`)
- Async HTTP client: the request event hook was a sync function, which `httpx.AsyncClient` rejects
- `openapi_schema()` raised `AttributeError`, it now downloads `/schema/openapi.json`
- The health endpoint ignored a custom `host` from the configuration
- Passing `apikey` with a `config` mutated that config (and the cached `load_settings()` result)
- Non-Json error responses (ie: gateway errors) raised a `JSONDecodeError` instead of `CalendarAPIClientError`
- `holidays.years("2026")` split the string into characters
- Responses compressed with brotli or zstd could not be decoded when the optional decoders were not installed: depend on `httpx[brotli,zstd]`

### Refactoring

- Drop `httpxyz` in favor of `httpx`
- Requests are described once (`ApiCall`) and executed by the sync or the async resources
- Remove the unneeded `wheel` build requirement, declare the setuptools build backend

### Tests

- Offline test suite on `httpx.MockTransport`, run against both the sync and async clients
- Test the Base Mixin (endpoints, deserialization, error handling)
- Live tests are marked `live` and skipped when `PYCALENDAR_APIKEY` is not defined
- Fix `testpaths` in `pytest.ini`

### CI

- GitHub release: exact changelog matching, fails when the version has no entry, attaches the built distributions
- GitLab: run the tests on merge requests and the default branch, publish only when tests pass, install the `docs` extra for the pages job

## [0.7.0](https://gitlab.com/ud-labs/py-calendar-api/-/releases/0.7.0) - 2026-08-19

### CI

- Add a `test` stage running the test suite on tags
- Build docs pages on the default branch
- Use `rules` and `needs` instead of `only` and `dependencies`

## [0.6.0](https://gitlab.com/ud-labs/py-calendar-api/-/releases/0.6.0) - 2026-08-19

### Bug Fixes

- Complete the `niquests` -> `httpxyz` migration started in 0.4.0: `config/settings.py` and the domains (`bdays`, `health`, `holidays`) still imported `niquests` for their type hints, although it was no longer a dependency. The package could not be imported without `niquests` installed (0.4.0 to 0.5.3)

### Documentation

- Make the ReadMe and the documentation index more SEO friendly

## [0.5.3](https://gitlab.com/ud-labs/py-calendar-api/-/releases/0.5.3) - 2026-08-19

### Documentation

- Fix the registration URL
- Add the PyPI badge

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

- Drop `niquests` in favor of `httpxyz` for the HTTP engine (`utils/http_client.py`) and the dependencies

### Known Issues

- `config/settings.py` and the domains still import `niquests` for their type hints: the package cannot be imported unless `niquests` is installed. Fixed in 0.6.0

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
