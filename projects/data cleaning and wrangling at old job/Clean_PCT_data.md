# Objectives

Clean `PCT.xlsx` data and then split into two data tables:
        
- PCT with IPC (one PCT might have multiple IPC codes, each PCT-IPC pair should be displayed as one record)
- PCT (distinct PCTs with `title`, `applicant`, `desginated to CN`, `Filing date` and `link`)

# Import PCT Data


```python
import numpy as np
import pandas as pd
pct = pd.read_excel("./Data/To clean in Jupyter/PCT.xlsx", engine='openpyxl')
pct.head(2)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PCT</th>
      <th>Title</th>
      <th>Applicant</th>
      <th>Designated to CN</th>
      <th>IPC</th>
      <th>Filing Date</th>
      <th>Link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>WO2017075268</td>
      <td>TROPONIN I AND SOLUBLE UROKINASE RECEPTOR DETE...</td>
      <td>ABBOTT LABORATORIES</td>
      <td>1</td>
      <td>G01N 33/68 (2006.01)</td>
      <td>27.10.2016</td>
      <td>https://patentscope.wipo.int/search/en/detail....</td>
    </tr>
    <tr>
      <th>1</th>
      <td>WO2008080030</td>
      <td>CARDIOVASCULAR AUTOIMMUNE DISEASE PANEL AND ME...</td>
      <td>ABBOTT LABORATORIES</td>
      <td>1</td>
      <td>G01N 33/53 (2006.01) ,G01N 33/49 (2006.01)</td>
      <td>21.12.2007</td>
      <td>https://patentscope.wipo.int/search/en/detail....</td>
    </tr>
  </tbody>
</table>
</div>



# Clean Data


```python
# check dataset
print(pct.info())
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 473 entries, 0 to 472
    Data columns (total 7 columns):
     #   Column            Non-Null Count  Dtype 
    ---  ------            --------------  ----- 
     0   PCT               473 non-null    object
     1   Title             473 non-null    object
     2   Applicant         473 non-null    object
     3   Designated to CN  473 non-null    int64 
     4   IPC               473 non-null    object
     5   Filing Date       473 non-null    object
     6   Link              473 non-null    object
    dtypes: int64(1), object(6)
    memory usage: 26.0+ KB
    None



```python
# check if any duplicate PCT due to multiple IPC
(pct.PCT.value_counts() > 1).sum()
```




    1




```python
# remove pct without ipc code
pct = pct[pct["IPC"].notnull()]

# remove tab character
pct["PCT"]=[st.replace('\t','') for st in pct["PCT"]]
```

# Convert Dates


```python
# check if filing date is datetime object
type(pct["Filing Date"][0])
```




    str




```python
# convert str to date
pct["Filing Date"] = pd.to_datetime(pct["Filing Date"], format="%d.%m.%Y")
pct["Filing Date"].head()
```




    0   2016-10-27
    1   2007-12-21
    2   2007-12-21
    3   1997-03-21
    4   1994-03-18
    Name: Filing Date, dtype: datetime64[ns]



# Split IPC Data


```python
# split IPC codes
# insert the splitted codes into multiple rows (with multiple leveled index - use PCT code as index)
IPC_data = pd.DataFrame(pct.IPC.str.split(',').tolist(), index=pct.PCT).stack()
IPC_data.head()
```




    PCT            
    WO2017075268  0     G01N 33/68 (2006.01)
    WO2008080030  0    G01N 33/53 (2006.01) 
                  1     G01N 33/49 (2006.01)
    WO1997036902  0    G01N 33/53 (2006.01) 
                  1     G01N 33/49 (2006.01)
    dtype: object




```python
len(IPC_data)
```




    1176




