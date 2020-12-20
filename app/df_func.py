import pandas as pd

def file_to_pd(file):
    dicts_from_file = []
    with open(file, encoding='utf-8') as inf:
        for line in inf:
            dicts_from_file.append(eval(line))

    return pd.DataFrame(dicts_from_file)


def customer_inn(df, inn):
    print(f'Контракты заказчика {df[df["customer_inn"] == inn]["customer_name"][0]} (ИНН {inn})')
    print(df[df['customer_inn'] == inn][[
        'conruct_num', 'contract_sub', 'publish_date', 
        'sign_date', 'price', 'url'
        ]])
    
def supplier_inn(df, inn):
    if df[df['sup_inn'] == inn]['sup_ip'][0] == True:
        name = ' '.join([df[df['sup_inn'] == inn]['sup_lname'][0], 
            df[df['sup_inn'] == inn]['sup_fname'][0],
            df[df['sup_inn'] == inn]['sup_mname'][0]])
        print(f'Контракты поставщика {name} (ИНН {inn})')
    else:   
        print(f'Контракты поставщика {df[df["sup_inn"] == inn]["sup_name"][0]} (ИНН {inn})')
    print(df[df['sup_inn'] == inn][[
        'conruct_num', 'contract_sub', 'publish_date', 
        'sign_date', 'price', 'url'
        ]])