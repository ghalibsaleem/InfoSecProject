### Profiling Internet Users ###

#### Contributors ####

1) Ghalib Saleem 

The source of data for this project is Cisco NetFlow version 5, which is one of the most popular technologies to collect IP traffic. Many parameters can be extracted from the source data including; Packets, Octets, beginning and ending of each flow, source and destination port numbers, source and destination IP addresses and many other variables which are included in the following figure.
To preserve the privacy, all the IP addresses are removed from the data. 54 Excel files are included in the project which each file corresponds to one user. Data is captured for a month long period. In average, the number of flows for each subject over a week worth of data is more than 7000.

```
Requirement: Python 3.7.5 or later 
```

#### Assignment Code Structure ####

```
Assignment01             // Root Folder
├── datahandlers        
│   ├── data_export.py   
│   └── datamain.py      
├── helper              
│   ├── calc_functions.py   
│   ├── helper_operations.py  
│   ├── progress_bar.py   
│   └── spearman_correlation.py  
├── input              
│   └── *.xlsx  
├── models              
│   ├── split_data.py   
│   ├── split_item.py  
│   ├── user_data.py   
│   └── user_info.py 
├── output                
│   └── *.csv    
├── saved_obj                
│   └── *.obj 
│── main.py              // Main File
└──README.md             // Read Me file
```

#### Input ####

The project takes two types of input:

1) saved_obj/*.obj 
2) input/*.xlsx 
```
NOTE: The above mention input is required to run the script. It gives error if not provided. When the program is executed for very first time. It will read the excel files and save the object files. So in next execution it will read information from ibj files instead of excel files.   
```

#### How to run the script ####

1) cd <PATH_TO_DOWNLOAD_FOLDER>/Assignment01
2) python3 main.py
3) When the script runs, it print all the important steps done or working on it
   

#### Output ####

```
************* Start of the program **************
Start: Object reading from file system
Obj read Progress: |██████████████████████████████████████████████████| 100.0% Completed
End: Object reading from file system
Check: All 54 User is loaded properly 
-------------------------------------------------------------------------------------------------
Start: Splitting
Splitting Progress: |██████████████████████████████████████████████████| 100.0% Completed
End: Splitting
End of Create Split for time interval 10
Done processing for Interval : 10
Start: Splitting
Splitting Progress: |██████████████████████████████████████████████████| 100.0% Completed
End: Splitting
End of Create Split for time interval 227
Done processing for Interval : 227
Start: Splitting
Splitting Progress: |██████████████████████████████████████████████████| 100.0% Completed
End: Splitting
End of Create Split for time interval 300
Done processing for Interval : 300
************* End of the program **************
```
