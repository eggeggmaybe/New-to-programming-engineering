# New-to-programming-engineering

The project is to let one experience in software engineering, Python programming and processing data from different sources. It's a very good practice for a beginner coder.
The goal of this project is to generate a html file, a JSON file and a csv file of a company.An simple data analysis (detail is showed below) will be also conducted. 

"HTML Generation.zip":
In this zip file, "html_generator.py" is used to generate the html which contains products and prices. "Product Photos" folder includes the photos used in the html. Moreover, "product_details.csv" is just product details.
A sample html file "index.html" is also uploaded but one can get the same file using the code in this zip file.

"JSON_CSV_generator.py":
This is used to generate a JSON file that contains information about customer interactions with the web site (clicks, hover time, viewing time, customer ID)
This will also generate a csv file that works as a SQL database of stock, customer purchases and shipping expenses.
A sample csv file "Purchase.csv" is also uploaded but one can get the same file using the code.

"eventsperday_test.py", "multiplylist_test.py", and "usermaker_test.py":
These are used for unittest some functions in "JSON_CSV_generator.py".

"analysis.py":
There are 14 things will be analysed using this code and they are printed one line per item, with spaces separating values. 
1. the highest priced product, giving the product id and the price; 
2. the mean number of words in the 32 info spans; 
3. the product that has the most hover time, giving the product id and the total number of seconds; 
4. the product that has the most read time, giving the product id and the total number of seconds; 
5. the product that has the most sales, giving the product id and the number of units sold; 
6. the product with the highest total shipping cost, giving the product id and the total cost; 
7. the product with the highest profit (price times quantity less shipping), giving the product and profit; 
8. the product with the lowest profit, giving the product and profit; 
9. the product with the lowest hover-to-profit ratio, giving the product and ratio; 
10. the product with the highest hover-to-profit ratio, giving the product and ratio; 
11. the product with the highest read-to-profit ratio, giving the product and ratio; and 
12. the product with the lowest read-to-profit ratio, giving the product and ratio. 
13. the product with the highest info-to-profit ratio, giving the product and ratio. 
14. the product with the lowest info-to-profit ratio, giving the product and ratio. Your analysis should allow for reads without hovers. 
The hover and read-to-profit ratio is defined as the total time for hover/read of a product divided by the total profit (quantity sold times price less the total shipping cost). The info-to-profit ratio is defined as the total number of words in the info span for the product product divided by the total profit (quantity sold times price less the total shipping cost). A word is any contiguous sequence as defined by the default functioning of python split 0. If there are two or more products with the highest profit/shipping cost/etc, return results for the product with the lowest ID number from amongst the ties. 
