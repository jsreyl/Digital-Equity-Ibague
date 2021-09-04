# Zonas Vibra: Digital Equity through free internet access points in Ibagué, Colombia
https://github.com/jsreyl/Digital-Equity-Ibague
##### Data Science 4 All 2021
##### Cristian Amezquita, Guillermo Cangrejo, Gabriela Garcia, Ever Sanchez, Juan S. Rey, Carlos Ruiz.

## Introduction
Internet connection is a basic and essential service for the Colombian population since it generates economic development and improves access to information, education, entertainment and work opportunities. However internet services in the country are not distributed equitably, according to MinTIC 21.7 million people have internet access while 23.8 million do not have the resources to access or are in remote areas of the country.

In order to fight this inequity, Alcaldía de Ibagué implemented free internet wifi points across the city called Zonas Vibra. To assess the use of Zonas Vibra and help decision making in the implementation of future internet zones we developed this project as part of the DS4A Colombia program offered by Correlation One.

![Logo de la Alcaldía de Ibagué y DS4A](/assets/logos_ibague_ds4a.png)

## Getting Started
This repository contains the code necessary for deploying a web application containing four views displaying statistical visualizations and heatmap of Ibagué.

The web page can be interacted by clicking [here!](http://3.131.143.43:8050/) or scanning the QR code below:
![Webapp QR code](/assets/webapp_qr_code.png)

The webapp is divided into four views:
1. **Statistics:** Shows the location of each Zona Vibra as a blue dot displayed over the map of Ibagué. Along with the map, number of connections per month and usage statistics aggregated across all Zonas Vibra are displayed. Also, we can filter the data displayed by each Comuna or Zona Vibra and the map will zoom to locate the comuna or Zona Vibra selected.
![Statistics view](/assets/Statistics_view.png)
2. **Demographics:** In this view the user can explore the distribution of the demographic variables on the CNPV 2018 Colombian census across Ibagué, the user can select the variable to be visualized and the webapp will display the corresponding heatmap.
![Demographics view](/assets/Demographics_view.png)
3. **Projection:** In this view the user can choose a location of Ibagué by clicking on the map. Then through the webapp backend we display on the left the address of the selected location and the probability of connectivity and proximity based on the two predictive models implemented. On the right side a summary of the demographic variables of the location is displayed.
![Projection view](/assets/Projection_view.png)
4. **Potential:** This view displays the potential blocks across the city where a Zona Vibra is needed and how far it is from a Zona Vibra already working. The heatmap indicates the probability of a block to be far from a Zona Vibra given its demographic variables as indicated by the second predictive model implemented.
![Potential view](/assets/Potential_view.png)

## Installation
1. (Recommended) Create a python virtual environment for installing this project's dependencies
```
python3 -m venv ./dash-env
```
and activate it
```
source ./dash-env/bin/activate
```
your shell prompt now should look like
```
(dash-env) user@host $
```
2. Install the python dependencies
```
pip install -r requirements.txt
```
these will be installed to the environment directory **/dash-env/** so no need to worry about breaking your system :) .

## Running the code
After installation simply run 
```
python3 app.py
```
This should deploy a working version of the app in your browser. The scripts in the main folder work as follows:
 - _app.py_ : Uses the Dash library to handle frontend visualization and interaction. Currently deployed in AWS EC2. Each of the views is controlled by this script using either .csv files in /data/ (to run using local resources) or an external database. Logos and icons displayed as well as stilesheets are used from /assets/.
 - _connector.py_ : Connects the frontend part of the application to the external PostreSQL database (currently deployed in AWS RDS). The functions here make queries to the database and convert them into pandas DataFrames that are used for visualization in the frontend.

## Model
Model training and visualization is performed apart from the main web application as it would be too heavy to train the model real time to generate predictions. The model training scripts can be found in /model/ as follows:
- _Zonas Vibra Connection Model_: A jupyter notebook containing the preprocessing of the dataset and training of a logit model to **predict connectivity*** of a Zona Vibra given the demographic variables of the population around it.
- _No Proximity Model_: A jupyter notebook containing the preprocessing of the dataset and training of a logit model to **predict proximity** of a given location block in the city to a Zona Vibra, notice this proximity uses demographic variables as well to geographic position to prioritize vulnerable population.
- _Plotly Map Plot_: A jupyter notebook exemplifying the process to generate heatmap visualizations using plotly.
- _Zonas Vibra EDA_: A jupyter notebook with the processing and Exploratory Data Analysis of the Zonas Vibra dataset and the generation of further data via aggreagation of population close to the Zonas Vibra. Can be obtained [here!](https://drive.google.com/file/d/1duelzzgN-SiNuplDWkk9tEAnzbQq2BNm/view?usp=sharing) (Please beware as multiple map visualizations can take quite some space.)
