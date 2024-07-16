import re
import letter.templates as templates


def fill_empty_spaces(template):
    """gets raw string, based on context fills the gaps with {input}"""
    pattern = re.compile(r"(.*?{})")
    matches = pattern.findall(template)

    if not matches:
        return template

    user_inputs = []
    for i, match in enumerate(matches):
        context = " ".join(
            match.split()[-6:]
        )  # Might be IndexError, based on text, just raise -6 to -2 or so
        user_input = input(f"Enter word(s) to fill in after '{context}': ")
        user_inputs.append(user_input)

    return template.format(*user_inputs)


intro = lambda x: templates.intro_eng if x == 1 else templates.intro_rus

motivation = {
    1: lambda x: (
        fill_empty_spaces(templates.motivation_prod_eng)
        if x == 1
        else fill_empty_spaces(templates.motivation_prod_rus)
    ),
    2: lambda x: (
        fill_empty_spaces(templates.motivation_startup_eng)
        if x == 1
        else fill_empty_spaces(templates.motivation_startup_rus)
    ),
    3: lambda x: (
        fill_empty_spaces(templates.motivation_fintech_eng)
        if x == 1
        else fill_empty_spaces(templates.motivation_fintech_rus)
    ),
    4: lambda x: (
        fill_empty_spaces(templates.motivation_ecommerce_eng)
        if x == 1
        else fill_empty_spaces(templates.motivation_ecommerce_rus)
    ),
    5: lambda x: (
        fill_empty_spaces(templates.motivation_elt_eng)
        if x == 1
        else fill_empty_spaces(templates.motivation_elt_rus)
    ),
}

stack = {
    1: lambda x: (
        fill_empty_spaces(templates.stack_django_eng)
        if x == 1
        else fill_empty_spaces(templates.stack_django_rus)
    ),
    2: lambda x: (
        fill_empty_spaces(templates.stack_fastapi_eng)
        if x == 1
        else fill_empty_spaces(templates.stack_fastapi_rus)
    ),
    3: lambda x: (
        fill_empty_spaces(templates.stack_parser_eng)
        if x == 1
        else fill_empty_spaces(templates.stack_parser_rus)
    ),
    4: lambda x: (
        fill_empty_spaces(templates.stack_elt_eng) if x == 1 else fill_empty_spaces(templates.stack_elt_rus)
    ),
}

patterns = lambda x: (
    fill_empty_spaces(templates.patterns_eng) if x == 1 else fill_empty_spaces(templates.patterns_rus)
)

end = lambda x: templates.ending_eng if x == 1 else templates.ending_rus


my_dict = {"prod": 1, "startup": 2, "fintech": 3, "parsing": 4, "elt": 5}

stack_dict = {
    "django": 1,
    "fastapi": 2,
    "parsing": 3,
    "elt": 4,
}
