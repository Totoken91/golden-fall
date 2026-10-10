class_name WebArchive
extends RefCounted

# Offline 2003 web: a handful of authored pages, matched by whole words and keyword prefixes.
var state: GoldenState

func _init(s: GoldenState) -> void:
	state = s

static func tokens(value: String) -> PackedStringArray:
	var regex := RegEx.new()
	regex.compile("[^a-z0-9]+")
	return regex.sub(value.to_lower()," ",true).strip_edges().split(" ",false)

static func word_matches(word: String, candidates: PackedStringArray) -> bool:
	for candidate in candidates:
		if candidate == word or (word.length() >= 4 and candidate.begins_with(word)): return true
	return false

func search(query: String) -> Array:
	var words := tokens(query)
	if words.is_empty(): return []
	var history: Array = state.data.search_history
	if query not in history: history.append(query)
	var results: Array = []
	for page in state.db.web_pages.values():
		var title := tokens(page.title)
		var keywords := tokens(" ".join(page.keywords))
		var body := tokens(page.body)
		var score := 0
		var matches := true
		for word in words:
			if word_matches(word,title): score += 6
			elif word_matches(word,keywords): score += 3
			elif word_matches(word,body): score += 1
			else: matches = false
		if matches: results.append({"page":page,"score":score})
	results.sort_custom(func(a,b): return a.score > b.score if a.score != b.score else a.page.id < b.page.id)
	return results

func open_page(id: String) -> Dictionary:
	var page := state.db.page(id)
	if page.is_empty(): return {}
	if id not in state.data.visited_sites: state.data.visited_sites.append(id)
	return page

func note(id: String) -> bool:
	var page := state.db.page(id)
	if page.is_empty() or id not in state.data.visited_sites: return false
	return state.observe("web_"+id,"Read online: %s." % page.title,"read")
