import requests
from bs4 import BeautifulSoup as bs

def find_quote():
    # Зависимости
    fin = open('test.txt', 'w')
    logs = open('logs_parser.txt', 'w')

    URL = 'https://citaty.info/random'
    r = requests.get(URL)
    soup = bs(r.text, 'html.parser')
    otv = []
    errors = 0

    # Поиск цитаты
    quote_tech = soup.find_all('div', class_='field-item even last')
    logs.write(str(quote_tech))
    for item in quote_tech:
        quote = item.p
        quote = str(quote)[3:][:-4]
        while '<' in quote:
            for i in range(len(quote)):
                if quote[i] == '<':
                    st = i
                if quote[i] == '>':
                    en = i
            quote = quote[:(st)]+quote[(en+1):]
        otv.append((quote + '\n'))

    logs.write('\n')
    otv.append('-----------------\n')

    # Поиск автора
    author_tech = soup.find_all('div', class_='field-item even')
    logs.write(str(author_tech))
    for item in author_tech:
        author_fin = ''
        try:
            author_fin += str(item.a['title'])
        except:
            errors += 1
        author_fin += ' - '
        author = str(item)
        while '<' in author:
            for g in range(len(author)):
                if author[g] == '<':
                    st = g
                if author[g] == '>':
                    en = g
            author = author[:(st)]+author[(en+1):]
        author_fin += author
        otv.append(author_fin + '\n')

    # Редактор ошибок
    while errors > 0:
        otv.pop(-1)
        errors -= 1

    # Финальная запись в файл
    for i in otv:
        fin.write(i)

    fin.close()
    logs.close()

    return ''.join(otv)
