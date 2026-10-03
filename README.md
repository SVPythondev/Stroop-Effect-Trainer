# Stroop Effect Trainer

A small game that tests how well your brain handles conflicting information.
A color word is shown in an ink color that may not match the word (for example, the word RED written in blue). Your job is to answer quickly and correctly.

**Play online:** https://svpythondev.github.io/Stroop-Effect-Trainer/

## What is the Stroop effect?

Reading is automatic for the brain, while naming a color takes more effort. When the word and its ink color disagree, the two processes collide, and you answer slower or make mistakes. This game turns that effect into a short attention test.

## Features

- **Two modes:** pick the color of the text, or pick the color the word names.
- **Adjustable round:** 60 seconds by default, from 30 to 300 seconds in steps of 10.
- **Live score:** hidden by default so it does not distract; show it with one button.
- **Results screen:** correct and wrong answers, accuracy, average reaction time, and a Brain performance score from 0 to 100 with a short rating.

## How the Brain performance score works

```
score = 60% accuracy + 40% reaction speed
```

Reaction speed maps 0.5 s per answer to 100 points and 2.5 s or slower to 0 points. This is a simple fun indicator, not a medical or scientific measurement.

## Two versions

| Version | File | How to run |
|---|---|---|
| Web | `index.html` | Open the online link above, or open the file in any browser |
| Desktop | `desktop/main.py` | Needs Python 3 (see below) |

### Run the web version locally

Download `index.html` and double-click it. No installation or internet connection is needed.

### Run the desktop version

1. Install [Python 3](https://www.python.org/downloads/). The `tkinter` library is included with the standard installation (on some Linux systems install it with `sudo apt install python3-tk`).
2. Download the repository: `git clone https://github.com/YOUR-USERNAME/stroop-effect-trainer.git`
3. Run the game:
   ```
   cd stroop-effect-trainer/desktop
   python main.py
   ```
   On macOS and Linux you may need `python3 main.py`.

## Project structure

```
stroop-effect-trainer/
├── index.html      # Web version (one file, no dependencies)
├── desktop/
│   └── main.py     # Python and tkinter version
└── README.md       # This file
```

## For beginners

Every line of code in both versions has a plain-language comment, so you can read the files without knowing Python or JavaScript.

## License

AThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
