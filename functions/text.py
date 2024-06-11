import random
from guidance import gen 

class Text:
    names = [
        "Michael Johnson",
        "Emily Davis",
        "Christopher Brown",
        "Amanda Martinez",
        "Matthew Wilson",
        "Sarah Miller",
        "Joshua Anderson",
        "Jennifer Taylor",
        "Andrew Thomas",
        "Stephanie Moore",
        "Jessica White",
        "Brian Jackson",
        "Ashley Harris",
        "Brandon Martin",
        "Megan Thompson",
        "James Garcia",
        "Brittany Clark",
        "Justin Lewis",
        "Rachel Walker",
        "Kevin Hall",
        "Samantha Allen",
        "Ryan Young",
        "Lauren King",
        "Nathan Wright",
        "Nicole Scott",
        "John Lopez",
        "Elizabeth Hill",
        "Benjamin Green",
        "Amber Adams",
        "Aaron Baker",
        "Melissa Nelson",
        "Daniel Carter",
        "Michelle Mitchell",
        "Jason Roberts",
        "Amanda Turner",
        "Timothy Phillips",
        "Heather Campbell",
        "Richard Parker",
        "Kimberly Evans",
        "Jeffrey Edwards",
        "Lauren Collins",
        "Sean Stewart",
        "Brittany Flores",
        "Nicholas Sanders",
        "Laura Morris",
        "Eric Rivera",
        "Katherine Price",
        "Adam Hughes",
        "Angela Reed",
        "Tyler Cooper",
        "Jessica Peterson",
        "Brandon Bailey",
        "Danielle Rogers",
        "Scott Bell",
        "Kimberly Ward",
        "Dylan Murphy",
        "Kelly Brooks",
        "Jonathan Powell",
        "Lisa Bryant",
        "Patrick Griffin",
        "Christine James",
        "Mark Howard",
        "Amy Jenkins",
        "Steven Ramirez",
        "Melissa Morgan",
        "Kyle Foster",
        "Stephanie Lee",
        "Kevin Ward",
        "Natalie Richardson",
        "Gregory Cox",
        "Elizabeth Hayes",
        "Charles Long",
        "Olivia Perry",
        "Jordan Russell",
        "Erin Hughes",
        "Alexander Griffin",
        "Christina Butler",
        "Jeremy Barnes",
        "Nicole Ross",
        "Christopher Fisher",
        "Amanda Sanders",
        "David Price",
        "Lauren Powell",
        "Anthony Rivera",
        "Sara Hughes",
        "Jonathan Ward",
        "Rachel Henderson",
        "Zachary Bennett",
        "Kimberly Jenkins",
        "Nathaniel Coleman",
        "Heather Perry",
        "Logan Alexander",
        "Alicia Morgan",
        "Paul Richardson",
        "Chelsea Cox",
        "Brandon Parker",
        "Laura Evans",
        "Stephen Murphy",
        "Michelle Brooks",
        "Thomas Hayes",
        "Alexander Müller",
        "Maria Rossi",
        "Guillaume Lefevre",
        "Ana Novak",
        "János Kovács",
        "Emma García",
        "Nils Johansson",
        "Klara Novakova",
        "Rui Silva",
        "Sofia Andersson",
        "Max Mustermann",
        "Eva Horváth",
        "Marcus Hansen",
        "Isabella Marino",
        "Jakob Schmidt",
        "Sofia Neagu",
        "Laura Popescu",
        "Peter Novak",
        "Katarzyna Kowalski",
        "Oliver Smith",
        "Julia Smirnova",
        "Oscar Martínez",
        "Viktor Orlov",
        "Elena Petrova",
        "Tomáš Dvořák",
        "Maja Kowalczyk",
        "Luca Conti",
        "Anna Muller",
        "Martin Schneider",
        "Louise Dubois",
        "Filippo Bianchi",
        "Teresa Sousa",
        "Elias Virtanen",
        "Karin Hansson",
        "Alexey Ivanov",
        "Elena Dimitrova",
        "Lars Madsen",
        "Hugo Pereira",
        "Kristina Horvat",
        "Monika Kovács",
        "Francesco Rizzo",
        "Gabriella Papadopoulos",
        "Lukas Schmidt",
        "Veronika Kovářová",
        "Anders Larsen",
        "Marie Dupont",
        "Joana Santos",
        "Michaela Kraus",
        "Peter Müller",
        "Isabella Rossi",
        "Magnus Nilsson",
        "Laura Pop",
        "Hans Bauer",
        "Marta Fernández",
        "Viktorija Pavlovic",
        "Dominik Novak",
        "Julia Schmidt",
        "Leif Johansson",
        "Clara Müller",
        "Ivan Petrović",
        "Sofia Georgiou",
        "Oliver Klein",
        "Marco Santoro",
        "Noemi Molnár",
        "Martin Karlsson",
        "Alina Morozova",
        "László Szabó",
        "Katja Bergmann",
        "Anne Weber",
        "David Novák",
        "Renata Kowalska",
        "Antonio Rodríguez",
        "Lucie Novotná",
        "Petar Markov",
        "Sanna Virtanen",
        "Leo Müller",
        "Johanna Schneider",
        "Paul Schmidt",
        "Elena Mihalcea",
        "Henrik Jensen",
        "Marie Boucher",
        "Manuel Pérez",
        "Yulia Smirnova",
        "Agnes Schmidt",
        "Jan Kowalski",
        "Jakob Hansen",
        "Klara Novak",
        "Thomas Müller",
        "Laura Horváth",
        "Afonso Almeida",
        "Ewa Kowalski",
        "Anna Schmidt",
        "Dimitrios Papadopoulos",
        "Tomáš Horák",
        "Victoria Pop",
        "Lars Lindberg",
        "Sander Nielsen",
        "Maria Petrova",
        "Emma Dubois",
        "Marko Novak"
    ]

    messages = [
        "I am running late for dinner",
        "I am running late",
        "I will be there soon",
        "I am on my way",
        "I am stuck in traffic",
        "I am almost there",
        "I am running behind"
    ]

    templates = [
        "Please text {} that {}",
    ]

    def get_name(self):
        return "text"

    def get_definition(self):
        return  {    
            "name": self.get_name(),
            "description": "Send text message to the specified contact",
            "parameters": [
                {
                    "name": "name",
                    "type": "string",
                },
                {
                    "name": "message",
                    "type": "string",
                }
            ]
        }
    
    def generate_parameters(self, llm):
        llm = llm + '{"name":"' + gen(name="name", stop='"') + '",'
        llm = llm + '{"message":"' + gen(name="message", stop='"') + '"}'

        return { "name": llm["name"], "message": llm["message"] }
    
    def build_scenario(self, template, name, message):
        return {
            "function": self.get_name(),
            "user_input": template.format(name, message),
            "expected": {
                "function": self.get_name(),
                "parameters": {
                    "name": name,
                    "message": message
                }
            }
        }
    
    def build_random_scenario(self):
        name = random.choice(self.names)

        # 50% of time just use the first name
        if random.random() < 0.5:
            name = name.split()[0]

        message = random.choice(self.messages)
        template = random.choice(self.templates)

        return self.build_scenario(template, name, message)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "name" in parameters and "message" in parameters
        
        
