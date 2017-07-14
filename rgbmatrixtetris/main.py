from __future__ import print_function
from lib.game import Game
import atexit
import config


def main():
    game = Game(
        config.game['switches'],
        config.game['columns'],
        config.game['rows'],
        config.game['shapes_next_count'],
        config.game['fps'],
        config.game['countdown'],
        config.game['interval'],
        config.game['score_increments'],
        config.game['level_increment'],
        config.game['interval_increment'],
        config.game['rgb_matrix_hardware'],
        config.game['rgb_matrix_rows'],
        config.game['rgb_matrix_chain_length'],
        config.game['rgb_matrix_parallel'],
        config.game['rgb_matrix_pwm_bits'],
        config.game['rgb_matrix_brightness'],
        config.game['rgb_matrix_lsb_nanoseconds'],
        config.game['rgb_matrix_gpio_slowdown'],
        config.game['rgb_matrix_disable_hardware_pulsing'],
        config.game['rgb_matrix_rgb_sequence'],
    )

    atexit.register(game.__exit__)

    game.start()

if __name__ == '__main__':
    main()
