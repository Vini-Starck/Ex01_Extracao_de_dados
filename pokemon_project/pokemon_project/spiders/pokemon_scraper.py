import scrapy

class PokemonScraper(scrapy.Spider):
    name = 'pokemon_scraper'
    allowed_domains = ["pokemondb.net"]
    start_urls = ["https://pokemondb.net/pokedex/all"]

    def parse(self, response):
        # Seleciona todos os Pokémon na tabela da página inicial
        pokemons = response.css('#pokedex > tbody > tr')
        
        # Itera sobre cada Pokémon e segue o link para a página de detalhes
        for pokemon in pokemons:
            link = pokemon.css("td.cell-name > a::attr(href)").get()
            if link:
                yield response.follow(link, self.parse_pokemon)

    def parse_pokemon(self, response):
        # Extrai informações detalhadas de cada Pokémon individual
        yield {
            'pokemon_name': response.css('#main > h1::text').get(),
            'pokemon_id': response.css('.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get(),
            'height': response.css('.vitals-table > tbody > tr:contains("Height") > td::text').get(),
            'weight': response.css('.vitals-table > tbody > tr:contains("Weight") > td::text').get(),
            'types': response.css('.vitals-table > tbody > tr:contains("Type") > td a::text').getall()
        }
