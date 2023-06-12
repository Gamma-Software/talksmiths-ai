
class InvalidPrompt(ValueError):
    """ Raised when the prompt is invalid """
    pass

def load_prompts(filename="prompts.txt") -> str:
    """ load the prompts from a file """
    with open(filename, 'r') as f:
        prompt_to_return = f.read()

    # Check whether its a valid prompt
    if len(prompt_to_return) < 1 or prompt_to_return is None:
        raise InvalidPrompt("Please check the prompt file and try again.")
    if not prompt_to_return.contains("{human}") \
        or not prompt_to_return.contains("{ai}") \
        or not prompt_to_return.contains("{history}"):
        raise InvalidPrompt("The prompt should at least contain {human}, {ai} and {history}")
    return prompt_to_return