import tkinter as tk
from tkinter import ttk
import requests


API_URL = ""


def fetch_rates():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data["conversion_rates"]
    except requests.RequestException as e:
        print(f"API bağlantı hatası: {e}")
        return {}


def convert_currency():
    try:
        amount = float(amount_entry.get())
    except ValueError:
        result_label.config(text="Enter a valid amount!")
        return

    source_currency = source_currency_var.get()
    target_currency = target_currency_var.get()

    if source_currency in rates and target_currency in rates:
        source_rate = rates[source_currency]
        target_rate = rates[target_currency]
        converted_amount = amount * (target_rate / source_rate)
        result_label.config(text=f"{amount} {source_currency} = {converted_amount:.2f} {target_currency}")
    else:
        result_label.config(text="Incorrect exchange rate selection!")


def on_keypress(event, combobox):
    key = event.char.upper()
    for index, value in enumerate(combobox['values']):
        if value.startswith(key):
            combobox.current(index)
            break


root = tk.Tk()
root.title("Exchange Rate Converter")
root.geometry("400x300")


rates = fetch_rates()


currency_list = list(rates.keys())


amount_label = tk.Label(root, text="Amount:")
amount_label.pack(pady=10)
amount_entry = tk.Entry(root)
amount_entry.pack()


source_currency_var = tk.StringVar()
source_label = tk.Label(root, text="Source Currency:")
source_label.pack(pady=5)
source_dropdown = ttk.Combobox(root, textvariable=source_currency_var, values=currency_list, state="readonly")
source_dropdown.pack()


target_currency_var = tk.StringVar()
target_label = tk.Label(root, text="Target Currency:")
target_label.pack(pady=5)
target_dropdown = ttk.Combobox(root, textvariable=target_currency_var, values=currency_list, state="readonly")
target_dropdown.pack()


source_dropdown.bind('<KeyRelease>', lambda event: on_keypress(event, source_dropdown))
target_dropdown.bind('<KeyRelease>', lambda event: on_keypress(event, target_dropdown))


convert_button = tk.Button(root, text="Exchange", command=convert_currency)
convert_button.pack(pady=20)


result_label = tk.Label(root, text="")
result_label.pack(pady=10)


root.mainloop()
