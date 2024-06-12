import random
from guidance import gen 

def random_part_of_address(address):
    parts = address.split(", ")
    choice = random.choice([1, 2, 3])
    
    if choice == 1:
        # Return only the street address
        return parts[0]
    elif choice == 2:
        # Return the street address and the city
        return ", ".join(parts[:2])
    else:
        # Return the full address
        return address
    
class Navigate:
    destinations = [
        "1600 Pennsylvania Avenue Northwest, Washington, District of Columbia",
        "1 Infinite Loop, Cupertino, California",
        "350 Fifth Avenue, New York, New York",
        "6000 Universal Boulevard, Orlando, Florida",
        "1701 Wynkoop Street, Denver, Colorado",
        "233 South Wacker Drive, Chicago, Illinois",
        "1000 Fifth Avenue, New York, New York",
        "500 South Capitol Boulevard, Boise, Idaho",
        "1020 South Figueroa Street, Los Angeles, California",
        "1500 Sugar Bowl Drive, New Orleans, Louisiana",
        "2311 North 45th Street, Seattle, Washington",
        "50 Massachusetts Avenue Northeast, Washington, District of Columbia",
        "1100 Orange Avenue, Coronado, California",
        "4155 East Grant Road, Tucson, Arizona",
        "3251 South Miami Avenue, Miami, Florida",
        "7000 Hollywood Boulevard, Los Angeles, California",
        "20 West 34th Street, New York, New York",
        "100 Aquarium Wharf, Charleston, South Carolina",
        "700 East Pratt Street, Baltimore, Maryland",
        "301 Front Street, Key West, Florida",
        "1600 Holloway Avenue, San Francisco, California",
        "2101 Constitution Avenue Northwest, Washington, District of Columbia",
        "400 Broad Street, Seattle, Washington",
        "700 Pennsylvania Avenue Northwest, Washington, District of Columbia",
        "1 Dali Boulevard, St. Petersburg, Florida",

        "15 Avenue des Champs-Élysées, Paris, France",
        "1 Plaza Mayor, Madrid, Spain",
        "30 Via del Corso, Rome, Italy",
        "175 Kurfürstendamm, Berlin, Germany",
        "60 Nevsky Prospect, Saint Petersburg, Russia",
        "42 O'Connell Street, Dublin, Ireland",
        "85 Königsallee, Düsseldorf, Germany",
        "10 Kärntner Straße, Vienna, Austria",
        "25 Váci Street, Budapest, Hungary",
        "100 Oxford Street, London, United Kingdom",
        "30 Strøget, Copenhagen, Denmark",
        "50 Náměstí Svobody, Brno, Czech Republic",
        "120 Mannerheimintie, Helsinki, Finland",
        "40 Kungsportsavenyen, Gothenburg, Sweden",
        "90 Andrássy Avenue, Budapest, Hungary",
        "80 Drottninggatan, Stockholm, Sweden",
        "75 La Rambla, Barcelona, Spain",
        "60 Vesterbrogade, Copenhagen, Denmark",
        "15 Piata Unirii, Bucharest, Romania",
        "20 Karl Johans gate, Oslo, Norway"
    ]

    templates = [
        "Navigate to {}",
        "Take me to {}",
        "Drive to {}",
        "Get directions to {}",
        "Route me to {}",
    ]

    def get_name(self):
        return "navigate"

    def get_definition(self):
        return  {    
            "name": self.get_name(),
            "description": "Navigate",
            "parameters": [
                {
                    "name": "destination",
                    "type": "string",
                }
            ]
        }
    
    def generate_parameters(self, llm):
        llm = llm + '{"destination":"' + gen(name="destination", stop='"') + '"}'

        return { "destination": llm["destination"] }
    
    def build_scenario(self, template, destination):
        return {
            "function": self.get_name(),
            "user_input": template.format(destination),
            "expected": {
                "function": self.get_name(),
                "parameters": {
                    "destination": destination,
                }
            }
        }
    
    def build_random_scenario(self):
        destination = random.choice(self.destinations)
        destination = random_part_of_address(destination)
        template = random.choice(self.templates)

        return self.build_scenario(template, destination)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "destination" in parameters
        
        
