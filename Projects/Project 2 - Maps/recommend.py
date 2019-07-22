"""A Yelp-powered Restaurant Recommendation Program"""

from abstractions import *
from data import ALL_RESTAURANTS, CATEGORIES, USER_FILES, load_user_file
from ucb import main, trace, interact
from utils import distance, mean, zip, enumerate, sample
from visualize import draw_map

##################################
# Phase 2: Unsupervised Learning #
##################################


def find_closest(location, centroids):
    """Return the centroid in centroids that is closest to location.
    If multiple centroids are equally close, return the first one.

    >>> find_closest([3.0, 4.0], [[0.0, 0.0], [2.0, 3.0], [4.0, 3.0], [5.0, 5.0]])
    [2.0, 3.0]
    """
    # BEGIN Question 3
    return min(centroids, key=lambda x: distance(location,x))
    # END Question 3


def group_by_first(pairs):
    """Return a list of pairs that relates each unique key in the [key, value]
    pairs to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_first(example)
    [[2, 3, 2], [2, 1], [4]]
    """
    keys = []
    for key, _ in pairs:
        if key not in keys:
            keys.append(key)
    return [[y for x, y in pairs if x == key] for key in keys]


def group_by_centroid(restaurants, centroids):
    #Note that the argument of this function takes a list of restaurants
    #(including name, location,reviews, etc), not just the location
    """Return a list of clusters, where each cluster contains all restaurants
    nearest to a corresponding centroid in centroids. Each item in
    restaurants should appear once in the result, along with the other
    restaurants closest to the same centroid.
    """
    # BEGIN Question 4
    # Centroid: A location that represents the center of a cluster
    # Cluster: A list of restaurants grouped around a centroid
    # find_closest: Returns the centroid in centroids that is closest to location

    #First we create a helper function that takes in a restaurant
    def helper(restaurant):
        # This function returns one centroid, but in the application, it'll
        # eventually return many centroids because we'll input multiple
        # restaurants
        return [find_closest(restaurant_location(restaurant), centroids)]
    lst = [[helper(restaurant), restaurant] for restaurant in restaurants]

    #This is what lst look like:
    # [[[[0, 0]], {'name': 'A', 'location': [-10, 2], 'categories': [], 'price': 2, 'reviews': [['A', 4]]}], 
    # [[[0, 0]], {'name': 'B', 'location': [-9, 1], 'categories': [], 'price': 3, 'reviews': [['B', 5], ['B', 3.5]]}], 
    # [[[3, 4]], {'name': 'C', 'location': [4, 2], 'categories': [], 'price': 1, 'reviews': [['C', 5]]}], 
    # [[[3, 4]], {'name': 'D', 'location': [-2, 6], 'categories': [], 'price': 4, 'reviews': [['D', 2]]}], 
    # [[[3, 4]], {'name': 'E', 'location': [4, 2], 'categories': [], 'price': 3.5, 'reviews': [['E', 2.5], ['E', 3]]}]]

    #This is what the return result look like:
    # [[{'name': 'A', 'location': [-10, 2], 'categories': [], 'price': 2, 'reviews': [['A', 4]]}, {'name': 'B', 'location': [-9, 1], 'categories': [], 'price': 3, 'reviews': [['B', 5], ['B', 3.5]]}], 
    # [{'name': 'C', 'location': [4, 2], 'categories': [], 'price': 1, 'reviews': [['C', 5]]}, {'name': 'D', 'location': [-2, 6], 'categories': [], 'price': 4, 'reviews': [['D', 2]]}, {'name': 'E', 'location': [4, 2], 'categories': [], 'price': 3.5, 'reviews': [['E', 2.5], ['E', 3]]}]]
    # Notice here that group_by_first groups the restaurants by 2 categories:
    # 1. Restaurants where the centroid is [0, 0]
    # 2. Restaurants where the centroid is [3, 4]

    return group_by_first(lst)
    # END Question 4


def find_centroid(cluster):
    """Return the centroid of the locations of the restaurants in cluster."""
    # BEGIN Question 5

    # The following is what a cluster looks like:
    # cluster1 = [make_restaurant('A', [-3, -4], [], 3, [make_review('A', 2)]), 
    # make_restaurant('B', [1, -1],  [], 1, [make_review('B', 1)]), 
    # make_restaurant('C', [2, -4],  [], 1, [make_review('C', 5)]),]

    #The centroid (the result that we're looking for) is the average (mean) of the x and y coordinates.
    #1. Grab JUST THE COORDINATES from the cluster of restaurants
    coordinates = [restaurant_location(restaurant) for restaurant in cluster]
    #coordinates = [[-3, -4], [1, -1], [2, -4]]

    #2.Grab all the x and y coordinates and keep them in a separate variable
    x_coordinates = [coordinate[0] for coordinate in coordinates]
    #x_coordinates = [-3, 1, 2]
    y_coordinates = [coordinate[1] for coordinate in coordinates]
    #y_coordinates = [-4, -1, -4]

    #3. Calculate the mean
    return [(mean(x_coordinates)), mean(y_coordinates)]

    # END Question 5


