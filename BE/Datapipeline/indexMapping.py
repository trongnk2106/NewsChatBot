indexMapping = {
    "properties": {
        "title": {
            "type" : "text",
        },
        "date": {
            "type" : "text",
        },
        "description": {
            "type" : "text",
        },
        "paragraphs": {
            "type" : "text",
        },
        "author": {
            "type" : "text",
        },
        "link": {
            "type" : "text",
        },
        "embedding": {
            "type" : "dense_vector",
            "dims" : 768,
            "index" : "true",
            "similarity" : "cosine"
        },
        
    }
}

# 'title', 'date', 'description', 'paragraphs', 'author', 'link', 'tokenizedVector'
