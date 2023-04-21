# BIOES2BIO
def bioes_to_bio(original_tags):
    def _change_prefix(original_tag, new_prefix):
        assert original_tag.find("-") > 0 and len(new_prefix) == 1
        chars = list(original_tag)
        chars[0] = new_prefix
        return "".join(chars)

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

    for tag in original_tags:
        if tag == "O":
            if len(stack) == 0:
                bio_sequence.append(tag)
            else:
                _process_stack(stack, bio_sequence)
                bio_sequence.append(tag)
        elif tag[0] == "E":
            stack.append(tag)
        elif tag[0] == "I":
            stack.append(tag)
        elif tag[0] == "S":
            if len(stack) > 0:
                _process_stack(stack, bio_sequence)
            stack.append(tag)
        elif tag[0] == "B":
            if len(stack) > 0:
                _process_stack(stack, bio_sequence)
            stack.append(tag)
        else:
            raise ValueError("Invalid tag:", tag)

    if len(stack) > 0:
        _process_stack(stack, bio_sequence)

    return bio_sequence


# BIO2BIEOS
def bio_to_bioes(original_tags):
    def _change_prefix(original_tag, new_prefix):
        assert original_tag.find("-") > 0 and len(new_prefix) == 1
        chars = list(original_tag)
        chars[0] = new_prefix
        return "".join(chars)

    def _pop_replace_append(stack, bioes_sequence, new_prefix):
        tag = stack.pop()
        new_tag = _change_prefix(tag, new_prefix)
        bioes_sequence.append(new_tag)

    def _process_stack(stack, bioes_sequence):
        if len(stack) == 1:
            _pop_replace_append(stack, bioes_sequence, "S")
            # _pop_replace_append(stack, bioes_sequence, "U")
        else:
            recoded_stack = []
            _pop_replace_append(stack, recoded_stack, "E")
            # _pop_replace_append(stack, recoded_stack, "L")
            while len(stack) >= 2:
                _pop_replace_append(stack, recoded_stack, "I")
            _pop_replace_append(stack, recoded_stack, "B")
            recoded_stack.reverse()
            bioes_sequence.extend(recoded_stack)

    bioes_sequence = []
    stack = []

    for tag in original_tags:
        if tag == "O":
            if len(stack) == 0:
                bioes_sequence.append(tag)
            else:
                _process_stack(stack, bioes_sequence)
                bioes_sequence.append(tag)
        elif tag[0] == "I":
            if len(stack) == 0:
                stack.append(tag)
                print("warning: I- not after B-")
            else:
                this_type = tag[2:]
                prev_type = stack[-1][2:]
                if this_type == prev_type:
                    stack.append(tag)
                else:
                    _process_stack(stack, bioes_sequence)
                    stack.append(tag)
        elif tag[0] == "B":
            if len(stack) > 0:
                _process_stack(stack, bioes_sequence)
            stack.append(tag)
        else:
            raise ValueError("Invalid tag:", tag)

    if len(stack) > 0:
        _process_stack(stack, bioes_sequence)

    return bioes_sequence