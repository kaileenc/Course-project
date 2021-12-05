import streamlit as st
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype
import sklearn
from sklearn.cluster import KMeans
import altair as alt
import seaborn as sns
import openpyxl as openpyxl

st.title("Analyzing Characteristics of K-Pop Listeners")

df = pd.read_excel(r'C:\Users\Kaileen\Documents\UCI\uci fall 2021\math 10\KPOP Data.xlsx', engine='openpyxl')

#first, clean the data

#remove column "Timestamp" as it has no useful information
df = df.drop("Timestamp",1)

#first replace null values in the data set with the string "none"

df = df.replace(np.nan, "none")

#next, clean the data by generalizing the values and making the columns that should be numerical numerical

#cleaning the column "Which is your favourite K-Pop group?"
group_list = list(df["Which is your favourite K-Pop group?"])
df["Which is your favourite K-Pop group?"] = ["other(s)" if (";" in x) or ("and" in x) or ("," in x) else x for x in group_list]
group = {"Got7":"GOT7","TWICE":"Twice","G idle":"(G)I-dle","Seventern ":"Seventeen","SEVENTEEN":"Seventeen",
         "Seventeen ":"Seventeen","Stray kids":"Stray Kids","Stray Kids ":"Stray Kids","ASTRO":"Astro","Multiple ":"other(s)"}
for key in group:
    x = key
    df = df.replace(x,f"{group[x]}")

#cleaning the column "When did you start listening to K-Pop?"
d = {"3-4 years ago":3.5,"More than 4 years ago":4,"1 -2 years ago":1.5,  "Less than a year ago":1, "7 years ago":7,
     "9 years coming April ":9, 
     "About 6 years ago, I got introduced to 2ne1 which was their song called â€œI am the bestâ€. So sad they disbanded": 6,
     "8+ years ago": 8, "9 years, since 2010": 9, "7 years": 7, 
     "Iâ€™ve been listening to it all my life basically, my cousins are Asian, and Iâ€™m mexican, so people think Iâ€™m just a koreaboo, when in reality Iâ€™ve only ever listened to korean and Chinese music": 6,
     "Started in 2006": 14}
for key in d:
    x = key
    df = df.replace(x,f"{d[x]}")
df["When did you start listening to K-Pop?"] = df["When did you start listening to K-Pop?"].apply(pd.to_numeric)

#cleaning the column "How many hours do you spend listening to K-Pop?"
df.iloc[156, 5] = '5 or more'
df.iloc[170, 5] = '5 or more'
dict_ = {"2-4 hours":3,"5 or more":5,"Less than an hour":0.5, "2020-07-24 00:00:00":5, "Most of the time.":10,
         "depends if iâ€™m in the mood for it":10, "Eh":10, 
         "Itâ€™s mainly the only music I listen to anymore, I listen to music all the time":10, "All the time.":10, 
         "The whole day almost":10, "Over half of my day (12+ hours)":10, 
         "Every time but only when I get the chance cause Iâ€™m busy with school .":10, "Hours on end":10, 
         "Nearly every hour unless im sleeping":10, 
         "Idk depends on my mood. But I can liste during multiple hours definitely. ":10, 
         "Everyday":10, "I mix in other songs in other languages too so very Day is different ":10, 
         "All day":10, "Whenever Iâ€™m listening to music, basically":10, 
         "Anytime I listen to music thatâ€™s all I listen to":10, 
         "It's depend on day. Usually one or two hours, sometimes more, sometimes, when I overeat kpop I need to do break. ":10, 
         "Everyday ":10, "Almost all day":10, "Everyday, constantly ":10, 
         "Any chance that i get. (I dont really count the hours) ":10, 
         "I don't rlly listen to music, music is like food to me. When I crave a song, I listen to it. So probably less than an hour? When Monsta X has comebacks I do stream (but it's just playing in the background sometimes my earphones are plugged in so I don't actually hear it)... I listen to it for almost the whole day I guess... gotta get those views and wins ":10}
for key in dict_:
    x = key
    df = df.replace(x,f"{dict_[x]}")
df["How many hours do you spend listening to K-Pop?"] = df["How many hours do you spend listening to K-Pop?"].apply(pd.to_numeric)
    
#cleaning the column "How old are you?"
age = {"15 - 20 years":18, "21 - 26 years":24, "10 - 14 years":12, "27 - 30":29}
for key in age:
    x = key
    df = df.replace(x,f"{age[x]}")
df["How old are you?"] = df["How old are you?"].apply(pd.to_numeric)

#cleaning the column "If you do watch K-Pop music videos, how long do you spend watching them?"
dictionary = {"1 hour":1,"2-3 hours":2.5,"3-4 hours":3.5,"More than four hours":4,"none":0}
for key in dictionary:
  x = key
  df = df.replace(x,f"{dictionary[x]}")

df["If you do watch K-Pop music videos, how long do you spend watching them?"] = df["If you do watch K-Pop music videos, how long do you spend watching them?"].apply(pd.to_numeric)
    
#cleaning the column "Which country are you from?"
country = {"A country in the UK": "UK", "Other European countries": "European country", "Canada ": "Canada"," Canada ": "Canada", 
           "canada": "Canada", "CANNNAADAAAA BOIIIIIIS": "Canada", "Other Asian country": "Asian country", "Australia ": "Australia",
           "A country from the Caribbean ": "other", "South Africa": "other", "South Africa ": "other", "Finland": "other", 
           "Sweden": "other", "Turkey": "other"}
for key in country:
    x = key
    df = df.replace(x,f"{country[x]}")
    
