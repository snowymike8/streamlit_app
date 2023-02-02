import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔  Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞  Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')
#Fruit Picker
selected_fruits = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))#,['Avocado','Strawberries'])
#Table of options
showme = my_fruit_list.loc[selected_fruits]
streamlit.dataframe(showme)

#New section for fruityvice api
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    function_return = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(function_return)
except URLError as e:
  streamlit.error()



#streamlit.stop()


streamlit.header("The fruit load list contains:")
#Snowflake-realted functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
  
#Add button to load fruit:
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_load_list()
  streamlit.dataframe(my_data_row)
#streamlit.text("The fruit load list contains:")
#streamlit.text(my_data_row)
#added_fruit = streamlit.text_input("What fruit would you like to add?","jackfruit")
#streamlit.write('Thanks for adding ', added_fruit)
#my_cur.execute("insert into fruit_load_list values ('from streamlit')")

