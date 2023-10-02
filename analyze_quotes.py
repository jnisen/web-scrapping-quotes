import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

quotes = pd.read_csv('quotes.csv')

# Data Formatting
quotes['tags'] = quotes['tags'].str.split(',')

# How many quotes are?
num_quotes = quotes.shape[0]

# How many pages are in the dataset?
total_pages = max(quotes['page'])

# How many quotes are per page?
total_quotes_per_page = num_quotes / total_pages

# Obtain all the authors
list_authors = quotes['author'].unique()

# How many authors are in the DataFrame?
nro_authors = quotes['author'].nunique()

# Obtain all the tags
quotes_tag = quotes['tags']

# How many tags n/a and which are in the dataset?
count_quotes_without_na = quotes['tags'].isnull().sum()
df_quotes_without_na = quotes[quotes['tags'].isnull()]

# List of quotes
list_tags = list()

for quote_tags in quotes_tag:
    if isinstance(quote_tags, str):
        tags = quote_tags.split(',')
        for tag in tags:
            if tag not in list_tags:
                list_tags.append(tag)

count_quotes = len(list_tags)


# Grouped Authors Tags
def grouped_authors_tags(quotes):
    tags_author = quotes.explode("tags").groupby("tags").count()["quote"].reset_index()
    tags_author = tags_author.rename(columns={'quote': 'total_tags'})
    return tags_author.sort_values('total_tags', ascending=False)

# Create bar chart
def bar_chart(x, y, title, xlabel, ylabel, rotation, image):
    sns.barplot(x=x, y=y)
    plt.xlabel(f'{xlabel}')
    plt.ylabel(f'{ylabel}')
    plt.title(f'{title}')
    plt.xticks(rotation=rotation)
    plt.savefig(f'{image}.png')
    plt.close()

# Get Top 10 total tags
def top10_total_tags():
    sort_count_list_quotes = grouped_authors_tags(quotes)

    top10_list_quotes = sort_count_list_quotes[:10]
    tags = top10_list_quotes['tags']
    total_quotes = top10_list_quotes['total_tags']

    bar_chart(tags, total_quotes, 'Top 10 tags in Quotes', 'Tags', 'Counts Tags', 45, 'top10_in_tags')

# Get total quotes per author
def total_quotes_author():
    count_list_author = quotes.groupby(by='author').count()['quote'].reset_index()
    count_list_author = count_list_author.rename(columns={'quote': 'total'})
    sort_count_list_quotes = count_list_author.sort_values('total', ascending=False)

    tags = sort_count_list_quotes['author']
    total_quotes = sort_count_list_quotes['total']

    bar_chart(tags, total_quotes, 'Total quotes per Author', 'Author', 'Count Tags', 90, 'total_quotes_per_author')

# Get the tags per author
def save_png_author_tags():
    for author in list_authors:
        quotes_author = quotes[quotes['author'] == author]
        df_grouped_authors_tags = grouped_authors_tags(quotes_author)
        all_tags = df_grouped_authors_tags['tags']
        all_total_quotes = df_grouped_authors_tags['total_tags']

        if df_grouped_authors_tags.shape[0] >= 1:
            bar_chart(all_tags, all_total_quotes, author, 'Tags', 'Count Tags', 90, f'{author}_tag')
            print(f'✅️Downloaded tags from author: {author} ')
        else:
            print(f'🅾️ Author: {author} does not have tags')


save_png_author_tags()
total_quotes_author()
top10_total_tags()
