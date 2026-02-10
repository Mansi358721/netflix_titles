
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

def load_and_clean_data(filepath):
    """Load dataset and perform initial cleaning."""
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Check for missing values
    print("\nMissing values before cleaning:")
    print(df.isnull().sum())
    
    # Fill missing values
    df['director'].fillna('Unknown', inplace=True)
    df['cast'].fillna('Unknown', inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    
    # Drop rows where date_added or rating is missing (small percentage usually)
    df.dropna(subset=['date_added', 'rating'], inplace=True)
    
    # Convert date_added to datetime
    df['date_added'] = df['date_added'].str.strip()
    df['date_added'] = pd.to_datetime(df['date_added'], format='mixed', errors='coerce')
    
    # Extract year and month added
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month_name()
    
    print("\nMissing values after cleaning:")
    print(df.isnull().sum())
    
    return df

def analyze_movies_vs_tv_shows(df):
    """Analyze the count of Movies vs TV Shows."""
    print("\n--- Movies vs TV Shows ---")
    type_counts = df['type'].value_counts()
    print(type_counts)
    
    plt.figure(figsize=(10, 6))
    sns.countplot(x='type', data=df, palette='viridis')
    plt.title('Distribution of Movies vs TV Shows')
    plt.savefig('distribution_type.png')
    plt.close()

def analyze_content_growth(df):
    """Study Netflix content growth over time."""
    print("\n--- Content Growth Over Time ---")
    data_by_year = df.groupby('year_added').size().reset_index(name='count')
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='year_added', y='count', data=data_by_year, marker='o')
    plt.title('Content Added to Netflix Over the Years')
    plt.xlabel('Year Added')
    plt.ylabel('Number of Titles')
    plt.savefig('content_growth.png')
    plt.close()

def identify_top_genres(df):
    """Identify top genres."""
    print("\n--- Top Genres ---")
    # Split 'listed_in' as some titles have multiple genres
    genres = df['listed_in'].str.split(', ', expand=True).stack().value_counts()
    print("Top 10 Genres:")
    print(genres.head(10))
    
    plt.figure(figsize=(12, 8))
    sns.barplot(y=genres.head(10).index, x=genres.head(10).values, palette='mako')
    plt.title('Top 10 Genres on Netflix')
    plt.xlabel('Count')
    plt.ylabel('Genre')
    plt.savefig('top_genres.png')
    plt.close()

def analyze_runtime(df):
    """Analyze runtime distribution."""
    print("\n--- Runtime Analysis ---")
    # Separate Movies and TV Shows
    movies = df[df['type'] == 'Movie'].copy()
    
    # Extract numeric value from duration
    # Some durations might be missing or weird, handled by regex extraction ideally
    # format "90 min"
    movies['duration_min'] = movies['duration'].str.replace(' min', '', regex=False)
    movies['duration_min'] = pd.to_numeric(movies['duration_min'], errors='coerce')
    
    plt.figure(figsize=(12, 6))
    sns.histplot(movies['duration_min'].dropna(), kde=True, color='red')
    plt.title('Distribution of Movie Duration')
    plt.xlabel('Duration (minutes)')
    plt.savefig('movie_duration_dist.png')
    plt.close()


def analyze_release_years(df):
    """Analyze top release years."""
    print("\n--- Top Release Years ---")
    release_years = df['release_year'].value_counts().head(10)
    print(release_years)
    
    plt.figure(figsize=(12, 6))
    sns.countplot(x='release_year', data=df, order=release_years.index, palette='rocket')
    plt.title('Top 10 Release Years')
    plt.xlabel('Release Year')
    plt.ylabel('Count')
    plt.savefig('top_release_years.png')
    plt.close()

def main():
    filepath = r'c:\Users\gkgan\Downloads\netflix\netflix_titles.csv'
    try:
        df = load_and_clean_data(filepath)
        analyze_movies_vs_tv_shows(df)
        analyze_content_growth(df)
        identify_top_genres(df)
        analyze_runtime(df)
        analyze_release_years(df)
        print("\nAnalysis complete. Plots saved as PNG files.")
    except FileNotFoundError:

        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