#cleaning the column "What is your profession?"
profession = {"student": "Student", "receptionist at an office for a clothing store": "Receptionist", "Student ": "Student",
             "To either be a designer, artist or an animator.": "Student", "None of the above.": "Unemployed", 
              "Full time worker": "Worker", "College Student": "Student", "I have job, plain n simple": "Worker",
             "Medical laboratory technician ": "Nursing/Medical", "Nurse": "Nursing/Medical", "Nursing/Medical ": "Nursing/Medical",
             "I don't have a profession.": "Unemployed", "Berklee Student": "Student"}
for key in profession:
    x = key
    df = df.replace(x,f"{profession[x]}")
df["What is your profession?"].value_counts()

#shortening the results of the column "What is your gender?" so the seaborn chart is easier to read
gender = {"Female":"F","Male":"M"}
for key in gender:
    x = key
    df = df.replace(x,f"{gender[x]}")
df["What is your gender?"].value_counts()


st.header("1. Listening habits of K-Pop fans")
#next, we will use KMeans clustering from scikit-learn
numeric_cols = [c for c in df.columns if is_numeric_dtype(df[c])]
df2 = df[numeric_cols].copy()
kmeans = KMeans(3)
kmeans.fit(df2)
kmeans.predict(df2)
df2["cluster"] = kmeans.predict(df2)

#now we will make an altair chart based off of two numerical columns that the user will chose to view our clustering
x_axis = st.selectbox("Please choose an x-value",numeric_cols)
y_axis = st.selectbox("Please choose a y-value", numeric_cols)
chart = alt.Chart(df2).mark_circle().encode(
    x = x_axis,
    y = y_axis,
    color = "cluster:N",
    tooltip = [x_axis, y_axis, "count()"]
    
)
st.altair_chart(chart, use_container_width = True)

st.write(f"We can see in this chart K-Pop listeners' responses to {x_axis} compared to {y_axis}")
st.write("Additionally, we can see the number of responses that are at the same point.")
st.write("While we did use clustering in this chart, there isn't much information we can obtain from it with these variables.")

#altair bar chart of which groups are surveyees' favorites

st.header("2. Listeners' favorite groups")

group_chart = alt.Chart(df).mark_bar().encode(
    x = "Which is your favourite K-Pop group?",
    y = "count()"
)
st.altair_chart(group_chart, use_container_width = True)

st.write("In this chart, we can see listeners favorite K-Pop groups and how many chose that group. The column 'other(s)' represents those who put more than one group as their favorite.")
st.write("We can see that most people like BTS the most. Next are those who like more than one group which may or may not include BTS.")

# altair chart comparing listener's demographics with their favorite groups

st.header("3. Fan demographics and their favorite groups")
st.subheader("First, we will compare a listener's favorite group with their age and which country they are from.")
brush = alt.selection_interval(empty='none')

listener_chart = alt.Chart(df).mark_point().encode(
    x = "Which is your favourite K-Pop group?",
    y = "Which country are you from?",
    color = alt.condition(brush,
                          alt.Color("How old are you?:Q", scale=alt.Scale(scheme='plasma',reverse=True)),
                          alt.value("lightgrey")),
    tooltip = ["Which country are you from?","Which is your favourite K-Pop group?","How old are you?", "count()"]
).add_selection(
    brush,
).properties(
    title="Fans' favorite K-Pop group compared to their home country and age"
)

st.altair_chart(listener_chart, use_container_width = True)

st.write("In the chart above we can see the diversity of K-Pop fans all around the world. BTS has fans from every country listed here and they also have the biggest age range of fans.")
st.write("Almost every group listed has fans from the USA and the majority of the fans from this survey are from the USA.")

#adding a column to see whether a listener's favorite group is BTS or not
df["BTS"] = df["Which is your favourite K-Pop group?"].map(lambda fav_group: "BTS" in fav_group)

st.subheader("Now we will compare if a fan's favorite group is BTS and what their age and profession is.")

#seaborn chart
g = sns.FacetGrid(df, col="BTS")
g.map(sns.scatterplot, "What is your gender?","What is your profession?", alpha=.7)
st.pyplot(g)

st.write("Because so many of the surveyees are BTS fans, we will compare BTS fans and other K-Pop fans in general. We can see across all K-Pop fans that their professions range greatly from students to medical professionals.")

st.write("Despite the belief that K-Pop fans are all teenage girls, we can see through these two charts that is actually not true. While BTS has the most diverse fandom age-wise, all K-Pop fans come from different walks of life as evident from this survey.")
#extra Streamlit component that is a sidebar with a Table of Contents
with st.sidebar:
    st.write("Table of Contents")
    st.write("1. Listening habits of K-Pop fans")
    st.write("2. Listeners' favorite groups")
    st.write("3. Fan demographics and their favorite groups")
    st.write("4. Github Repository")
    st.write("5. References")
    
st.header("4. Github Repository")
st.write("Github Repository link: https://github.com/kaileenc/Course-project")

st.header("5. References:")
st.write("This dataset was obtained from https://figshare.com/articles/dataset/KPOP_DATA_xlsx/12093648/2")
st.write("The cleaning of this code was taken from https://towardsdatascience.com/analyzing-k-pop-using-machine-learning-part-1-data-collection-cleaning-4b407baf7bce")
st.write("The code for interactive altair charts is from the class notes https://christopherdavisuci.github.io/UCI-Math-10/Week3/First-Altair-examples.html")
st.write("The code to count the number of points on the graph in the tooltip is from https://github.com/altair-viz/altair/issues/1065")
st.write("The code to make a seaborn chart is from https://seaborn.pydata.org/tutorial/axis_grids.html")
st.write("The code to display the seaborn chart in Streamlit is from https://pythonwife.com/seaborn-with-streamlit/")

