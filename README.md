# Google Hashcode 2020 score calculator

requires `python>=3.6`

## Usage

`python score.py example/a_example.txt example/a_example.txt.out`

output:

```
score: 17
```

`python score.py example/a_example.txt example/a_example.txt.out --debug`

output:

```
DEBUG:root:day 2: library 0 signup is finished
DEBUG:root:day 2: 5 books sent: [3, 4, 2, 1, 0]
score: 17
```

## Errors

The score calculator should be robust against most errors.

Score might be inaccurate when output file is erroneous though.

### Invalid book id

```
python score.py example/a_example.txt example/a_example-invalid-book-id.out
```

```
WARNING:root:line 5: book id 6 is invalid should be >= 0 and < 6
WARNING:root:line 5: book id 7 is invalid should be >= 0 and < 6
WARNING:root:line 5: book id 9 is invalid should be >= 0 and < 6
score: 17
```

### Invalid library id

```
python score.py example/a_example.txt example/a_example-invalid-library-id.out
```

```
WARNING:root:line 4: library id 2 is invalid should be >= 0 and < 2
score: 17
```

### Library with 0 book sent

```
python score.py example/a_example.txt example/a_example-library-nothing-sent.out
```

```
WARNING:root:line 4: library books sent 0 == 0
WARNING:root:line 5: invalid content: '' should be <books>...
score: 16
```

### Discrepancies between books sent and declaration

```
python score.py example/a_example.txt example/a_example-wrong-number-of-books.out
```

```
WARNING:root:line 3: number of books (4) does not match declaration at line 2 (5)
```