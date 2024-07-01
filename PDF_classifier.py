# import pymupdf
#
#
# def pdf_to_text(pdf_path):
#     doc = pymupdf.open(pdf_path)
#     text = ""
#     # assuming that the first 5 pages contain relevant information
#     for page in doc.pages(0, 6):
#         text += page.get_text().encode("utf-8") + "\n"
#     return text

headers = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9',
  'authorizationtoken': '5H3sE+8nY0FRWU6ckR30zC/Ouj1LwZYGgC633mIb6iWXHgz9Q6Sp6pqkOhR2CqM8yI4Q5ZB1D/GKm2VWEMNU9ZkKXLwictLoQ20v0aw/ZCfUHJERKyMLjZ62BJ24lQtYB6f9Z4KK4j==',
  'dnt': '1',
  'origin': 'https://www.sgx.com',
  'priority': 'u=1, i',
  'referer': 'https://www.sgx.com/',
  'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}

headers2 = {
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'authorizationtoken': '4Q26oeKGQOsF4P8vnKtAFzUPtYi1Hnzy95U4/j2jtjiITsHjn/Qds5KWyFTkkyv+8u2JRP3AVsvn3t6AhYLYwR8fNo6kB9S97dh6pfPXs2+oX2L47Ee5HggwyHdNsXo4s6J3ts5pJD==',
      'dnt': '1',
      'origin': 'https://www.sgx.com',
      'priority': 'u=1, i',
      'referer': 'https://www.sgx.com/',
      'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }

print(headers == headers2)
