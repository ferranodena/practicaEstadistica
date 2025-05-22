# Statistics Practice Project

## Overview

This repository contains the statistical analysis of Airbnb listings in Barcelona. The project applies fundamental statistical concepts to analyze accommodation patterns, pricing, and neighborhood characteristics across Barcelona's districts.

## Repository Structure

- `dataset cleanse/`: Scripts for data preprocessing
  - `neteja_bàsica.py`: Main cleaning script
  - `barcelona_listings.csv`: Raw data
  - `base_dades_districtes.csv`: Processed data
- `analysis/`: Statistical analysis notebooks/scripts
  - `questions/` Contains the RMarkdown files used to answer the questions
    - `4.1.rmd`: Analysis for the first question
    - `4.2.rmd`: Analysis for the second question
    - `4.3.rmd`: Analysis for the third question
    - `4.4.rmd`: Analysis for the fourth question
  - `correlations.rmd`: Creates the correlatiom map between the numeric variables
  - `general_analysis.rmd`: General analysis of the dataset
  - `inference.rmd`: Inference analysis
- `graphs/`: Contains the 20+ graphs used in the project, ordered by their appearance in the report
  - `base_dades_districtes.csv`: Processed data again, necessary to be here to be able to run the graphs
- `README.md`: This file

## Authors

This project was developed by:

- Ferran Òdena
- Pol Riera
- Jan Estrada
- Carlos Palazón 