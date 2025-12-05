# CHANGELOG

<!-- version list -->

## v0.2.2 (2025-12-05)

### Bug Fixes

- Trigger patch release
  ([`b09f0af`](https://github.com/apathetic-tools/python-utils/commit/b09f0af829258bf88d41e63daa14c318771a3445))

### Chores

- **deps**: Bump actions/checkout from 5 to 6
  ([#1](https://github.com/apathetic-tools/python-utils/pull/1),
  [`56119b2`](https://github.com/apathetic-tools/python-utils/commit/56119b2769c68ea97feac5eab1e60957e9ef4b27))

### Continuous Integration

- Rename GitHub Actions workflow files
  ([`55dc4db`](https://github.com/apathetic-tools/python-utils/commit/55dc4dbb314c24282b7eed46a032fb2586a7ddc5))

### Documentation

- **api**: Add missing functions to API documentation
  ([`665f6b4`](https://github.com/apathetic-tools/python-utils/commit/665f6b4e64d1ece936c97cc2eb84b2cd3ac5f4ce))

### Refactoring

- Update code formatting and test structure
  ([`8062cdf`](https://github.com/apathetic-tools/python-utils/commit/8062cdf108ea4349f7046b0f5d0ed1f55c4d77d6))

- **project**: Major cleanup and module reorganization
  ([`21ce5c0`](https://github.com/apathetic-tools/python-utils/commit/21ce5c037043f8133c20d848eb0b510776737fc7))

### Testing

- **30_independant**: Add tests migrated from serger
  ([`da9f245`](https://github.com/apathetic-tools/python-utils/commit/da9f24528b6f611ef3e8af9731315b79eb6ebbe9))

- **pytest**: Add parallel execution support and fix zipapp tests
  ([`a4e5314`](https://github.com/apathetic-tools/python-utils/commit/a4e5314a63358c2e294f9823cfe9e9a577dd8c9a))


## v0.2.1 (2025-11-28)

### Bug Fixes

- **tests**: Fix logging registration in stitched builds
  ([`4048bfc`](https://github.com/apathetic-tools/python-utils/commit/4048bfcf1e64d22bd61e507339465caa8f1d298e))

### Refactoring

- **tests**: Simplify test utilities and remove unused modules
  ([`b7dc2a9`](https://github.com/apathetic-tools/python-utils/commit/b7dc2a996210fac1dbfeb9fd8e0acbe70c613b2c))


## v0.2.0 (2025-11-28)

### Bug Fixes

- **runtime**: Correct zipapp detection and update tests after system->runtime rename
  ([`2710597`](https://github.com/apathetic-tools/python-utils/commit/271059794bdef6bdb4417bc1e6fb08e82ec2a2e0))

- **subprocess**: Fix run_with_separated_output and remove test skips
  ([`ba84ea9`](https://github.com/apathetic-tools/python-utils/commit/ba84ea9d19adb8f055128f8eba8f023be0c0589f))

### Documentation

- Update documentation to reflect apathetic-utils instead of apathetic-logging
  ([`a415318`](https://github.com/apathetic-tools/python-utils/commit/a415318c22323867d977d0e15dd9c0697f1f5554))

### Features

- **__init__**: Expose all public mixin functions
  ([`26f29f0`](https://github.com/apathetic-tools/python-utils/commit/26f29f0dad3f18abb8656d1e6ad61af36ac612bb))


## v0.1.1 (2025-11-27)

### Bug Fixes

- **ci**: Add workflow_run trigger and tag verification to publish workflow
  ([`f39fa37`](https://github.com/apathetic-tools/python-utils/commit/f39fa37be146f2e10fd81f34f2778af47fc7f849))


## v0.1.0 (2025-11-27)

### Features

- **system**: Add package_name parameter to detect_runtime_mode
  ([`b3c10a8`](https://github.com/apathetic-tools/python-utils/commit/b3c10a8b8ff698638137ef6c721d6e64f6ab7389))


## v0.0.1 (2025-11-27)

- Initial Release
