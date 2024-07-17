def convert_to_abbreviation(text):
    unit_dict = {
        'milligram': 'mg',
        'gram': 'g',
        'kilogram': 'kg',
        'liter': 'L',
        'meter': 'm',
        'centimeter': 'cm',
        'millimeter': 'mm',
        'mile': 'mi',
        'yard': 'yd',
        'foot': 'ft',
        'inch': 'in',
        'second': 's',
        'minute': 'min',
        'hour': 'h',
        'day': 'd',
        'week': 'wk',
        'period': '.',
        'year old': 'year-old'
    }
    
    # Process text
    for unit, abbreviation in unit_dict.items():
        text = text.replace(unit, abbreviation)
    
    # Handle new paragraphs
    paragraphs = text.split('\n')
    formatted_text = '\n'.join(paragraph.strip() for paragraph in paragraphs)
    
    return formatted_text