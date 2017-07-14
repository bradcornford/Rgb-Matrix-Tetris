game = {
    'switches': {
        # GPIO17 - Pin 11
        17: 'ESCAPE',
        # GPIO06 - Pin 31
        6: 'LEFT',
        # GPIO13 - Pin 33
        13: 'RIGHT',
        # GPIO19 - Pin 35
        19: 'DOWN',
        # GPIO23 - Pin 16
        23: 'UP',
        # GPIO24 - Pin 18
        24: 'p',
        # GPIO27 - Pin 13
        27: 'RETURN'
    },
    'columns': 10,
    'rows': 37,
    'shapes_next_count': 8,
    'fps': 60,
    'countdown': 5,
    'interval': 800,
    'score_increments': [
        0,
        10,
        20,
        40,
        80,
        160,
        320,
        640,
        1280,
        2560,
        5120,
        10240,
        20480,
        40960,
        81920,
        163840
    ],
    'level_increment': 2,
    'interval_increment': 50,
    'rgb_matrix_hardware': 'adafruit-hat',
    'rgb_matrix_rows': 32,
    'rgb_matrix_chain_length': 2,
    'rgb_matrix_parallel': 1,
    'rgb_matrix_pwm_bits': 11,
    'rgb_matrix_brightness': 25,
    'rgb_matrix_lsb_nanoseconds': 130,
    'rgb_matrix_gpio_slowdown': 1,
    'rgb_matrix_disable_hardware_pulsing': False,
    'rgb_matrix_rgb_sequence': 'RGB'
}
