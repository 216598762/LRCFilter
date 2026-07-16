# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-16

### Added

#### Core Features
- **Audio Scanner** (`scanner.py`): Recursive folder scanning with support for flac, mp3, m4a, ogg, opus formats; symlink loop detection and stat error handling
- **Metadata Extraction** (`metadata.py`): Audio file metadata extraction using Mutagen with full tag parsing for title, artist, album, and duration
- **Lyrics Fetching** (`lyrics.py`): LRCLib API integration with Genius API fallback for retrieving song lyrics; configurable API delay and match scoring
- **Audio Analysis** (`analyzer.py`): FasterWhisper integration for speech-to-text transcription with word-level timestamps; model caching with thread-safe double-checked locking
- **Censorship Detection** (`censorship.py`): Profanity detection using better-profanity with fallback word list; lyrics/transcription mismatch scoring
- **Instrumental Detection** (`instrumental.py`): Vocal content analysis based on word count thresholds and speech detection
- **Metadata Mismatch Detection** (`mismatch.py`): Title and artist similarity comparison using RapidFuzz; confidence scoring for mismatch detection
- **Pipeline Orchestration** (`pipeline.py`): Full pipeline chaining all modules together; parallel processing with progress callbacks
- **Output Writer** (`output.py`): Categorized text file output for censored, instrumental, and mismatched tracks with timestamp support

#### Configuration & CLI
- **Pipeline Config** (`config.py`): Centralized configuration with validation for beam_size, thresholds, API delays, and output options
- **CLI Interface** (`__main__.py`): Command-line interface with argparse; support for all pipeline options and configuration parameters
- **Parameter Validation**: Comprehensive validation for all numeric parameters across all modules

#### Infrastructure
- **pyproject.toml**: Modern Python packaging with all dependencies and dev tools configured
- **Docker Support**: Dockerfile and docker-compose.yml for containerized deployment
- **GitHub Actions CI/CD**: Automated testing, linting, and coverage reporting on push/PR
- **Dependabot**: Automated dependency security updates configuration
- **Pre-commit Hooks**: Automated linting and formatting before commits

#### Testing
- **331 Tests**: Comprehensive test suite achieving 99% code coverage
- **Unit Tests**: Individual module tests for all core functionality
- **Integration Tests**: Full pipeline tests with mocked dependencies
- **Parameter Validation Tests**: Cross-module validation testing

#### Documentation
- **README.md**: Usage instructions, CLI options, programmatic API, Docker usage, troubleshooting
- **ARCHITECTURE.md**: Detailed project architecture and module documentation
- **CONTRIBUTING.md**: Contributor guidelines and development setup
- **CODE_OF_CONDUCT.md**: Contributor Covenant guidelines
- **SECURITY.md**: Vulnerability reporting guidelines
- **LICENSE**: MIT License

### Changed
- Migrated from setup.py to pyproject.toml for modern Python packaging
- Consolidated three separate write_results calls into single call for efficiency
- Refactored `_normalize_text` into shared `utils.py` module to eliminate duplication
- Removed dead `_calculate_duration_difference` function from mismatch.py
- Cleaned up unused `DURATION_TOLERANCE` import from mismatch.py

### Fixed
- Fixed fragile profanity counting in censorship.py
- Fixed unused `lyrics_duration` parameter in mismatch.py
- Fixed scanner symlink loop detection for proper recursion prevention
- Fixed metadata extraction for files without duration information

### Security
- GPG-signed commits for all changes
- Automated dependency updates via Dependabot

## [0.0.1] - 2026-07-15

### Added
- Initial project structure
- Core module implementations
- Basic pipeline orchestration
- Logging configuration
- CLI argument parsing

---

## Release Notes

### v0.1.0 Highlights

This is the first stable release of LRCFilter, a Python tool for analyzing audio files to detect:

- **Censored/Explicit Content**: Profanity detection and lyrics mismatch analysis
- **Instrumental Tracks**: Vocal content analysis using speech-to-text
- **Metadata Mismatches**: File metadata vs. lyrics API comparison

The tool supports flac, mp3, m4a, ogg, and opus formats with recursive folder scanning and outputs results to categorized text files.

**Quick Start:**
```bash
# Install
pip install -e .

# Run
lrcfilter /path/to/music/folder

# With options
lrcfilter /path/to/music --beam-size 10 --censorship-threshold 0.5 --output ./results
```

**Test Coverage:** 331 tests with 99% code coverage across all modules.
