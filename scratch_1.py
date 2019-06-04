import psycopg2 as pg
import pandas as pd
import matplotlib.pyplot as plt

#connect to postgreSQL
connect = pg.connect(database='stockdb'
                     , host='142.93.196.0'
                     , port='5432'
                     , user='stock'
                     ,password='???')

cursor = connect.cursor()

#get data
def load_data(table):

    sql_command = "SELECT * FROM {};".format(str(table))
    print (sql_command)

    # Load the data
    data = pd.read_sql(sql_command, connect)

    # print(data)
    return (data)

#collect 2 columns for pivot table
new_data = load_data('tbl_quy_analyst_3')[['revenue_growth', 'capital_growth']]

# print(new_data)

#customize pivot table
pivot_table = pd.pivot_table(new_data, index='capital_growth',columns='revenue_growth', aggfunc='size')
pivot_table = pivot_table.reindex(['[Low, -30)', '[-30, 0)', '[0, 30)', '[30, High)'])
pivot_table = pivot_table[['[Low, -30)', '[-30, 0)', '[0, 30)', '[30, High)']]

#total value
sum_value = pivot_table.sum().sum()

#percentage value
final_table = (pivot_table/sum_value * 100).round(2)
print(final_table)

#Visualization
plt.plot(final_table)
plt.title('Correlation between revenue and capital')
plt.xlabel('Revenue Growth')
plt.ylabel('Capital Growth')
plt.show()




