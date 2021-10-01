import enum
from pandas.io.pytables import DuplicateWarning
from py2neo import Node, Relationship, Graph, NodeMatcher
import pandas as pd
from operator import itemgetter
from typing import List, Dict
import random

graph = Graph("http://localhost:7474", username="neo4j", password='nusiss')

main_ingr = set(['apple', 'banana', 'bell pepper', 'broccoli', 'cabbage', 'carrot', 'cheese', 'coconut', 'cucumber', 'egg', 'fish', 'grapes', 'lemon', 'mango', 'milk', 'mushroom', 'oranges', 'peach', 'pear', 'pineapple', 'potatoes', 'pumpkin', 'seafood', 'shrimp', 'strawberry', 'tomatoes', 'watermelon', 'winter melon', 'garlic', 'corn', 'eggplant', 'lettuce', 'onion', 'scallion', 'chicken', 'beef', 'lamb', 'pork', 'sauce', 'duck', 'meatball', 'wine', 'berries', 'crabmeat', 'kiwi', 'bitter melon', 'pepper', 'peas', 'ginger', 'shells', 'chili', 'ham', 'sausage', 'butter', 'bread', 'rice', 'vanilla'])
random_set = {}


def getRecipes(
    ingr: List[str], 
    topk: int = 10, 
    dietary: str = None, 
    cuisine: str = None) -> List[Dict]:

    n = len(ingr)
    if (n == 0): return [{}]

    ingr_type = {}
    for it in ingr:
        it = it.lower()
        if it in main_ingr:
            ingr_type[it] = (it.upper(), 'Has_Main_Ingredient', 'main_ingredient')
            print(it, ' is main ingredient')
        else:
            ingr_type[it] = (it.lower(), 'Has_Ingredient', 'ingredient')

    cand = {name: 0 for name in ingr}
    query_indegree = "WITH "
    for i in range(n):
        query_indegree += "size((:recipe)-[:{2}]->(:{3}{{Name:'{0}'}})) as a{1},".format(ingr_type[ingr[i]][0], str(i), ingr_type[ingr[i]][1], ingr_type[ingr[i]][2])
    query_indegree = query_indegree[:-1] + " RETURN "
    for i in range(n):
        query_indegree += "a{0},".format(str(i))
    query_indegree = query_indegree[:-1]
    res = graph.run(query_indegree)
    indegrees = pd.DataFrame(res)
    for i, name in enumerate(ingr):
        cand[name] = indegrees.iloc[[0],[i]].values[0][0]
    sorted_ingr = sorted(cand, key=lambda x : x[1])
    
    query = ''
    for i in range(n):
        query += "OPTIONAL MATCH ((rep:recipe)-[r{0}:{3}]->(i{1}:{4}{{Name: '{2}'}})) ".format(str(i), str(i), ingr_type[sorted_ingr[i]][0], ingr_type[sorted_ingr[i]][1], ingr_type[sorted_ingr[i]][2])
    if dietary is not None:
        query += "MATCH (rep)-[rs:Has_Meal_Type]->(:meal_type{{Name: '{0}'}}) WHERE (rep)-[:Has_Meal_Type]->(:meal_type{{Name: '{1}'}})".format(dietary, dietary)
    query += "WITH rep, "
    for i in range(n):
        query += "r{0}, i{1}, ".format(str(i), str(i))
    query += "(size((rep:recipe)-[:Has_Ingredient]->(:ingredient)) + size((rep:recipe)-[:Has_Main_Ingredient]->(:main_ingredient))) as degree, "
    for i in range(n):
        query += "size((rep:recipe)-[:{2}]->(:{3}{{Name: '{0}'}})) as minus_degree{1},".format(ingr_type[sorted_ingr[i]][0], str(i), ingr_type[sorted_ingr[i]][1], ingr_type[sorted_ingr[i]][2])
    query = query[:-1] + ' '
    query += "RETURN rep, "
    for i in range(n):
        query += "r{0}, i{1}, minus_degree{2},".format(str(i), str(i), str(i))
    query += "degree ORDER BY degree"
    for i in range(n):
        query += "-minus_degree{0} * 2".format(str(i))
    query += ","
    for i in range(n):
        query += "(case when minus_degree{0}>=1 then 1 else 0 end)+".format(str(i))
    query = query[:-1] + " desc"
    query += ",degree LIMIT 25;"

    print(query)
    res = graph.run(query)
    res = pd.DataFrame(res)
    # print(res)

    recipes = []
    for i in range(min(topk, res.shape[0])):
        recipes.append(res.iloc[i,0])

    return recipes

