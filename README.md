# Raspberry Pi Python rgb matrix tetris

A project to create a tetris game on a Raspberry Pi using RGB Matrix / USB JoyStick.

## Requirements

This package requires the following system packages to be installed:

- python-dev
- build-essential
- python-pip

These can be installed using the following:

    sudo apt-get update
    sudo apt-get install -y python-dev build-essential python-pip

## Installation

Begin by installing this packages requirements:

    sudo -H pip install -e .
    
Finally copy the example configuration file `example.config.py`, and save it as `config.py`

    cp rgbmatrixtetris/example.config.py rgbmatrixtetris/config.py

## Configuration

You can now configure Rgb-Matrix-Tetris in a few simple steps. Open `rgbmatrixtetris/config.py` and update the options as needed.

- `switches` - An array of Switches using GPIO pin as the key.
- `columns` - The number of columns the board has.
- `rows` - The number of rows the board has.
- `shapes_next_count` - The number of shapes to generate in advance.
- `fps` - The games frames per second.
- `countdown` - The game countdown in seconds.
- `interval` - The game tick interval in milliseconds.
- `score_increments` - An array of numbers to increment score by in game.
- `level_increment` - The score when to increment the level by in game.
- `interval_increment` - The number to reduce the game tick interval by in milliseconds.
- `rgb_matrix_hardware` - The rgb matrix hardware.
- `rgb_matrix_rows` - The number of rows the rgb matrix panel has.
- `rgb_matrix_chain_length` - Number of daisy-chained panels.
- `rgb_matrix_parallel` - Number of panels that are parallel chains.
- `rgb_matrix_pwm_bits` - Bits used for PWM.
- `rgb_matrix_brightness` - Sets brightness level.
- `rgb_matrix_lsb_nanoseconds` - Base time-unit for the on-time in the lowest significant bit in nanoseconds.
- `rgb_matrix_gpio_slowdown` - Slow down writing to GPIO.
    
## Usage

It's really as simple as using the main file

    sudo python rgbmatrixtetris/main.py
    
### License

Rgb-Matrix-Tetris is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT)
