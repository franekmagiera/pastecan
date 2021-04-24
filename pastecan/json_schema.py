post_pastes_schema = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        'language',
        'content',
        'title',
        'exposure'
    ],
    'properties': {
        'language': {'type': 'string'},
        'content': {'type': 'string'},
        'title': {'type': 'string'},
        'exposure': {'type': 'string'}
    }
}