def k_means(restaurants, k, max_updates=100):
    """Use k-means to group restaurants by location into k clusters."""
    assert len(restaurants) >= k, 'Not enough restaurants to cluster'
    old_centroids, n = [], 0
    # Select initial centroids randomly by choosing k different restaurants
    centroids = [restaurant_location(r) for r in sample(restaurants, k)]

    #This is what the restaurants argument look like:
    # restaurants1 = [
    #  make_restaurant('A', [-3, -4], [], 3, [make_review('A', 2)]),
    #  make_restaurant('B', [1, -1],  [], 1, [make_review('B', 1)]),
    #  make_restaurant('C', [2, -4],  [], 1, [make_review('C', 5)]),
    # ]

    #This is what the centroids look like at first:
    [[-3, 4]]


    while old_centroids != centroids and n < max_updates:
        old_centroids = centroids
        # BEGIN Question 6
        # 1. Group restaurants into clusters. Each cluster contains all restaurants
        # closest to the same centroid.
        grouped_clusters = group_by_centroid(restaurants, centroids)

        # This is what grouped_clusters look like:
        # [[<Restaurant A>, <Restaurant B>, <Restaurant C>]]

        # 2. Update centroids based on the clusters.
        #NOTE: grouped_clusters is multiple clusters. When we use the find_centroid
        # function, use the function for each cluster, NOT the whole group
        centroids = [find_centroid(cluster) for cluster in grouped_clusters]

        # END Question 6
        n += 1
        # The cycle stops once the centroids don't change anymore
    return centroids


################################
# Phase 3: Supervised Learning #
################################


def find_predictor(user, restaurants, feature_fn):
    """Return a rating predictor (a function from restaurants to ratings),
    for a user by performing least-squares linear regression using feature_fn
    on the items in restaurants. Also, return the R^2 value of this model.

    Arguments:
    user -- A user
    restaurants -- A sequence of restaurants
    feature_fn -- A function that takes a restaurant and returns a number
    """
    reviews_by_user = {review_restaurant_name(review): review_rating(review)
                       for review in user_reviews(user).values()}

    #The list xs represents the extracted feature value for each restaurant in restaurants
    xs = [feature_fn(r) for r in restaurants] # xs is a list of numbers!
    #The list ys represent the average rating for the restaurants in restaurants
    ys = [reviews_by_user[restaurant_name(r)] for r in restaurants] # ys is also a list of numbers!

    # BEGIN Question 7
    Sxx = sum([(x - mean(xs))**2 for x in xs])
    Syy = sum([(y - mean(ys))**2 for y in ys])
    #For Sxy, notice that we need to sum a list where each element is (x-mean(xs)) * (y-mean(ys)).
    # for this, we need to zip xs and ys in one list, then we'll create a list comprehension
    # that uses that zipped list
    Sxy = sum([(x - mean(xs)) * (y - mean (ys)) for x, y in zip(xs, ys)])

    b = Sxy / Sxx
    a = mean(ys) - (b * mean(xs))
    r_squared = (Sxy**2) / (Sxx * Syy)
    # END Question 7

    def predictor(restaurant):
        return b * feature_fn(restaurant) + a

    return predictor, r_squared
    #This predictor function takes in a restaurant and returns the predicted rating for that restaurant


def best_predictor(user, restaurants, feature_fns):
    #Returns a predictor function and it's r_squared value
    """Find the feature within feature_fns that gives the highest R^2 value
    for predicting ratings by the user; return a predictor using that feature.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of functions that each takes a restaurant
    """
    #============= This is what user looks like: ===============
    # ['Cheapskate', {'A': ['A', 2], 'B': ['B', 5], 'C': ['C', 2], 'D': ['D', 5]}]

    # reviewed is a list of restaurants that have been reviewed by users
    reviewed = user_reviewed_restaurants(user, restaurants)
    #=============This is what looks reviewed look like: ================
    # [{'name': 'A', 'location': [5, 2], 'categories': [], 'price': 4, 'reviews': [['A', 5]]},
    # {'name': 'B', 'location': [3, 2], 'categories': [], 'price': 2, 'reviews': [['B', 5]]}, 
    # {'name': 'C', 'location': [-2, 6], 'categories': [], 'price': 4, 'reviews': [['C', 4]]}, 
    # {'name': 'D', 'location': [4, 2], 'categories': [], 'price': 2, 'reviews': [['D', 3], ['D', 4]]}]

    # BEGIN Question 8

    #============== This is what feature_fns look like: ===============
    # [<function restaurant_price at 0x0463A6F0>, <function <lambda> at 0x06D3C198>]
    # From above, we have 2 different feature_fn functions but we don't know which one gives greater R_squared
    # value.
    list_of_predictor_and_r_squared = [find_predictor(user, reviewed, function) for function in feature_fns] 

    #============== This is what 'list_of_predictor_and_r_squared' look like:==================
    # [(<function find_predictor.<locals>.predictor at 0x0715C300>, 1.0), 
    # (<function find_predictor.<locals>.predictor at 0x0715C3D8>, 0.037037037037037035)]

    #After computing a list of [predictor, r_squared] pairs, we select
    # the predictor with the highest r_squared value
    predictor_with_highest_r_squared = max(list_of_predictor_and_r_squared, key = lambda x: x[1])
    # With the key argument, the max function returns the result based on the 2nd element of the tuples, which are
    # between the number 1.0 or 0.037037037...

    #============== This is what 'predictor_with_highest_r_squared look like: ===================
    # (<function find_predictor.<locals>.predictor at 0x06D7D300>, 1.0)
    # All that's left is returning the predictor function, which is the first element of the 
    # tuple
    return predictor_with_highest_r_squared[0]
    # END Question 8


