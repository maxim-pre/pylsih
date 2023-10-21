import lang

while True:
    text = input('lang: ')

    result, error = lang.run(text)

    if error: print(error.as_string())
    else: print(result)