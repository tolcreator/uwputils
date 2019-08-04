PALETTE = [
    '#793f0d',
    '#004159',
    '#6e7649',
    '#8c65d3',
    '#846d74',
    '#0052A5',
    '#846d74',
    '#00c590',
    '#AC703D',
    '#65A8C4',
    '#9d9754',
    '#9a93ec',
    '#b7a6ad',
    '#00adce',
    '#c38e63',
    '#aacee2',
    '#c7c397',
    '#81cbf8',
    '#d3c9ce',
    '#b5f9d3'
]


def constructPalette(systems):
    stateColours = {
        'Na': '#c0c0c0',
        '  ': '#c0c0c0'
    }
    for system in systems:
        if system['type'] == 'system':
            if system['allegiance'] not in stateColours:
                stateColours[system['allegiance']] = PALETTE[len(stateColours) % len(PALETTE) ]
    return stateColours