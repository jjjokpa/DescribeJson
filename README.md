## JsonToCsv

JsonToCsv is a script for creating Csv by Json.

<pre>
options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Insert Json file path.
  -l LIST, --list LIST  Insert List filed name in Json.
  -c COLS, --cols COLS  Insert Cols to select.
  -d HEADER, --header HEADER
                        Insert Headers to display.
  -o OUTPUT, --output OUTPUT
                        Insert Output file name.
</pre>

## Installation

<code>pip install -r requirements.txt</code>

## Usage

### ▼ sample.json

<pre>
{
    "accounting": [
        {
            "firstName": "John",
            "lastName": "Doe",
            "age": 23
        },
        {
            "firstName": "Mary",
            "lastName": "Smith",
            "age": 32
        }
    ],
    "sales": [
        {
            "firstName": "Sally",
            "lastName": "Green",
            "age": 27
        },
        {
            "firstName": "Jim",
            "lastName": "Galley",
            "age": 41
        }
    ]
}
</pre>

### 1. Create csv by json

<code>python jsonToCsv.py --file sample.json</code>

### ▼ Result

<pre>
accounting.firstName,accounting.lastName,accounting.age,sales.firstName,sales.lastName,sales.age
John,Doe,23,Sally,Green,27
John,Doe,23,Jim,Galley,41
Mary,Smith,32,Sally,Green,27
Mary,Smith,32,Jim,Galley,41
</pre>

### 2. Create csv by selected field

<code>python jsonToCsv.py --file sample.json --list accounting</code>

### ▼ Result

<pre>
firstName,lastName,age
John,Doe,23
Mary,Smith,32
</pre>

### 3. Output only selected columns

<code>python jsonToCsv.py --file sample.json --cols accounting.firstName,accounting.lastName</code>

### ▼ Result

<pre>
accounting.firstName,accounting.lastName
John,Doe
Mary,Smith
</pre>

### 4. Set headers

<code>python jsonToCsv.py --file sample.json --header a_firstName,a_lastName,a_age,s_firstName,s_lastName,s_age</code>

### ▼ Result

<pre>
a_firstName,a_lastName,a_age,s_firstName,s_lastName,s_age
John,Doe,23,Sally,Green,27
John,Doe,23,Jim,Galley,41
Mary,Smith,32,Sally,Green,27
Mary,Smith,32,Jim,Galley,41
</pre>

## License

[MIT](https://choosealicense.com/licenses/mit/)