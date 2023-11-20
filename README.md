<div align="center">

# Two-dimensional Display Interface <br> for Brain-Computer Interface Control

### Framework to control a two-dimensional display using a Brain-computer Interface

[Quick Start](#%EF%B8%8F-quick-start) •
[Edit Me!](#-edit-me)  •
[AEG](#-the-applied-electromagnetics-group)

</div>

## ⚡️ Quick start 

First, install all python dependencies using the `requirements.txt` file. This can be done by one of the following methods:

```bash
# using conda, without creating new env
conda install --file requirements.txt

# using conda, creating new env
conda create --name <env> --file requirements.txt

# using pip
pip install -r requirements.txt
```
> ⚠️ **If you're executing the second command:** Substitute ```<env>``` by the name of the env you want to create!

Next, edit the ```src/main.py``` selecting the desired display interface and the image to be shown:

```python
# ...
display_type = 'external'
image_path = 'assets/ghost.png'
#...
```

Then, install the package using pip in editable mode and execute the ```main.py``` file:

```bash
# move to the src folder
pip install -e .

# execute the main file
python src/main.py
```

That's all! The framework will execute using the default configuration.

## 📝 Edit Me!

When using the external display interface, it's possible to change the LED Matrix settings to be used in the ```settings/led_matrix.toml``` file. The default specs are:

```toml
[specs]
gpio_pin = 18           # GPIO pin connect to the matrix signal line (must support PWM)
led_count = 512         # Number of LEDs in the matrix
led_freq_hz = 800000    # LED signal frequency in hertz (usually 800khz)
led_dma = 10            # DMA channel to use for generating signal (defaults to 10)
led_invert = false      # True to invert the signal (when using NPN transistor level shift)
led_brightness = 1      # Set to 0 for darkest and 1 for brightest
width_count = 32        # Number of LEDs in the width of the matrix
height_count = 16       # Number of LEDs in the height of the matrix
```


##

### You can, as well, execute this script with diferrent datasets and use the results in your analysis.


To do so, just **edit the value of the variables** in the ```src/user_inputs.py``` file acording to the desired values. A description of what each variable means can be found in the begining of the file. 

```
├── ...
├── res/
├── src/
│   ├── app_multiprocessing.py
│   ├── app.py
│   ├── ...
│   └── user_inputs.py  <–––
├── README.md
└── requirements.txt
```


## 💡 The Applied Electromagnetics Group

**This project is part of [The Applied Electromagnetics Group](http://www.sel.eesc.usp.br/leonardo/)**. 