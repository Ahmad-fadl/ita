# Classifier Evaluation
  * For the final evaluation we need a file containing some information and numbers regarding Covid-19. Therefore go to [github](https://github.com/owid/covid-19-data/tree/master/public/data) and click "Download our complete COVID-19 dataset" as csv. Save the file in `src/data/Classifier_Evaluation/owid-covid-data.csv`.
  * The authors describe the data as follows: "Our complete COVID-19 dataset is a collection of the COVID-19 data maintained by Our World in Data. It is updated daily and includes data on confirmed cases, deaths, hospitalizations, and testing, as well as other variables of potential interest."
  * The data is generated by running ``src/Classifier_Evaluation.py`` (see main read me for instructions)
-----------
## Visualisations
* Our visualizations of the sentiments can be found [here](https://github.com/Ahmad-fadl/ita/issues/2#issue-815278548) as a zip file AND here in ```Classifier/Evaluation/Plots/```
-----------
## Tip
* to speed up runtime and if not needed comment out the "# Test multiple classifiers"- part in ``src/Classifier_Evaluation.py``. Then it will only generate and save the visualisations, but not compute the f1-measure for the different classifiers.