```python
#reset_index of the new df, so that PCT code become a column and no duplicated value later
IPC_data = IPC_data.reset_index()
IPC_data = IPC_data[["PCT",0]]
IPC_data.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PCT</th>
      <th>0</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>WO2017075268</td>
      <td>G01N 33/68 (2006.01)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>WO2008080030</td>
      <td>G01N 33/53 (2006.01)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>WO2008080030</td>
      <td>G01N 33/49 (2006.01)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>WO1997036902</td>
      <td>G01N 33/53 (2006.01)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>WO1997036902</td>
      <td>G01N 33/49 (2006.01)</td>
    </tr>
  </tbody>
</table>
</div>




```python
# rename the columns
IPC_data.columns = ["PCT", "IPC"]
IPC_data.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PCT</th>
      <th>IPC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>WO2017075268</td>
      <td>G01N 33/68 (2006.01)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>WO2008080030</td>
      <td>G01N 33/53 (2006.01)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>WO2008080030</td>
      <td>G01N 33/49 (2006.01)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>WO1997036902</td>
      <td>G01N 33/53 (2006.01)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>WO1997036902</td>
      <td>G01N 33/49 (2006.01)</td>
    </tr>
  </tbody>
</table>
</div>




```python
# add IPC subClass
IPC_data["IPC SubClass"] = pd.Series([st[:4] for st in IPC_data["IPC"]])
IPC_data.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PCT</th>
      <th>IPC</th>
      <th>IPC SubClass</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>WO2017075268</td>
      <td>G01N 33/68 (2006.01)</td>
      <td>G01N</td>
    </tr>
    <tr>
      <th>1</th>
      <td>WO2008080030</td>
      <td>G01N 33/53 (2006.01)</td>
      <td>G01N</td>
    </tr>
    <tr>
      <th>2</th>
      <td>WO2008080030</td>
      <td>G01N 33/49 (2006.01)</td>
      <td>G01N</td>
    </tr>
    <tr>
      <th>3</th>
      <td>WO1997036902</td>
      <td>G01N 33/53 (2006.01)</td>
      <td>G01N</td>
    </tr>
    <tr>
      <th>4</th>
      <td>WO1997036902</td>
      <td>G01N 33/49 (2006.01)</td>
      <td>G01N</td>
    </tr>
  </tbody>
</table>
</div>




```python
IPC_data["IPC SubClass"].unique()
```




    array(['G01N', 'C07D', 'A61K', 'C07C', 'C07K', 'A61M', 'G06F', 'A61P',
           'A23L', 'C08G', 'A61F', 'B29C', 'A61B', 'A61L', 'C22C', 'C22F',
           'C08J', 'G06T', 'G09B', 'B23K', 'C08L', 'F26B', 'B05D', 'B05B',
           'B05C', 'C08H', 'A61N', 'C08F', 'C09D', 'B65B', 'B01J', 'C08K',
           'G01G', 'C25F', 'B24C', 'B26F', 'C23C', 'B21D', 'C21D', 'B29B',
           'B29L'], dtype=object)




```python
# export PCT-IPC data
IPC_data.to_csv("./Data/Ready for Excel/PCT_IPC.csv")
```

# Export Clean PCT Data


```python
columns = ["PCT", "Title", "Applicant", "Designated to CN", "Filing Date", "Link"]
new_pct = pct[columns]
new_pct.head(2)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PCT</th>
      <th>Title</th>
      <th>Applicant</th>
      <th>Designated to CN</th>
      <th>Filing Date</th>
      <th>Link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>WO2017075268</td>
      <td>TROPONIN I AND SOLUBLE UROKINASE RECEPTOR DETE...</td>
      <td>ABBOTT LABORATORIES</td>
      <td>1</td>
      <td>2016-10-27</td>
      <td>https://patentscope.wipo.int/search/en/detail....</td>
    </tr>
    <tr>
      <th>1</th>
      <td>WO2008080030</td>
      <td>CARDIOVASCULAR AUTOIMMUNE DISEASE PANEL AND ME...</td>
      <td>ABBOTT LABORATORIES</td>
      <td>1</td>
      <td>2007-12-21</td>
      <td>https://patentscope.wipo.int/search/en/detail....</td>
    </tr>
  </tbody>
</table>
</div>




```python
new_pct.to_csv("./Data/Ready for Excel/clean_PCT.csv")
```
