import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))


# creating Dataframe
def txt_to_df(name):
    with open(name, 'r') as f:
        lines = f.readlines()

    words = [word for line in lines for word in line.strip().split()]

    dataframe = pd.DataFrame({'Word': words})

    # Create a counts DataFrame
    counts_df = dataframe['Word'].value_counts().reset_index()
    counts_df.columns = ['Word', 'Count']

    return counts_df


# Function to generate and save word cloud
def generate_wordcloud(data, output_file):
    wordcloud = WordCloud(width=800, height=400, background_color='black'). \
        generate_from_frequencies(data.set_index('Word')['Count'])

    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(output_file)
    plt.show()


# Function to plot top terms and save as image
def plot_top_terms(df1, num_terms, save_filename='most_freq_terms.png'):
    # Select the top n terms
    top_terms = df1.head(num_terms)

    # Plot the bar plot using Plotly Express
    fig = px.bar(top_terms, x='Word', y='Count',
                 labels={'Count': 'Frequency'},
                 title=f'Top {num_terms} Frequent Terms')

    fig.update_layout(xaxis_tickangle=-45)

    # Save the plot as an image file
    fig.write_image(save_filename)

    # Display the plot
    fig.show()


df = txt_to_df('un_declaration_hr_text_data.txt')

# deleting stopwords from dataframe
df = df[~df['Word'].isin(stopwords)]

# Generate and save the word cloud
generate_wordcloud(df, 'word_cloud.png')

# Plot the top 25 frequent terms and save as image
plot_top_terms(df, 25, 'most_freq_terms.png')
