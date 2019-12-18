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
    
    # With the restaurant_location selector, obtain each restaurant's location and put in a list
    restaurant_locations = [restaurant_location(restaurant) for restaurant in restaurants]
    # Calculate the closest centroid for each restaurant location
    closest_centroid = [find_closest(location, centroids) for location in restaurant_locations]
    # Zip each restaurant with its closest centroid
    zipped_pair = zip(closest_centroid, restaurants)
    # Then group the zipped_pair using group_by_first
    return group_by_first(zipped_pair)

    # END Question 4


def find_centroid(cluster):
    """Return the centroid of the locations of the restaurants in cluster."""
    # BEGIN Question 5
    # Obtain the location of each restaurant using the restaurant_location selector
    locations = [restaurant_location(restaurant) for restaurant in cluster]
    # Obtain the latitudes from locations, indicated by index 0 of each location
    latitudes = [location[0] for location in locations]
    # Obtain the longitude, indicated by index 1 of each location
    longitudes = [location[1] for location in locations]
    # Simply calculate the mean of latitudes and longitudes separately then return them in a form of list
    return [mean(latitudes), mean(longitudes)]
    # END Question 5


def k_means(restaurants, k, max_updates=100):
    """Use k-means to group restaurants by location into k clusters."""
    assert len(restaurants) >= k, 'Not enough restaurants to cluster'
    old_centroids, n = [], 0
    # Select initial centroids randomly by choosing k different restaurants
    centroids = [restaurant_location(r) for r in sample(restaurants, k)]

    while old_centroids != centroids and n < max_updates:
        old_centroids = centroids
        # BEGIN Question 6
        # Group restaurants into clusters. Each cluster consists of all restaurants closest to the same centroid
        clusters = group_by_centroid(restaurants, centroids)
        # find the centroid of each cluster in clusters, and bind it to the variable 'centroids'
        centroids = [find_centroid(cluster) for cluster in clusters]
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

    xs = [feature_fn(r) for r in restaurants]
    ys = [reviews_by_user[restaurant_name(r)] for r in restaurants]

    # BEGIN Question 7
    # Simply calculate the components of linear regression
    Sxx = sum([(xi - mean(xs))**2 for xi in xs])
    Syy = sum([(yi - mean(ys))**2 for yi in ys])
    Sxy = sum([(xi - mean(xs)) * (yi - mean(ys)) for xi, yi in zip(xs, ys)])

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
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 8
    # Find the predictor for each feature function
    predictors_and_rsquared = [find_predictor(user, reviewed, feature_fn) for feature_fn in feature_fns]
    # Among the various predictors, choose the one with highest r_squared value
    return max(predictors_and_rsquared, key = lambda x: x[1])[0]
    # END Question 8


def rate_all(user, restaurants, feature_fns):
    """Return the predicted ratings of restaurants by user using the best
    predictor based on a function from feature_fns.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of feature functions
    """

    predictor = best_predictor(user, ALL_RESTAURANTS, feature_fns)
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 9

    result = {}
    for r in restaurants:
        if r in reviewed: # If the restaurant is in 'reviewed'
            # Use the 'user_rating' function to get the rating
            result[restaurant_name(r)] = user_rating(user, restaurant_name(r))
        else:
            # Otherwise, use the predictor function
            result[restaurant_name(r)] = predictor(r)

    return result

    # END Question 9

def search(query, restaurants):
    """Return each restaurant in restaurants that has query as a category.

    Arguments:
    query -- A string
    restaurants -- A sequence of restaurants
    """
    # BEGIN Question 10
    return [r for r in restaurants if query in restaurant_categories(r)]
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