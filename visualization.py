import matplotlib.pyplot as plt
import pandas as pd
import sys


def load_data():
    try:
        # Load CSV files with pandas
        df_persons = pd.read_csv('persons.csv')
        df_pets = pd.read_csv('pets.csv')
        df_occupations = pd.read_csv('occupations.csv')
        return df_persons, df_pets, df_occupations
    except FileNotFoundError as e:
        print(f"Error: Could not find one of the required CSV files: {e}")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("Error: One of the CSV files is empty")
        sys.exit(1)


def plot_pets_per_person(df_persons, df_pets):
    try:
        # Count number of pets per person
        pets_per_person = df_pets.groupby('owner_id').size().reset_index(name='pet_count')
        merged = pd.merge(df_persons, pets_per_person, left_on='person_id', right_on='owner_id', how='left').fillna(0)

        plt.figure(figsize=(12, 6))
        plt.bar(merged['full_name'], merged['pet_count'], color='skyblue')
        plt.xlabel('Person Name')
        plt.ylabel('Number of Pets')
        plt.title('Number of Pets per Person')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Save the plot before showing it
        plt.savefig('pets_per_person.png')

        # Add a small pause to ensure the plot is fully rendered
        plt.pause(1)
        plt.close()

    except Exception as e:
        print(f"Error in plot_pets_per_person: {e}")
        plt.close()


def plot_pet_species_distribution(df_pets):
    try:
        species_counts = df_pets['species'].value_counts()

        plt.figure(figsize=(8, 8))
        plt.pie(species_counts.values, labels=species_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title('Distribution of Pet Species')
        plt.axis('equal')

        plt.savefig('pet_species_pie.png')
        plt.pause(1)
        plt.close()

    except Exception as e:
        print(f"Error in plot_pet_species_distribution: {e}")
        plt.close()


def plot_pets_and_occupations(df_persons, df_pets, df_occupations):
    try:
        pets_count = df_pets.groupby('owner_id').size().reset_index(name='pet_count')
        occupations_count = df_occupations.groupby('person_id').size().reset_index(name='occupation_count')

        merged = pd.merge(pets_count, occupations_count,
                          left_on='owner_id', right_on='person_id',
                          how='outer').fillna(0)

        plt.figure(figsize=(10, 6))
        plt.scatter(merged['occupation_count'], merged['pet_count'], alpha=0.5)
        plt.xlabel('Number of Occupations')
        plt.ylabel('Number of Pets')
        plt.title('Relationship between Number of Pets and Occupations')
        plt.grid(True, linestyle='--', alpha=0.7)

        plt.savefig('pets_vs_occupations.png')
        plt.pause(1)
        plt.close()

    except Exception as e:
        print(f"Error in plot_pets_and_occupations: {e}")
        plt.close()


def plot_popular_pet_names(df_pets):
    try:
        name_counts = df_pets['pet_name'].value_counts().head(10)

        plt.figure(figsize=(10, 6))
        name_counts.plot(kind='bar', color='lightgreen')
        plt.xlabel('Pet Name')
        plt.ylabel('Count')
        plt.title('Most Common Pet Names')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.savefig('popular_pet_names.png')
        plt.pause(1)
        plt.close()

    except Exception as e:
        print(f"Error in plot_popular_pet_names: {e}")
        plt.close()


if __name__ == "__main__":
    try:
        print("Loading data...")
        df_persons, df_pets, df_occupations = load_data()

        print("\nGenerating visualizations...")
        print("1. Creating pets per person plot...")
        plot_pets_per_person(df_persons, df_pets)

        print("2. Creating pet species distribution plot...")
        plot_pet_species_distribution(df_pets)

        print("3. Creating pets vs occupations plot...")
        plot_pets_and_occupations(df_persons, df_pets, df_occupations)

        print("4. Creating popular pet names plot...")
        plot_popular_pet_names(df_pets)

        print("\nAll visualizations have been created and saved as PNG files!")

    except KeyboardInterrupt:
        print("\nVisualization process interrupted by user.")
        plt.close('all')
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        plt.close('all')