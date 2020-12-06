# cf-crawler
Python script to crawl submissions on [Codeforces](https://codeforces.com/)


## Installation

Python 3+ is required.

Clone this repository:

```
git clone https://github.com/ksk642/cf-crawler.git
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies:

```
pip install -r requirements.txt
```

## Usage

`crawler.py` currently can only crawl public view-able submissions. That means submissions for some problems from gym, groups, or ICPC minor contests are excluded.

Run `crawler.py` with Python interpreter:

```
python crawler.py <handle1> <handle2> <etc.>
```

To get only `Accepted` submissions:

```
python crawler.py -ac <handle1> <handle2> <etc.>
```

In the end, submissions of different handles will be separated in different folders accordingly.