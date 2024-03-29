class Constants:
    FPS = 60

    # DEFAULT_SCREEN = False
    # FULL_SCREEN = False
    # FULL_WINDOW_SCREEN = True

    DEFAULT_SCREEN = True
    FULL_SCREEN = False
    FULL_WINDOW_SCREEN = False

    DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT = 1280, 720
    WINDOW_WIDTH, WINDOW_HEIGHT = None, None
    if DEFAULT_SCREEN:
        WINDOW_WIDTH, WINDOW_HEIGHT = DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT

    ALLCARD = ['1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
               '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
               '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
               '1z', '2z', '3z', '4z', '5z', '6z', '7z']

    ALLCARDS = ['1m', '1m', '1m', '1m',
                '2m', '2m', '2m', '2m',
                '3m', '3m', '3m', '3m',
                '4m', '4m', '4m', '4m',
                '5m', '5m', '5m', '5m',
                '6m', '6m', '6m', '6m',
                '7m', '7m', '7m', '7m',
                '8m', '8m', '8m', '8m',
                '9m', '9m', '9m', '9m',

                '1p', '1p', '1p', '1p',
                '2p', '2p', '2p', '2p',
                '3p', '3p', '3p', '3p',
                '4p', '4p', '4p', '4p',
                '5p', '5p', '5p', '5p',
                '6p', '6p', '6p', '6p',
                '7p', '7p', '7p', '7p',
                '8p', '8p', '8p', '8p',
                '9p', '9p', '9p', '9p',

                '1s', '1s', '1s', '1s',
                '2s', '2s', '2s', '2s',
                '3s', '3s', '3s', '3s',
                '4s', '4s', '4s', '4s',
                '5s', '5s', '5s', '5s',
                '6s', '6s', '6s', '6s',
                '7s', '7s', '7s', '7s',
                '8s', '8s', '8s', '8s',
                '9s', '9s', '9s', '9s',

                '1z', '1z', '1z', '1z',
                '2z', '2z', '2z', '2z',
                '3z', '3z', '3z', '3z',
                '4z', '4z', '4z', '4z',

                '5z', '5z', '5z', '5z',
                '6z', '6z', '6z', '6z',
                '7z', '7z', '7z', '7z',
                ]

    ORPHANS = ['1m', '9m', '1p', '9p', '1s', '9s',
               '1z', '2z', '3z', '4z', '5z', '6z', '7z']

    CARD_POSITION = {'1m': (0, 1385), '2m': (192, 1385), '3m': (384, 1385), '4m': (576, 1385), '5m': (768, 1385), '6m': (0, 1640), '7m': (192, 1640), '8m': (384, 1640), '9m': (576, 1640),
                     '1p': (0, 0), '2p': (195, 0), '3p': (390, 0), '4p': (585, 0), '5p': (780, 0), '6p': (0, 255), '7p': (195, 255), '8p': (390, 255), '9p': (585, 255),
                     '1s': (585, 822.0999999999999), '2s': (390, 544), '3s': (789.75, 544), '4s': (585, 544), '5s': (0, 814), '6s': (195, 814), '7s': (390, 816.6999999999999), '8s': (195, 544), '9s': (0, 544),
                     '1z': (410, 1120), '2z': (615, 1120), '3z': (830.25, 1120), '4z': (1049.6, 1120), '5z': (1289.45, 1120), '6z': (205, 1120), '7z': (0, 1120)}

    CARD_LEVEL = {'white': (255, 255, 255), 'green': (0, 255, 0), 'blue': (0, 0, 255),
                  'purple': (128, 0, 128), 'yellow': (255, 255, 0), 'red': (255, 0, 0),
                  'black': (1, 1, 1)}

    MAX_HANDS = 13

    REGULAR_BASE_SCORE = 500
    SEVEN_PAIRS_BASE_SCORE = 400
    THIRTEEN_ORPHANS_BASE_SCORE = 32000
    FAIL_BASE_SCORE = -8000

    def FUNC_DO_NOTHING(): pass
