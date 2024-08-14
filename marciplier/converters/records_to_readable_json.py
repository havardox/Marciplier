from marciplier.marc_record import MarcRecord

def records_to_readable_json(records: list[MarcRecord]):
    result = {
        "title": None,
        "subtitle": None,
        "volume_number": None,
        "authors": [],
        "year_published": None,
        "country_published": None,
        "publisher": None,
        "num_pages": None,
        "isbn": None,
        "series": None,
        "dimensions": None,
        "language": None,
        "original_language": None,
        "genres": [],
        "designers": [],
        "illustrators": [],
        "editors": [],
        "translators": [],
    }
    
    for record in records:
        # Title (MARC 245)
        title_field = record.get_field("245")
        if title_field:
            for field in title_field:
                title = ''.join(field.get_subfield('a')[0].values).rstrip(" /")
                subtitle = ''.join(field.get_subfield('b')[0].values).rstrip(" /")
                result["title"] = title if title else result["title"]
                result["subtitle"] = subtitle if subtitle else result["subtitle"]

        # Authors (MARC 100 and 700)
        author_field = record.get_field("100")
        if author_field:
            for field in author_field:
                author = ''.join(field.get_subfield('a')[0].values).rstrip(".")
                result["authors"].append(author)

        contributors_field = record.get_field("700")
        if contributors_field:
            for field in contributors_field:
                contributor = ''.join(field.get_subfield('a')[0].values).rstrip(".")
                result["authors"].append(contributor)

        # Publisher (MARC 260 or 264)
        publisher_field = record.get_field("260") or record.get_field("264")
        if publisher_field:
            for field in publisher_field:
                publisher = ''.join(field.get_subfield('b')[0].values).rstrip(",")
                result["publisher"] = publisher if publisher else result["publisher"]

        # Year Published (MARC 260 or 264)
        if publisher_field:
            for field in publisher_field:
                year = ''.join(field.get_subfield('c')[0].values).rstrip(".")
                result["year_published"] = year if year else result["year_published"]

        # ISBN (MARC 020)
        isbn_field = record.get_field("020")
        if isbn_field:
            for field in isbn_field:
                isbn = ''.join(field.get_subfield('a')[0].values).split(' ')[0]
                result["isbn"] = isbn if isbn else result["isbn"]

        # Language (MARC 041)
        language_field = record.get_field("041")
        if language_field:
            for field in language_field:
                language = ''.join(field.get_subfield('a')[0].values)
                result["language"] = language if language else result["language"]

        # Number of Pages (MARC 300)
        pages_field = record.get_field("300")
        if pages_field:
            for field in pages_field:
                pages = ''.join(field.get_subfield('a')[0].values).split(' ')[0]
                result["num_pages"] = pages if pages else result["num_pages"]

        # Series (MARC 490)
        series_field = record.get_field("490")
        if series_field:
            for field in series_field:
                series = ''.join(field.get_subfield('a')[0].values)
                result["series"] = series if series else result["series"]

        # Genres (MARC 655)
        genres_field = record.get_field("655")
        if genres_field:
            for field in genres_field:
                genre = ''.join(field.get_subfield('a')[0].values)
                result["genres"].append(genre)

        # Additional contributors (Designers, Illustrators, Editors, Translators) using MARC 700
        if contributors_field:
            for field in contributors_field:
                relator_code = ''.join(field.get_subfield('e')[0].values).lower()
                name = ''.join(field.get_subfield('a')[0].values).rstrip(".")
                if "designer" in relator_code:
                    result["designers"].append(name)
                elif "illustrator" in relator_code:
                    result["illustrators"].append(name)
                elif "editor" in relator_code:
                    result["editors"].append(name)
                elif "translator" in relator_code:
                    result["translators"].append(name)

    return result