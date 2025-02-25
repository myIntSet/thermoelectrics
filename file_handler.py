import numpy as np
import pandas as pd
import os

def save_file(I, I_var, J_QH, P, eff, sigma, TUR, epsilons, lamdas, INPUT):

    # Flatten the arrays
    Epsilon, Lamda = np.meshgrid(epsilons, lamdas)    # Create a 2D grid
    arrays = [Epsilon, Lamda, I, I_var, J_QH, P, eff, sigma, TUR]
    flattened_data = [array.flatten() for array in arrays]

    # Create a DataFrame for the results
    df_new = pd.DataFrame(np.column_stack(flattened_data), columns=['epsilon', 'lambda', 'I', 'I_var', 'J_QH', 'P', 'eff', 'sigma', 'TUR'])

    # Add the parameters as new columns (this will be the same for all rows)
    for param, value in INPUT.items():
        df_new[param] = value

    # Define the filename
    filename = 'results.csv'

    # Check if the CSV file already exists
    if os.path.exists(filename):
        print("It found the existing one")
        # Load the existing results
        df_existing = pd.read_csv(filename)
        print("Existing one:", df_existing.shape)

        # Concatenate the old and new results
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        print("combined one one:", df_combined.shape)

        df_combined = df_combined.round(6)  # Adjust the decimal places as needed
        # Drop duplicate rows (keeping only unique ones)
        df_combined = df_combined.drop_duplicates()
        print("After dropping duplicates:", df_combined.shape)

        # Save the updated DataFrame back to CSV
        df_combined.to_csv(filename, index=False)
    else:
        # If the file does not exist, just save the new results
        df_new.to_csv(filename, index=False)

    # Print the DataFrame to check the structure
    #print(df_results.head())