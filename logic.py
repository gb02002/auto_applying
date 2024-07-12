import texts


def start_logic(type_of_company: int, language: int) -> str:
    """"""
    result: str = ""
    result += texts.intro(language)
    result += texts.motivation[type_of_company](language)
    print(
        f"Which stack you'd like to use?\nYou have a choice of those: {list(texts.stack_dict.keys())}"
    )
    current_stack = str(input())
    result += texts.stack[texts.stack_dict[current_stack]](language)
    result += texts.patterns(language)
    print(result)
    result += texts.end(language)
    print(result)
    return result
