# Airbnb Barcelona Analysis

## Overview

This repository contains a statistical analysis of Airbnb listings in Barcelona, examining how short-term rentals impact the city's housing market through data-driven insights. We analyse accommodation patterns, pricing structures, and neighbourhood characteristics while highlighting both economic benefits and challenges associated with the platform's growth. Our approach includes descriptive statistics, correlation studies, and visual representations to identify market trends and inequalities across districts. This project is relevant as Barcelona balances tourism demands with residents' needs, especially as housing decisions become increasingly difficult for locals and students.

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
