import numpy as np
import pandas as pd
import os

#epsilons_R should be of the same length as epsilons_L
def save_file(I, I_var, J_QH, P, eff, sigma, TUR, epsilons, lamdas, INPUT, epsilons_R=None):

    # Flatten the arrays
    Epsilon_L, Lamda = np.meshgrid(epsilons, lamdas)    # Create a 2D grid

    if epsilons_R:
        Epsilon_R, _ = np.meshgrid(epsilons_R, lamdas)
        print("Found epsilon R!")
    else:
        Epsilon_R = Epsilon_L
        print("No epsilon R!")

    arrays = [Epsilon_L, Epsilon_R, Lamda, TUR, I, I_var, J_QH, P, eff, sigma]
    flattened_data = [array.flatten() for array in arrays]

    # Create a DataFrame for the results
    df_new = pd.DataFrame(np.column_stack(flattened_data), columns=['epsilon_L', 'epsilon_R', 'lambda', 'TUR', 'I', 'I_var', 'J_QH', 'P', 'eff', 'sigma'])

    # Add the parameters as new columns (this will be the same for all rows)
    for param, value in INPUT.items():
        df_new[param] = value

    df_new.to_csv('latest_results.csv', index=False)

    # Define the filename
    filename = 'results.csv'

    # Check if the CSV file already exists
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename)
        print("Existing one:", df_existing.shape)

        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        print("combined one one:", df_combined.shape)

        df_combined = df_combined.round(6)  # Adjust the decimal places as needed
        df_combined = df_combined.drop_duplicates()
        print("After dropping duplicates:", df_combined.shape)

        # Save the updated DataFrame back to CSV
        df_combined.to_csv(filename, index=False)
    else:
        # If the file does not exist, just save the new results
        print("Saved to a new results file")
        df_new.to_csv(filename, index=False)

    # Print the DataFrame to check the structure
    #print(df_results.head())