import requests
import random

def get_random_quote():
    r = requests.get("https://api.quotable.io/random")
    data = r.json()
    return f'"{data["content"]}" — {data["author"]}'

def get_random_joke():
    r = requests.get("https://official-joke-api.appspot.com/random_joke")
    data = r.json()
    return f'{data["setup"]} {data["punchline"]}'

if __name__ == "__main__":
    choice = random.choice(["quote", "joke"])
    
    if choice == "quote":
        print(get_random_joke())
    else:
        print(get_random_joke())

#get_random_joke in else too cause random quote api is dead!
