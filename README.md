# Marciplier

I wrote this because I couldn't find a good tool that converts MARCXML to JSON at an okay-ish speed. This program is memory efficient and fast as it uses Python's Simple API for XML (SAX) to parse the XML. SAX is a streaming API and doesn't load the entire tree into memory. This program works pretty well with large files (2 GB and upwards).

The JSON format is by own intuition. I don't think there's a any recognized standard for a JSON representation of MARC 21.

If you found this repo through Google, please do consider giving it a star. It really does help.
