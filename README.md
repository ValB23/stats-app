# Stats app
An application in Python with QT to show some basic stats

## Prerequisite
- PyQT must be installed

## Installing in Linux/WSL

```shell
git clone
cd stats-app
python main_app.py
```

## How to use

`File -> Open`

Select any .dat file where only numbers are in.

After opening the file, the histogram (bar graph), will be displayed in red.

You can also drag & drop the .dat file into the app window.

## Actions

- Switching between a bar graph (histogram) and a pie chart (pie)
- Changing color `Display -> Color`
- Saving the bar graph into a file `File -> Save`
- Restoring the bar graph into the app in `File -> Restore`

### Issues to fix

- Restoring an empty histogram crashes the app