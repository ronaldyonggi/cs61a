# Yelp Maps
![map](https://inst.eecs.berkeley.edu/~cs61a/sp18/proj/maps/visualize/voronoi.png)

## Introduction

A visualization of a [Voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram) of restaurant ratings around Berkeley, CA. Based on [University of California - Berkeley CS61A Spring 2018 course Project #2: Yelp Maps](https://inst.eecs.berkeley.edu/~cs61a/sp18/proj/maps/).

## Instruction on How to Use

On any of the following visualization, the rating is represented by a number in parentheses next to the restaurant name.

### Generate visualization of all restaurants rated by a user

Using a terminal or shell, run the following:
```
python3 recommend.py -u [user]
```

Where `user` is any of the `.dat` filename in the `/users` directory. For example, if you want to generate a visualization of all the restaurants rated by the user who `likes_everything` (there is the `likes_everything.dat` file in `/users` directory), run the following:

```
python3 recommend.py -u likes_everything
```

By default, ommitting the `-u` argument will default to user `test_user`.

### Generate visualization of restaurants that are close to each other

Using a terminal or shell, run the following:

```
python3 recommend.py -k [number of clusters]
```

Where `[number of clusters]` is the number of grouping desired. Dots that have the same color on the map belong to the same cluster of restaurants. For example, if you want to group restaurants by 2 groupings, run the following:

```
python3 recommend.py -k 2
```

### Generate visualization of restaurants rated by a user that are close to each other

The 2 previous steps can be combined:

```
python3 recommend.py -u [user] -k [number of clusters]
```

For example, if you want to group restaurants by 2 groups for the restaurants that are rated by `likes_expensive.dat`, run the following:

```
python3 recommend.py -u likes_expensive -k 3
```

### Generate visualization of restaurants both rated by a user and predicted what rating that user would give

Even if a user has not rated a restaurant before, you can see the prediction of what rating that user will rate a restaurant. Simply add the `-p` option.

For example, if you want to see the restaurants that are both rated and predicted for the user `likes_southside`, grouped into 5 clusters, run the following,

```
python3 recommend.py -u likes_southside -k 5 -p
```

### Generate visualization of restaurants, filtered by a query

The `-q` option allows you to filter based a category. For example, if you want to visualize all sandwich restaurants and their predicted ratings for the `likes_expensive` user, run the following:

```
python3 recommend.py -u likes_expensive -p -q Sandwiches
```

### Predict Your Own Ratings

In the `/users` directory, there are a couple of `.dat` files available. Copy one of them and rename the new file to `[any name].dat` (for example, `noob.dat`)

In the `.dat` files, you'll see something like the following,

```
make_user(
    'Positive Patty',      # name
    [                   # reviews
        # Northside restaurants
        make_review('Jasmine Thai', 4.0),
        make_review('Gomnaru Restaurant', 4.5),
        make_review('Top Dog 2', 5.0),
        ...
    ]
```

Replace second line with your name and replace the existing reviews on your own! You can get a list of Berkeley restaurants by running the following:

```
python3 recommend.py -r
```

Then use `recommend.py` to predict your ratings.

```
python3 recommend.py -u noob -k 2 -p -q Sandwiches
```

## Files and Directories

My implementations are as the following:
* `utils.py`: Utility functions for data processing
* `abstractions.py`: Data abstractions used in the project
* `recommend.py`: Machine learning algorithms and data processing
* `jupyter`: A directory containing Jupyter notebooks that explain my code in details

Supplemental files and directories that come with the project package:

* `ucb.py`: Utility functions for CS61A
* `data.py`: A directory of Yelp users, restaurants, and reviews
* `ok`: The autograder
* `proj2.ok`: The `ok` configuration file
* `tests`: A directory of tests used by `ok`
* `users`: A directory of user files
* `visualize`: A directory of tools for drawing the final visualization