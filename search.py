import os, sys

from collections import defaultdict
from collections import OrderedDict

from ranking import ranking
from helper import search_term_posting_in_index

cache = defaultdict(lambda : False)

# get terms - postings from inverted index list according to query terms
def get_query_postings(config,total_query_terms,term_line_relationship):
	global cache

	unique_query_terms = list(OrderedDict.fromkeys(total_query_terms))

	query_postings = defaultdict(lambda : False)

	for term in unique_query_terms:
		# term not exist in cache
		# if cache[term] == False:
		resource_term_posting = search_term_posting_in_index(config,term,term_line_relationship)
		if resource_term_posting is not None:
			query_postings[term] = resource_term_posting[term]
		# term exists in cache
		# else:
		# 	query_postings[term] = cache[term][0]

	return query_postings


# main search function: currently still use boolean retrieval AND
# return the query result as a dictionary of doc_id and its score
def search(config, total_query_terms, doc_ids,term_line_relationship, prev_cache, strong_index):
	global cache

	cache = prev_cache

	if len(total_query_terms) == 0:
		return None

	query_postings = get_query_postings(config,total_query_terms,term_line_relationship)

	if query_postings is None:
		return None

	query_result = ranking(config, doc_ids,total_query_terms, strong_index,query_postings)

	if query_result is None:
		query_result = []

	if len(query_result) > config.max_num_urls_per_query:
			query_result = query_result[:config.max_num_urls_per_query]

	return query_result