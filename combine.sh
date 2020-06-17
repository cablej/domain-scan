curl https://raw.githubusercontent.com/GSA/data/master/dotgov-domains/current-federal.csv -s > current_federal.csv
csvsort current_federal.csv > current_federal_sorted.csv
mv current_federal_sorted.csv current_federal.csv
csvsort results/securitytxt.csv > securitytxt.csv
paste -d, securitytxt.csv current_federal.csv | csvjson > all_combined.json
rm securitytxt.csv current_federal.csv