########################################
# Unit Test 1
########################################

# res = getRecipes(['apple','banana', 'strawberry'], dietary='vegan')
# print(type(res[0]))

# Sample query

# query = 
# '''
# OPTIONAL MATCH ((rep:recipe)-[r0:Has_Main_Ingredient]->(i0:main_ingredient{Name: 'BANANA'})) 
# OPTIONAL MATCH ((rep:recipe)-[r1:Has_Main_Ingredient]->(i1:main_ingredient{Name: 'APPLE'})) 
# OPTIONAL MATCH ((rep:recipe)-[r2:Has_Main_Ingredient]->(i2:main_ingredient{Name: 'STRAWBERRY'})) 
# MATCH (rep)-[rs:Has_Meal_Type]->(:meal_type{Name: 'vegan'})
# WHERE (rep)-[:Has_Meal_Type]->(:meal_type{Name: 'vegan'})
# WITH rep, r0, i0, r1, i1, r2, i2, rs,
# (size((rep:recipe)-[:Has_Ingredient]->(:ingredient)) + size((rep:recipe)-[:Has_Main_Ingredient]->(:main_ingredient))) as degree, size((rep:recipe)-[:Has_Main_Ingredient]->(:main_ingredient{Name: 'BANANA'})) as minus_degree0,
# size((rep:recipe)-[:Has_Main_Ingredient]->(:main_ingredient{Name: 'APPLE'})) as minus_degree1,
# size((rep:recipe)-[:Has_Main_Ingredient]->(:main_ingredient{Name: 'STRAWBERRY'})) as minus_degree2
# RETURN rep, r0, i0, minus_degree0,r1, i1, rs, minus_degree1,r2, i2, minus_degree2,degree 
# ORDER BY degree-minus_degree0 * 2-minus_degree1 * 2-minus_degree2 * 2,
# (case when minus_degree0>=1 then 1 else 0 end)+(case when minus_degree1>=1 then 1 else 0 end)+(case when minus_degree2>=1 then 1 else 0 end) desc,degree LIMIT 25;
# '''

def getRecipeByName(rep: str) -> Dict:
    query = "MATCH (rep:recipe) WHERE rep.Name=~'(?i){0}' RETURN rep".format(rep)
    res = graph.run(query)
    res = pd.DataFrame(res)
    if res.empty:
        return None
    return res.iloc[0,0]

########################################
# Unit Test 2
########################################

# rep = 'super Fruity Smoothie'
# print(getRecipeByName(rep))

# Sample query
# MATCH (rep:recipe) 
# WHERE rep.Name=~'(?i)super Fruity Smoothie'
# RETURN rep


def getIngredient(id: str, rep: str) -> List[str]:
    query = "MATCH (rep:recipe)-[:Has_Ingredient]->(a:ingredient) WHERE rep.Name=~'(?i){0}' AND rep.RecipeId='{1}' RETURN a".format(rep, id)
    res = graph.run(query)
    res = pd.DataFrame(res)
    ingrs = []
    for i in range(res.shape[0]):
        ingrs.append(res.iloc[i,0]['Name'])
    return ingrs


########################################
# Unit Test 3
########################################

# rep = 'super Fruity Smoothie'
# print(getIngredient(rep))

# Sample query
# MATCH (rep:recipe)-[:Has_Ingredient]->(a:ingredient)
# WHERE rep.Name=~'(?i)super Fruity Smoothie'
# RETURN a


def random_init(length = 50):
    query = "MATCH (n:recipe) RETURN n LIMIT {0}".format(str(length))
    res = graph.run(query)
    res = pd.DataFrame(res)
    for i in range(res.shape[0]):
        random_set[i] = res.iloc[i,0]

def browser(topk: int = 10, dietary: str = None, cuisine: str = None) -> List[Dict]:
    if (len(random_set) == 0):
        random_init()
    keys = random.sample(range(1,len(random_set)), topk)
    res = itemgetter(*keys)(random_set)
    return res


########################################
# Unit Test 3
########################################

# print(browser())


    
    
