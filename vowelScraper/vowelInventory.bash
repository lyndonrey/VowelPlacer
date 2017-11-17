#! /bin/bash

if [ "$1" == "true" ] 
then 
	python praatVowelScraper.py "$2" "scrapeOut.csv"
	java vowelFilter "scrapeOut.csv" "FAE-G01-OUT_3-75-50.csv" $3 $4 $5
#	python clusterAnalysis.py "filterOut.csv" $6 "$7"
fi

if [ "$1" == "false" ] 
then
	java vowelFilter "$2" "filterOut.csv" $3 $4 $5
	python clusterAnalysis.py "filterOut.csv" $6 "$7" "$8"
fi


# Scrape vowels from data
