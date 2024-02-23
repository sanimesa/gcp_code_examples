import asyncio
import aiohttp
import os
from bs4 import BeautifulSoup
from write_to_bq import write_to_bq

project_id = os.environ.get('PROJECT_ID')  
dataset_id = os.environ.get('DATASET_ID')
table_id = f'{project_id}.{dataset_id}.wine_reviews'

import uuid
def generate_uuid():
    return str(uuid.uuid4())

async def fetch_url(session, n, semaphore):
    async with semaphore:
        # url = f'https://www.winespectator.com/dailypicks/more_than_40/page/{n}'
        url = f'https://www.winespectator.com/dailypicks/20_to_40/page/{n}'
        
        async with session.get(url) as response:
            if response.status == 200:
                page_content = await response.read()
                wines = extractWine(page_content)
                if len(wines) > 0:
                    write_to_bq(table_id, wines)
            else:
                print(f"Failed to fetch page {n}. Status code: {response.status}")

async def scrape_wine_reviews_parallel(concurrency=40):
    semaphore = asyncio.Semaphore(concurrency)  # Control the number of concurrent requests
    start_page = 2
    end_page = 400
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, n, semaphore) for n in range(start_page, end_page + 1)]
        await asyncio.gather(*tasks)

def extractWine(page_content): 
    segment_html = '''
    <div class="md:text-3-xl">
        <h3 class="mb-8">
            <a href="/wine/wine-detail/id/1298120/name/garnacha-campo-de-borja-2020" class="text-gray-darkest">BODEGAS ALTO MONCAYO</a>
        </h3>
        <h4 class="mb-8">
            <a href="/wine/wine-detail/id/1298120/name/garnacha-campo-de-borja-2020" class="text-gray-darkest">Garnacha Campo De Borja 2020</a>
        </h4>
        <p>
            $47
        </p>
        <p>
            A sleek, harmonious red, with a rich undertow of sweet smoke, fig jam and mocha notes, plus generous flavors of blackberry paste, crushed black cherry and grilled thyme. Long and silky, with lots of fragrant spices on the finish. Drink now through 2030. 4,550 cases made, 1,800 cases imported.
            <em>&mdash;Alison Napjus </em>
        </p>
    </div>
    '''

    # Create a BeautifulSoup object to parse the segment HTML
    soup = BeautifulSoup(page_content, 'html.parser')
    segments = soup.find_all('div', class_='md:text-3-xl')
    # print(segments)

    wines = []
    # Iterate over the segments

    for segment in segments: 

        # Extract the vineyard name
        vineyard = segment.select_one('h3 > a').text.strip()

        # Extract the wine name
        wine_name = segment.select_one('h4 > a').text.strip()

        # Extract the price
        price = segment.select_one('p:nth-child(3)').text.strip()
        #remove the leading $ from the price string and check if it is numeric  
        if price[0] == '$':
           price = price[1:]
        if not price.isnumeric():
            price = 0
 
        # Extract the tasting notes
        tasting_notes = segment.select_one('p:nth-child(4)').text.strip()

        notes = tasting_notes
        if 'Drink now through' in tasting_notes:
            notes = tasting_notes.split('Drink now through')[0]
        if 'To be released' in tasting_notes:
            notes = tasting_notes.split('To be released')[0]
        if 'Drink now' in tasting_notes:
            notes = tasting_notes.split('Drink now')[0]
        if 'Best from' in tasting_notes:
            notes = tasting_notes.split('Best from')[0]

        wine = {'id': generate_uuid(), 'vineyard': vineyard, 'wine_name': wine_name, 'price': price, 'tasting_note': notes}

        print(wine)
        wines.append(wine)

    return wines


# Entry point for the asyncio program
if __name__ == "__main__":
    asyncio.run(scrape_wine_reviews_parallel())
