# Just Table

Just table is a plugin for Pelican to create an easily table. Before this plugin, you can create tables like below way or maybe another way that I don't know :).
```
|   |   |   |   |   |
|---|---|---|---|---|
|   |   |   |   |   |
|   |   |   |   |   |
|   |   |   |   |   |
```
It looks easy, but sometimes you want to create a basic table quickly by the different way. Actually,  I hate above way. Now, time to the just table's way.
## Usage



*  Basic table



```
[jtable]
Year,Make,Model,Length
1994,Ford,E350,2.34
2000,Mercury,Cougar,2.38
[/jtable]
```



| Year |   Make  |  Model | Length |
|:----:|:-------:|:------:|:------:|
| 1994 |   Ford  |  E350  |  2.34  |
| 2000 | Mercury | Cougar |  2.38  |




*  More complicated


```
[jtable]
Year,Make,Model,Description,Price
1997,Ford,E350,ac,3000.00
1999,Chevy,Venture Extended Edition,,4900.00
1999,Chevy,Venture Extended Edition and Very Large,,5000.00
1996,Jeep,Grand Cherokee,MUST SELL!,4799.00
[/jtable]
```



| Year | Make  | Model                                       | Description   | Price   |
|------|-------|---------------------------------------------|---------------|---------|
| 1997 | Ford  | E350                                        | ac | 3000.00 |
| 1999 | Chevy | Venture Extended Edition                |               | 4900.00 |
| 1999 | Chevy | Venture Extended Edition and Very Large |               | 5000.00 |
| 1996 | Jeep  | Grand Cherokee                              | MUST SELL!    | 4799.00 |


*  Table with no heading



```
[jtable th="0"]
row1col1,row1col2,row1col3
row2col1,row2col2,row2col3
row3col1,row3col2,row3col3
[/jtable]
```



|  |  |  |
|----------|----------|----------|
| row1col1 | row1col2 | row1col3 |
| row2col1 | row2col2 | row2col3 |
| row3col1 | row3col2 | row3col3 |




*  Table with caption without heading



```
[jtable caption="This is caption" th="0"]
row1col1,row1col2,row1col3
row2col1,row2col2,row2col3
row3col1,row3col2,row3col3
[/jtable]
```


||This is caption ||
|----------|----------|----------|
| row1col1 | row1col2 | row1col3 |
| row2col1 | row2col2 | row2col3 |
| row3col1 | row3col2 | row3col3 |


or if you want to head and caption both, you can delete ```th="0"```


*  Table with auto index and It'll start from 1



```
[jtable ai="1"]
head1,head2,head3
row1col1,row1col2,row1col3
row2col1,row2col2,row2col3
row3col1,row3col2,row3col3
row4col1,row4col2,row4col3 
[/jtable]
```


| No. |   head1  |  head2 | head3 |
|:----:|:-------:|:------:|:------:|
| 1 |   row1col1  |  row1col2  |  row1col3  |
| 2 | row2col1 | row2col2 |  row2col3  |
| 3 | row3col1 | row3col2 |  row3col3  |
| 4 | row4col1 | row4col2 |  row4col3  |


*  Custom separator for specific table


```
[jtable separator="|"]
head1|head2|head3
row1col1|row1col2|row1col3
row2col1|row2col2|row2col3
row3col1|row3col2|row3col3
row4col1|row4col2|row4col3
[/jtable]
```


### Installation

- When using pip: `pip install pelican-just-table`
- When using poetry: `poetry add pelican-just-table`
- When using pipenv: `pipenv install pelican-just-table`

Now add the plugin the Pelican ª`PLUGINS` setting

```PLUGINS = [... , 'pelican_just_table' , ... ]```


### Configuration

**Custom template**

You can customize table look by specifying `JTABLE_TEMPLATE` in your
`pelicanconf.py`. For example to match your bootstrap theme:

````
JTABLE_TEMPLATE = """
<table class="table table-hover">
    {% if caption %}
    <caption> {{ caption }} </caption>
    {% endif %}
    {% if th != 0 %}
    <thead>
    <tr>
        {% if ai == 1 %}
        <th> No. </th>
        {% endif %}
        {% for head in heads %}
        <th>{{ head }}</th>
        {% endfor %}
    </tr>
    </thead>
    {% endif %}
    <tbody>
        {% for body in bodies %}
        <tr>
            {% if ai == 1 %}
            <td> {{ loop.index }} </td>
            {% endif %}
            {% for entry in body %}
            <td>{{ entry }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </tbody>
</table>
"""
````

**Custom separator**

Custom separator for all tables also can be specified:

````
JTABLE_SEPARATOR = '|'
````


### Todo's

 - Read from CSV
 


### License
GPL
