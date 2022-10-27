import pandas as pd
from mesa import Agent, Model
from tokenize import Number
import numpy as np
import pandas as pd
from pyswip import Prolog
from itertools import chain
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from sklearn.ensemble import RandomForestClassifier

class Agent_IOA(Agent): #Creating Agent
    # First Deliverable
    def __init__(self):
        print("Hello human, I'm your IOA")
    
    # Second Deliverable
    def get_best_product_to_buy(self, number_of_products_to_buy):
        sales_dataframe = pd.read_csv('sales_stats.csv')
        sales_dataframe[['entry_date','sold_date']] = sales_dataframe[['entry_date','sold_date']].apply(pd.to_datetime)
        sales_dataframe['days_inv'] = (sales_dataframe['sold_date'] - sales_dataframe['entry_date']) / np.timedelta64(1, 'D')
        print(sales_dataframe)
        sum_df = sales_dataframe.groupby(['product_id']).agg(
        sum_sale_price = ('sale_price','sum'),
        sum_cost = ('cost','sum'),
        sum_days_in_inv = ('days_inv', 'sum')
        ).reset_index()
        sum_df['profit_per_day'] = (sum_df['sum_sale_price'] - sum_df['sum_cost']) / sum_df['sum_days_in_inv']
        print(sum_df)
        products_to_buy_df = sum_df.nlargest(number_of_products_to_buy, columns=['profit_per_day', 'product_id'])
        print('\n-------------------------------Top ', number_of_products_to_buy, ' products to buy:--------------------\n')
        print(products_to_buy_df)

class Model_IOA(Model):
    agent = {}

    def __init__(self):
        self.agent = Agent_IOA()

    def secondDeliverable(self, products):
        self.agent.get_best_product_to_buy(products)


IOA = Model_IOA() #Results of first iteration
products_to_buy = int(input("How many products to buy?"))
IOA.secondDeliverable(products_to_buy) #Results of second iteration

#Third Deliverable
prolog = Prolog()
prolog.consult("LogicaTemporal.pl")

def analizarInv():
  # Funcion que analiza todos los productos del inventario llegado el caso de
  # y determina si con el presupuesto actual se puede reabastecer la cantidad
  # indicada
  q1 = prolog.query("analizarInventario(X, 8, 10000)") 

  print("Los productos que se pueden reabastecer son: \n")
  for i in q1:
    print(i)
  
  print("Por favor eliga uno de los anteriores")

analizarInv() # Results of third iteration


#Fourth Deliverable

# Antecedentes / Consecuentes
cost = ctrl.Antecedent(np.arange(0, 16, 1), 'cost')
demand = ctrl.Antecedent(np.arange(0, 16, 1), 'demand')
profitability = ctrl.Consequent(np.arange(0, 101, 1), 'profitability')

# Definir valores default
cost.automf(5)
demand.automf(5)

# Definir estados
profitability['low'] = fuzz.trimf(profitability.universe, [0, 0, 16])
profitability['below-average'] = fuzz.trimf(profitability.universe, [0, 16, 33])
profitability['average'] = fuzz.trimf(profitability.universe, [0, 33, 50])
profitability['above-average'] = fuzz.trimf(profitability.universe, [33, 50, 67])
profitability['high'] = fuzz.trimf(profitability.universe, [50, 67, 101])

# Reglas
rule1 = ctrl.Rule(cost['poor'] | demand['poor'], profitability['low'])
rule2 = ctrl.Rule(cost['mediocre'] | demand['mediocre'], profitability['below-average'])
rule3 = ctrl.Rule(((cost['decent'] & demand['average']) | (cost['average'] & demand['decent'])), profitability['average'])
rule4 = ctrl.Rule((cost['decent'] | demand['decent']), profitability['above-average'])
rule5 = ctrl.Rule((cost['good'] & demand['good']), profitability['high'])

profitability_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])

profitability_sim = ctrl.ControlSystemSimulation(profitability_ctrl)

profitability_sim.input['cost'] = 6.5
profitability_sim.input['demand'] = 9.8

profitability_sim.compute() # Results of fourth iteration

print(profitability_sim.output['profitability'])
profitability.view(sim=profitability_sim)

#Fifth Deliverable

df = pd.read_csv('sales_stats.csv')

target = []
for i in range(1000): #
    if df['demand_average'][i] > 0.5 and df['average_time_sale'][i] < 6.5: #determine whether it is profitable to purchase the product
        target.append(1)
    else:
       target.append(0)

df['target'] = target
#df.to_csv('Sales.csv', index=False) Export to use it in jupyter book


# Creamos 100 arboles cada uno con 1/10 de los datos, aleatorizando los features con el método de la raíz
# En este caso como tenemos que 5 columnas son relevantes, entonces √5 = 2.23 => más o menos 2, se usa como criterio
# de división gini, bootstrap es para que no se use todo el dataset, sino un subconjunto ofreciendo mejores resultados,
# oob_score, como se utiliza bootstrap puede que hayan datos que queden fuera del árbol, entonces este cuando crea el árbol
# valida los datos que quedaron por fuera con el árbol.
forest = RandomForestClassifier(n_estimators = 100,
                                criterion = "gini",
                                max_features = "sqrt",
                                bootstrap = True,
                                max_samples = 1/10,
                                oob_score = True) 

# entregamos los datos al bosque
forest.fit(
    df[["cost", "sale_price", "profitability", "demand_average", "average_time_sale"]].values,
    df["target"].values
    )

productos = [ #Results of fifth iteration
    ["Monitor", 3548219, 6841616, 3293397, 0.4674, 5.898],
    ["Gabinete", 644947, 1325399, 680452, 0.733, 4.901],
    ["Teclado", 122819, 333356, 210537, 0.3249, 8.798],
    ["Mouse", 505343, 1060152, 554809, 0.4539, 5.533],
    ["Procesador", 1959856, 3823726, 1863870, 0.5157, 8.916],
    ["RAM", 3407633, 6574503, 3166870, 0.6376, 4.028]
]

for i in productos:
  if forest.predict([i[1:]])[0] == 1:
    print("Es recomendable comprar el producto", i[0])
  else:
    print("No es recomendable comprar el producto", i[0])

print("Precisión de predicción", forest.oob_score_)

importances = pd.DataFrame(
    {'feature':["cost", "sale_price", "profitability", "demand_average", "average_time_sale"],
    'importance':np.round(forest.feature_importances_,3)}
)
importances = importances.sort_values('importance',ascending=False)
print(importances)
