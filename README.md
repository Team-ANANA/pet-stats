# pet-stats
This is the main repository of the pet-stats project. All of the source code will be stored here.
# Project Background
Our project focuses on the pet adoption dataset made available through the [petfinder API](https://www.petfinder.com/developers/v2/docs/), which supports both live data around pets currently available for adoption, and historical data regarding pet adoption outcomes. According to the Petfinder documentation, their adoption data originates from a network of “over ten thousand animal welfare organizations” covering the United States, Canada, and Mexico. 

A tool already exists that uses this API to provide individuals with the ability to view and adopt currently available pets. Our project, however, aims to achieve a different **goal: help our users understand large-scale trends on historic and current pet adoption in the United States and Canada.** 

Specifically, our goal is to provide information around how certain factors, such as geography, time, significant events (such as the COVID-19 pandemic), and pet-related data (such as breed or gender), affect adoption availability and outcomes. 

# Achieving Our Goal
This project will achieve our goal through the use of data visualization. Specifically, two visualization types will be used: 

- pie charts
- geographical heatmaps

Pie charts will be used to display data regarding the distribution of subsets — for example, availability of different breeds of dogs. Geographical heatmaps also the user to easily see trends over geography regions. Our project contains two geographic maps, one for the United States and one for Canada.

# Features Not Delivered
(1) Line Graph Visualization 

On Dec 7th (the day before the presentation), the Line graph visualization is done; however, the filter and api connections are far from complete. In addition, adjusting the line graph to a single line is still time consuming. Due to a lack of time and need to complete other work such as the writeup and presentation we voted on whether to cut this feature. As a group, we made the decision to cut Line Graph Visualization from scope.

(2) Examples/Premade 

Completing this feature would require work from the db, api, and frontend. In addition, not much code can be reused and result in a huge workload. The addition of this feature is not that impactful to achieving our goal. So we brought this up in a group meeting and voted to cut this feature from our scope.


(3) Mexico

After validing the amount of data PetFinderAPI has for each of the countries. We recognize that there was too little data from Mexico. Analysis done on Mexico would be limited and biased on data avaibility. So we voted and cut Maxico from our scope.



## Installation
**DO NOT** directly clone this repository. We have created Docker images containing the latest version of our code at Docker Hub. To download and run our web app, clone the [logistic](https://github.com/Team-ANANA/logistics) repository and follow the instruction in its README.

## Project Structure
The project consist of three main modules, frontend, backend(api), and database. Please reference the README.md for each module.

Frontend is located at [src/frontend/web](https://github.com/Team-ANANA/pet-stats/tree/main/src/frontend/web).

Backend is located at [src/api/environments](https://github.com/Team-ANANA/pet-stats/tree/main/src/api/environments).

Database is still under development.

The workflow folder contains Github Action scripts that deals with CI/CD.
