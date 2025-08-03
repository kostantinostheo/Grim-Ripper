# 𓌳 Grim Ripper

![Grim Rippper Logo](./icon/GrimRipperIcon_ssm.png) 

## 📖 Background

While digging through some old boxes, I found a collection of DVDs from when I was young. I wanted to digitize them to preserve those memories, but ripping each DVD one by one was tedious and time-consuming. 

To save time, I decided to create **Grim Ripper** — a **Python** wrapper around [HandBrakeCLI](https://handbrake.fr/docs/en/latest/cli/cli-options.html) that can batch and parallel rip multiple DVDs at once. It supports GPU or CPU encoding, resolution presets, and full customizability via external argument files.

---

## 🚀 Features

- 🔁 Batch rip multiple DVDs from a directory
- 🖥️ Use GPU (`nvenc_h264`) or CPU (`x264`) encoding
- 📏 Choose output resolution: `720p`, `1080p`, or `2160p`
- ⚙️ Select encoding speed: `slow`, `mid`, or `fast`
- 📄 Provide a custom argument file to override all defaults
- 📂 Outputs organized by DVD label

---

## 📦 Requirements

- Python 3.8+
- [HandBrakeCLI](https://handbrake.fr/downloads2.php) installed and available in your `PATH`
- [libdvdcss](https://www.videolan.org/developers/libdvdcss.html) installed and available in your `PATH`

## Installing HandBrakeCLI and libdvdcss

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install handbrake-cli libdvd-pkg
sudo dpkg-reconfigure libdvd-pkg
```
### Fedora
```bash
sudo dnf install HandBrake-cli
# For libdvdcss (from RPM Fusion repository):
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install libdvdcss
```
### macOS (using Homebrew)
```bash
brew install handbrake libdvdcss
```


## 🔧 Grim Ripper Installation

Clone this repo:

```bash
git clone https://github.com/yourusername/rippper.git
cd rippper
```
---

## ⚙️ Usage
### Option 1: Use built-in presets

```bash
python3 grimripper.parallel.py -i /media/{user}/ -o ./output_directory -r 1080p -s mid -g
```

### Option 2: Use a custom HandBrakeCLI argument file
- Create a file custom_args.txt with your HandBrakeCLI argument:

```txt
--main-feature --preset "Fast 720p30" -f mp4 -e x264 -q 22 --subtitle none
```
- Run with the custom file:

```bash
python3 grimripper.parallel.py -i /media/youruser/ -o ./rips --custom-args-file custom_args.txt
```

---

## 🔍 Command-Line Options

| Flag                 | Description                                                        |
|----------------------|--------------------------------------------------------------------|
| `-i`, `--input`      | Directory containing mounted DVDs (e.g. `/media/user`)            |
| `-o`, `--output`     | Output directory for ripped `.mp4` files                           |
| `-r`, `--resolution` | Target resolution: `720p`, `1080p`, or `2160p`                    |
| `-s`, `--speed`      | Encoding speed preset: `slow`, `mid`, or `fast`                   |
| `-g`, `--gpu`        | Enable GPU encoding (`nvenc_h264`); otherwise uses CPU (`x264`)   |
| `--custom-args-file` | Path to a file with full custom HandBrakeCLI arguments            |

---

## 📂 Output Structure

```
./rips/ 
├── MOVIE_ONE/
│   └── MOVIE_ONE.mp4
├── MOVIE_TWO/
│   └── MOVIE_TWO.mp4
```
