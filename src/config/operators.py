comparable_operator = {
    '==': '',
    '=~': ''
}

text_operator = {
    'contains': '|contains',
    'startswith': '|startswith',
    'endswith': '|endswith',
    'matches_regex': '|re:'
}
array_operator = {
    'in': '',
    'in~': '',
    'has_all': '|contains|all'
}
operators = {**comparable_operator, **text_operator, **array_operator}