def rate_all(user, restaurants, feature_fns):
    """Return the predicted ratings of restaurants by user using the best
    predictor based on a function from feature_fns.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of feature functions
    """
    #This rate_all function is supposed to return a dictionary where:
    # The keys = Restaurant names
    # The values = numbers - a mix of user ratings and predicted ratings

    predictor = best_predictor(user, ALL_RESTAURANTS, feature_fns)
    # ============= This is what predictor look like: =============
    # <function find_predictor.<locals>.predictor at 0x06960420>
    # Recall that predictor is a function that takes in a restaurant and
    # returns a rating number.

    # Reviewed represents a list of restaurants reviewed by the user
    reviewed = user_reviewed_restaurants(user, restaurants)

    # BEGIN Question 9
    dict_result = {} #Initialize a dictionary that's going to be the result
    #Loop through each restaurant in RESTAURANTS, not just REVIEWED
    for restaurant in restaurants:
        #Case 1: If the restaurant is in reviewed, it means there's
        # already a rating and we don't need to predict it
        if restaurant in reviewed:
            dict_result[restaurant_name(restaurant)] = user_rating(user, restaurant_name(restaurant)) 
        #Case 2: If the restaurant is not in reviewed, it means the restaurant
        # hasn't been rated by the user. Here's where the rating predictor
        # comes in!
        else:
            dict_result[restaurant_name(restaurant)] = predictor(restaurant)
    return dict_result

    # END Question 9

def search(query, restaurants):
    """Return each restaurant in restaurants that has query as a category.

    Arguments:
    query -- A string
    restaurants -- A sequence of restaurants
    """

    """ A few hints:
    1. Given a restaurant, the restaurant_categories in abstraction.py returns
    categories in form of a list of strings
    2. A restaurant match a search query if the query string is one of
    the restaurant's categories
    3. This 'search' function should return a list of restaurants objects, NOT JUST
    THE RESTAURANT NAMES"""
    # BEGIN Question 10
    return [restaurant for restaurant in restaurants if query in restaurant_categories(restaurant)]
    # END Question 10


def feature_set():
    """Return a sequence of feature functions."""
    return [lambda r: mean(restaurant_ratings(r)),
            restaurant_price,
            lambda r: len(restaurant_ratings(r)),
            lambda r: restaurant_location(r)[0],
            lambda r: restaurant_location(r)[1]]


@main
def main(*args):
    import argparse
    parser = argparse.ArgumentParser(
        description='Run Recommendations',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-u', '--user', type=str, choices=USER_FILES,
                        default='test_user',
                        metavar='USER',
                        help='user file, e.g.\n' +
                        '{{{}}}'.format(','.join(sample(USER_FILES, 3))))
    parser.add_argument('-k', '--k', type=int, help='for k-means')
    parser.add_argument('-q', '--query', choices=CATEGORIES,
                        metavar='QUERY',
                        help='search for restaurants by category e.g.\n'
                        '{{{}}}'.format(','.join(sample(CATEGORIES, 3))))
    parser.add_argument('-p', '--predict', action='store_true',
                        help='predict ratings for all restaurants')
    parser.add_argument('-r', '--restaurants', action='store_true',
                        help='outputs a list of restaurant names')
    args = parser.parse_args()

    # Output a list of restaurant names
    if args.restaurants:
        print('Restaurant names:')
        for restaurant in sorted(ALL_RESTAURANTS, key=restaurant_name):
            print(repr(restaurant_name(restaurant)))
        exit(0)

    # Select restaurants using a category query
    if args.query:
        restaurants = search(args.query, ALL_RESTAURANTS)
    else:
        restaurants = ALL_RESTAURANTS

    # Load a user
    assert args.user, 'A --user is required to draw a map'
    user = load_user_file('{}.dat'.format(args.user))

    # Collect ratings
    if args.predict:
        ratings = rate_all(user, restaurants, feature_set())
    else:
        restaurants = user_reviewed_restaurants(user, restaurants)
        names = [restaurant_name(r) for r in restaurants]
        ratings = {name: user_rating(user, name) for name in names}

    # Draw the visualization
    if args.k:
        centroids = k_means(restaurants, min(args.k, len(restaurants)))
    else:
        centroids = [restaurant_location(r) for r in restaurants]
    draw_map(centroids, restaurants, ratings)