# JsonToCsv

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

Create Csv by Json

<code>python jsonToCsv.py --file sample.json</code>

Create Csv by List field

<code>python jsonToCsv.py --file sample.json --list accounting</code>

Select Columns

<code>python jsonToCsv.py --file sample.json --cols accounting.firstName,accounting.lastName</code>

Set Csv Header

<code>python jsonToCsv.py --file sample.json --header a_firstName,a_lastName,a_age,s_firstName,s_lastName,s_age</code>

## License

[MIT](https://choosealicense.com/licenses/mit/)