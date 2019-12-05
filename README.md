# Application Package-management Proxy (APP)
__APP__ is an extensible simple cli proxy wrapper for existing package-manager tools. It facilities interaction with multiple separate package-managers through a single cli interface.

## Why do I need this?
This project was started to scratch my own itch. If you bounce between different Linux distros or get frustrated with the separate package manger interfaces, then it may be for you as well.

## What Package-managers will this work with?
In theory... any! New package manager interfaces are added by sub-classing the _ManagerBase_ class in the mangers package of this project. 
### Current supported managers:
- APT
- Yay/Pacman (Yay is preferred)
- Snap
- SPM (AppImage)
### Planned new managers:
- FlatPack (In work)
- DNF

## CLI Style, Operations and Options
The `app` __CLI__ is shamelessly based on pacman and committed to implementing the Python design philosophy with regard to package management.

> there should be one—and preferably only one—obvious way to do it

__Usage:__ 
```bash
$ app [operation] [options] [package name(s)]
```

Operations | Type | Description
--- | --- | ---
`-S`,`--sync` | _flag_ | (re)Installs list of packages
`-R`, `--remove` |  _flag_ | Removes list of packages

Options | Type | Description
--- | --- | ---
`-i`, `--info` |  _flag_ | Provides info on list of packages
`-s`,`--search` | _flag_ | Searches for supplied package
`-y`,`--refresh` | _flag_ | Refresh the package databases
`-u`,`--upgrade` | _flag_ | Upgrade all applicable packages
`--noconfirm` | _flag_ | Accepts all questions
`--needed` | _flag_ | Syncs only needed packages

At this point, the __CLI__ is only partially implemented. The design goal is to completely mirror the pacman cli, but this pacman cli is extensive. Additional features will be added as needed.

## TODO
- Finish flatpak manager
- Add more native system package-manager wrappers
- Expand __CLI__ to include more options
