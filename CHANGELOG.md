# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2023-06-08

### Added
- Blacklisting games to avoid auto entering their giveaways

### Changed
- Moved all the logic to a python class
- Moved the run logic to a separate python file main.py
- Moved the python run logic to a docker_entrypoint.sh bash script

### Fixed
- Exception with giveaways without cover image
- Exception trying to join your own giveaways

## [0.1.0] - 2023-06-02

This is the initial version! It automatizes the giveway entering process for wishlisted, DLCs and recommended giveaways and supports steam login with mobile 2fa.

### Added
- Automatic login. Only login with mobile MFA is currently supported
- Automatic giveaway enter for wishlist, DLCs and recommended giveaways in that order