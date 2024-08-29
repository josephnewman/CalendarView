def dictionary_lookup(dictionary, key):
    return dictionary.get(key, None)


def remove_bracketed_words(txt, open_bracket='<', close_bracket = '>'):
    processed_text = ''
    is_adding = True
    for char in txt:
        if char == open_bracket:
            is_adding = False
        if is_adding:
            processed_text += char
        if char == close_bracket:
            is_adding = True
    return processed_text


def add_weekday(current_weekday):
    return (current_weekday + 1) % 7


def is_num(input_string): # used only in the version on Glitch, where isnumeric is not processed properly
  try:
    int(input_string)
    return True
  except:
    return False