## Introduction
pet-stats is a web application to display analysis of animal welfare and adoption statistics.

This is the main repository of the pet-stats project. All of the source code will be stored here.

# Project Background
Our project focuses on the pet adoption dataset made available through the [petfinder API](https://www.petfinder.com/developers/v2/docs/), which supports both live data around pets currently available for adoption, and historical data regarding pet adoption outcomes. According to the Petfinder documentation, their adoption data originates from a network of “over ten thousand animal welfare organizations” covering the United States, Canada, and Mexico. 

A tool already exists that uses this API to provide individuals with the ability to view and adopt currently available pets. Our project, however, aims to achieve a different **goal: help our users understand large-scale trends on historic and current pet adoption in the United States and Canada.** 

Specifically, our goal is to provide information around how certain factors, such as geography, time, significant events (such as the COVID-19 pandemic), and pet-related data (such as breed or gender), affect adoption availability and outcomes. 

## Installation
**DO NOT** directly clone this repository for the purposes of running the final product. We have created Docker images containing the latest version of our code at Docker Hub. To download and run our web app, clone the [logistic](https://github.com/Team-ANANA/logistics) repository and follow the instruction in its README.

## Project Structure
The project consist of three main modules, frontend, backend(api), and database. Please reference the README.md for each module.

Frontend is located at [src/frontend/web](https://github.com/Team-ANANA/pet-stats/tree/main/src/frontend/web).

Backend is located at [src/api/environments](https://github.com/Team-ANANA/pet-stats/tree/main/src/api/environments).

Database is located at [src/DB-api/environments](https://github.com/Team-ANANA/pet-stats/blob/master/src/DB-api/environments/) 

The workflow folder contains Github Action scripts that deals with CI/CD.
