import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import random
import time


# after import the package, open a terminal, run the code 'streamlit run xxx.py'. A new tab will open in you browser.
# everytime save the script, the tab will be updated.

# add a title
st.title('Basic 01') 

# add a header 
st.header('This is a header')

# add text
st.write('In this script, I will go throgh some basics of streamlit.') 

# add some code
code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language='python')

# add markdown
name = 'NC State'
st.markdown(f' # Markdown Head 1')
st.write(f' # Markdown Head 1. Wow, st.write() also works') 
st.markdown(f'{name} is **_really_ cool**. I like the weather there.')
st.markdown('```here is some code```')

# You can pass almost anything to st.write(): text, data, Matplotlib figures, Altair charts, and more. Don’t worry, Streamlit will figure it out and render things the right way.

st.write('Create a pandas dataframe')
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))


st.write('Charts:')

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

# or we can build the chart first and use st.write() to plot it.
c = alt.Chart(chart_data).mark_circle().encode(x='a', y='b', size='c', color='c')

st.write('Here is the same chart:', c)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

# matplotlib
arr = np.random.normal(1, 1, size=100)

st.write('Here is a histrogram:', plt.hist(arr, bins=20)) # TODO why?

plt.hist(arr, bins=20)
st.pyplot()

# add widgets

# check box 
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.line_chart(chart_data)

if st.checkbox('Guest a number from 1 to 10'):
    st.write(random.randint(1,10))
    

    
# selectbox
option = st.selectbox(
    'Which number do you like best?',
     chart_data['a'])

'You selected: ', option

# Put widgets in a sidebar
option = st.sidebar.selectbox(
    'Which number do you like best?',
     chart_data['a'])

'You selected: ', option

if st.sidebar.checkbox('Guest a number from 1 to 10'):
    st.write(random.randint(1,10))
    

# progress bar
'Starting a long computation...'

# Add a placeholder
# latest_iteration = st.empty()
# bar = st.progress(0)

# for i in range(100):
#   # Update the progress bar with each iteration.
#   latest_iteration.text('Iteration %d' % i)
#   bar.progress(i + 1)
#   time.sleep(0.1)

'...and now we\'re done!'

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))


# insert elements out of order
st.text('This will appear first')
# Appends some text to the app.

my_slot1 = st.empty()
# Appends an empty slot to the app. We'll use this later.

my_slot2 = st.empty()
# Appends another empty slot.

st.text('This will appear last')
# Appends some more text to the app.

my_slot1.text('This will appear second')
# Replaces the first empty slot with a text string.

my_slot2.line_chart(np.random.randn(20, 2))
# Replaces the second empty slot with a chart.


progress_bar = st.progress(0)
status_text = st.empty()
chart = st.line_chart(np.random.randn(10, 2))

for i in range(100):
    # Update progress bar.
    progress_bar.progress(i)

    new_rows = np.random.randn(10, 2)

    # Update status text.
    status_text.text(
        'The latest random number is: %s' % new_rows[-1, 1])

    # Append data to the chart.
    chart.add_rows(new_rows)

    # Pretend we're doing some computation that takes time.
    time.sleep(0.1)

status_text.text('Done!')
st.balloons()

import numpy as np
import time

# Get some data.
data = np.random.randn(10, 2)

# Show the data as a chart.
chart = st.line_chart(data)

# Wait 1 second, so the change is clearer.
time.sleep(1)

# Grab some more data.
data2 = np.random.randn(10, 2)

# Append the new data to the existing chart.
chart.add_rows(data2)