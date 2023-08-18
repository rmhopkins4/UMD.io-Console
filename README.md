# UMD.io Console

UMD.io Console is a command-line program meant to help University of Maryland students (primarily myself) with finding information on courses, majors, and the university itself.

The program also features a schedule manager, where users can build schedules for the upcoming semester without relying on outdated, finnicky programs like venus!

## Disclaimers

- [ ] Built off of [UMD.io API](https://github.com/umdio/umdio) and [PlanetTerp API](https://github.com/planetterp/PlanetTerp-API).
- [ ] Requires internet connection to access and scrape information!

## Required Libraries from `pip`

- `requests`
- `matplotlib` & `mplcursors`
- `datetime`

## How to Use

To begin the program, simply run `umd.io`! Works best in the console, but any python editor should work.

#### Commands

Info regarding these commands is also accessible by running `commands`

| Command      | Result                                                             |
| ------------ | ------------------------------------------------------------------ |
| `commands`   | List all available commands                                        |
| `sections`   | List all sections for a class in most recent or specified semester |
| `courseinfo` | Display most recent information for a course and all-time GPA      |
| `major`      | Display limited information on specific majors                     |
| `map`        | Plot all university buildings on a pyplot                          |
| `schedule`   | Manage/view class schedule                                         |
| `end`        | End program                                                        |
