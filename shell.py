from src.run import run


while True:
    text = input('lang: ')

    result, error = run(text)

    if error: print(error.as_string())
    else: print(result)