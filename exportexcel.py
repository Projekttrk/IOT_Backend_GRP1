import pandas as pd

cars = {'Brand': ['Honda Civic', 'Toyota Corolla', 'Ford Focus', 'Audi A4'],
        'Price': [32000, 35000, 37000, 45000]
        }

df = pd.DataFrame(cars, columns=['Brand','Price'])

df.to_excel(r"C:\Users\Jovan\Desktop\export_dataframe.xlsx", index=False, header=True)
