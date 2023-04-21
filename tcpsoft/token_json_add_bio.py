def token_json_add_bio(original_tags):
    def _change_prefix(original_tag, new_prefix):
        assert original_tag.find("-") < 0 and len(new_prefix) == 1
        return new_prefix+"-"+original_tag

    def _pop_replace_append(stack, bio_sequence, new_prefix):
        tag = stack.pop()
        new_tag = _change_prefix(tag, new_prefix)
        bio_sequence.append(new_tag)

    def _process_stack(stack, bio_sequence):
        if len(stack) == 1:
            _pop_replace_append(stack, bio_sequence, "B")
            # _pop_replace_append(stack, bioes_sequence, "U")
        else:
            recoded_stack = []
            _pop_replace_append(stack, recoded_stack, "I")
            # _pop_replace_append(stack, recoded_stack, "L")
            while len(stack) >= 2:
                _pop_replace_append(stack, recoded_stack, "I")
            _pop_replace_append(stack, recoded_stack, "B")
            recoded_stack.reverse()
            bio_sequence.extend(recoded_stack)

    bio_sequence = []
    stack = []
    last_tag = "O"

    for tag in original_tags:
        if tag == "O":  # B/I/O O
            if len(stack) == 0:
                bio_sequence.append(tag)
            else:
                _process_stack(stack, bio_sequence)
                bio_sequence.append(tag)
        elif last_tag == "O":  # O B/I
            stack.append(tag)
        elif last_tag == tag:  # B I
            stack.append(tag)
        elif last_tag != tag:  # I B/O
            _process_stack(stack, bio_sequence)
            stack.append(tag)
        else:
            raise ValueError("Invalid tag:", tag)
        last_tag = tag

    if len(stack) > 0:
        _process_stack(stack, bio_sequence)

    return bio_sequence